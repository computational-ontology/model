"""Builds notebooks/02_stage1_llm_bakeoff.ipynb. Run from the repo root: python notebooks/build_02.py"""

from pathlib import Path

import nbformat as nbf
from _shared_cells import ENV_CELL, LOADER_CELL, PROMPT_CELL, TOKEN_CELL

nb = nbf.v4.new_notebook()
C: list = []
md, code = (lambda s: C.append(nbf.v4.new_markdown_cell(s))), (lambda s: C.append(nbf.v4.new_code_cell(s)))

md("""# 02 · Stage 1 bake-off — three open-weights models on the 100-section pilot

Sprint 1 of the New-Realism Analyzer (github.com/computational-ontology/model). The three
candidates fixed in decision D15 — Gemma-4-12B-it, Qwen3.5-9B, EuroLLM-9B-Instruct-2512 — each
annotate the **same 100 pilot sections** (`data/splits/pilot_100.json`, seed 20260914, stratified by
chapter type × language) under the **same prompt, grammar and decoding**: XGrammar-constrained
compact JSON (D16), greedy, `max_new_tokens=1600`, one pass. Every output becomes a `Stage1Record`
(section by id + hash, emitter = the model, date, codebook and prompt version, decoding settings)
and is written to JSONL as it is produced.

What this notebook is **not**: it is not the evaluation. Model–human agreement needs the gold
labels of the annotation campaign, which starts only after the OSF preregistration. What it gives
now: (1) a machine-readable silver set for every candidate, (2) format discipline per model —
validity, EOS termination, verbatim spans, duplicates, tokens and seconds, (3) model–model
agreement on the T5 operator at section level, and (4) a small prompt-paraphrase sensitivity
check, because check 3 showed that wording alone can flip a label.

Load-check results feeding this design: `02a` v1–v2.2 (all three load in fp16 on 2×T4; the
grammar works on all three; Qwen needs the EOS union; EuroLLM is usable only under the grammar;
decoding mode can change labels, so constrained is the only mode here).

Settings: Accelerator **GPU T4 ×2**, Internet **on**, secret `HF_TOKEN`, dataset
`luisdscientist/nra-snapshot-em`. Expected wall time: ~1.5–2 h per model (100 sections ×
30–120 s) → run all three in one version (< 12 h) or set `ONLY_MODEL` below to split.""")

md("""## 0 · Environment and run parameters

Same environment as `02a` v2.2. `ONLY_MODEL` restricts the run to one candidate (a version per
model keeps each run under two hours); `LIMIT` caps the number of sections (smoke test);
`SENSITIVITY_N` is the number of sections for the paraphrase check (0 disables it).""")
code(ENV_CELL + """

ONLY_MODEL = None        # e.g. "google/gemma-4-12B-it" — None runs all three
LIMIT = None             # e.g. 10 for a smoke test — None runs the whole pilot
SENSITIVITY_N = 20       # sections for the prompt-paraphrase check on the first model; 0 = skip
OUT_DIR = "/kaggle/working/stage1"
import os as _os; _os.makedirs(OUT_DIR, exist_ok=True)
print("params:", dict(ONLY_MODEL=ONLY_MODEL, LIMIT=LIMIT, SENSITIVITY_N=SENSITIVITY_N, OUT_DIR=OUT_DIR))""")

md("""## 1 · Hugging Face token""")
code(TOKEN_CELL)

md("""## 2 · The pilot: 100 sections, hash-verified

The draw is fetched from the repository at `main`; every text is read from the mounted snapshot
and its SHA-256 checked against the manifest hash before use. A mismatch stops the run: the record
must be the record.""")
code("""import requests, hashlib, unicodedata
ROOT = "/kaggle/input/datasets/luisdscientist/nra-snapshot-em"
RAW = "https://raw.githubusercontent.com/computational-ontology/model/main/"
pilot_meta = requests.get(RAW + "data/splits/pilot_100.json", timeout=30).json()
pilot = pilot_meta["sections"]
if LIMIT:
    pilot = pilot[:LIMIT]

def fname(cid, sid, lang):
    return f"{cid}__{sid.replace('/', '_')}__{lang}.txt"

def sha256_text(text):
    return hashlib.sha256(unicodedata.normalize("NFC", text).strip().encode("utf-8")).hexdigest()

sections = []
for rec in pilot:
    text = open(f"{ROOT}/{fname(rec['constitution_id'], rec['section_id'], rec['lang'])}", encoding="utf-8").read()
    assert sha256_text(text) == rec["sha256"], f"hash mismatch on {rec['constitution_id']} §{rec['section_id']}"
    sections.append({**rec, "text": text})
import collections
print(len(sections), "sections verified |", dict(collections.Counter(s["lang"] for s in sections)),
      "| seed", pilot_meta["seed"], "| chars: min", min(len(s["text"]) for s in sections),
      "median", sorted(len(s["text"]) for s in sections)[len(sections)//2], "max", max(len(s["text"]) for s in sections))""")

md("""## 3 · Schema and prompt (frozen)

Byte-identical to `02a` v2.2, so `PROMPT_VERSION` is the same `p1-e482d89f` and the two
notebooks' outputs are comparable. The prompt is the wording that will be named in the
preregistration; it does not change inside this notebook.""")
code(PROMPT_CELL)

md("""## 4 · Loader and generator

Identical to `02a` v2.2 (fp16 across both T4s, thinking off, XGrammar grammar per model, EOS
union, greedy, duplicate mentions removed and counted).""")
code(LOADER_CELL)

md("""## 5 · Records

`make_record` wraps a model output into a `Stage1Record`: the section by id and hash (never the
text), the model as emitter, an aware UTC timestamp, codebook and prompt versions, the decoding
settings, the validated output, and `parse_ok` / `verbatim_ok`. Records are appended to one
JSONL file per model as they are produced, so a killed session loses at most one section; on a
re-run with a previous output attached, already-done sections are skipped.

Two files per model: `*.jsonl` keeps the verbatim spans (private working file — the spans are
quotations of Constitute text, CC BY-NC) and `*.offsets.jsonl` replaces every span by character
offsets into the section, which is the form that can be released with the hash-only manifest.""")
code("""from datetime import datetime, timezone
from nra.schema import Stage1Record

CODEBOOK_VERSION = "1.0"
DECODING = {"grammar": True, "decoder": "xgrammar", "do_sample": False, "max_new_tokens": 1600}

def slug(model_id):
    return model_id.replace("/", "__")

def make_record(sec, model_id, obj, verdict, raw, n_in, n_out, dt, stopped):
    out = obj if obj is not None else FAILED_OUTPUT
    rec = Stage1Record(
        constitution_id=sec["constitution_id"], section_id=sec["section_id"], lang=sec["lang"],
        sha256=sec["sha256"], annotator=model_id, emitter_kind="model",
        emitted_at=datetime.now(tz=timezone.utc), codebook_version=CODEBOOK_VERSION,
        prompt_version=PROMPT_VERSION, decoding=DECODING, output=out,
        parse_ok=obj is not None, verbatim_ok=(obj is not None and verdict.startswith("verbatim ok")),
    )
    d = rec.model_dump(mode="json")
    d["run"] = {"n_in": n_in, "n_out": n_out, "sec": round(dt, 1), "stopped_by_eos": stopped,
                "verdict": verdict, "chapter_type": sec["chapter_type"], "n_dup_removed": _ndup(verdict)}
    if obj is None:
        d["raw_head"] = raw[:400]  # private file only; helps diagnose the failure
    return d

from nra.schema import Claim
# Stage1Record requires an output; a failed parse gets this sentinel and parse_ok=False.
FAILED_OUTPUT = Stage1Output(t2=[], t5=[Claim(claim="<parse failed>", operator="other", markers=[])], notes="parse failed")

def _ndup(verdict):
    import re
    m = re.search(r"(\\d+) duplicate", verdict)
    return int(m.group(1)) if m else 0

def to_offsets(d, text):
    # release form: spans → [start, end] character offsets; unmatched spans → null
    import copy
    e = copy.deepcopy(d)
    e.pop("raw_head", None)
    def off(s):
        i = text.find(s)
        return [i, i + len(s)] if i >= 0 else None
    for m in e["output"]["t2"]:
        m["mention"] = off(m["mention"])
    for c in e["output"]["t5"]:
        c["claim"] = off(c["claim"])
        c["markers"] = [off(mk) for mk in c["markers"]]
    return e

def done_keys(path):
    keys = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                keys.add((r["constitution_id"], r["section_id"], r["lang"]))
    return keys
print("record helpers ready")""")

md("""## 6 · Run: every candidate over the pilot

One model at a time. Per section: generate under the grammar, parse, build the record, append
both files, print one status line. A failed generation is recorded with `parse_ok=false` and the
exception, never skipped silently. GPUs are freed between models.""")
code("""import traceback
runs = [c for c in CANDIDATES if ONLY_MODEL is None or c[0] == ONLY_MODEL]
timing = {}
for model_id, kind in runs:
    print("=" * 100); print(model_id, "|", len(sections), "sections")
    free()
    try:
        tok, model, grammar = load(model_id, kind)
    except Exception as e:  # noqa: BLE001
        print("LOAD FAILED:", type(e).__name__, str(e)[:300]); continue
    path = f"{OUT_DIR}/{slug(model_id)}.jsonl"; path_off = f"{OUT_DIR}/{slug(model_id)}.offsets.jsonl"
    skip = done_keys(path)
    t_model = time.time(); n_ok = n_verb = 0; n_done = 0
    for i, sec in enumerate(sections, 1):
        key = (sec["constitution_id"], sec["section_id"], sec["lang"])
        if key in skip:
            continue
        try:
            raw, n_in, n_out, dt, stopped = generate(tok, model, kind, sec["text"], grammar=grammar)
            obj, verdict = parse(raw, sec["text"])
        except Exception as e:  # noqa: BLE001
            raw, n_in, n_out, dt, stopped = "", 0, 0, 0.0, False
            obj, verdict = None, f"generation failed: {type(e).__name__}: {str(e)[:160]}"
            traceback.print_exc(limit=1)
        d = make_record(sec, model_id, obj, verdict, raw, n_in, n_out, dt, stopped)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(d, ensure_ascii=False) + "\\n")
        with open(path_off, "a", encoding="utf-8") as f:
            f.write(json.dumps(to_offsets(d, sec["text"]), ensure_ascii=False) + "\\n")
        n_done += 1; n_ok += d["parse_ok"]; n_verb += bool(d["verbatim_ok"])
        labels = [c["operator"] for c in d["output"]["t5"]] if d["parse_ok"] else []
        print(f"[{i:3d}/{len(sections)}] {sec['lang']} {sec['constitution_id']} §{sec['section_id']} | {n_out} tok {dt:.0f}s eos={stopped} | {verdict[:60]} | T5={collections.Counter(labels).most_common(3)}")
    timing[model_id] = round(time.time() - t_model, 1)
    print(f"-- {model_id}: {n_done} new records, {n_ok} valid, {n_verb} verbatim, {timing[model_id]} s")
    del model, tok, grammar; free()
print("timing (s):", timing)""")

md("""## 7 · Format discipline and throughput per model

Reads the JSONL files back (so this cell works on an attached previous output too) and reports,
per model: records, valid, EOS-terminated, fully verbatim, duplicates removed, tokens and seconds
per section, and the T5 label distribution per language. These are properties of the *emitters*,
not measures of correctness.""")
code("""import glob, pandas as pd
rows = []
for path in sorted(glob.glob(f"{OUT_DIR}/*.jsonl")):
    if path.endswith(".offsets.jsonl"):
        continue
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            rows.append({"model": r["annotator"], "lang": r["lang"], "cid": r["constitution_id"], "sid": r["section_id"],
                         "chapter_type": r["run"]["chapter_type"], "parse_ok": r["parse_ok"], "verbatim_ok": bool(r["verbatim_ok"]),
                         "eos": r["run"]["stopped_by_eos"], "n_out": r["run"]["n_out"], "sec": r["run"]["sec"],
                         "n_dup": r["run"]["n_dup_removed"], "n_t2": len(r["output"]["t2"]), "n_t5": len(r["output"]["t5"]),
                         "labels": [c["operator"] for c in r["output"]["t5"]] if r["parse_ok"] else []})
df = pd.DataFrame(rows)
print(len(df), "records")
disc = df.groupby("model").agg(records=("cid", "size"), valid=("parse_ok", "mean"), eos=("eos", "mean"),
                               verbatim=("verbatim_ok", "mean"), dup_per_sec=("n_dup", "mean"),
                               tok_mean=("n_out", "mean"), sec_mean=("sec", "mean"), sec_p90=("sec", lambda s: s.quantile(.9)),
                               t2_mean=("n_t2", "mean"), t5_mean=("n_t5", "mean")).round(2)
display(disc)
lab = df.explode("labels").dropna(subset=["labels"]).groupby(["model", "lang", "labels"]).size().unstack(fill_value=0)
lab = lab.div(lab.sum(axis=1), axis=0).round(2)
print("\\nT5 label shares per model and language (claim level):"); display(lab)""")

md("""## 8 · Model–model agreement on the operator (section level)

Models segment claims differently, so agreement is computed at **section level** on the
dominant T5 label (ties → `other`). Pairwise raw agreement and Krippendorff's α (nominal) across
the three emitters. This is agreement between machines under one prompt — a ceiling-free
diagnostic, not the reliability of the task; that comes from the human campaign (D11 gates).""")
code("""import itertools, numpy as np
def dominant(labels):
    if not labels:
        return None
    c = collections.Counter(labels).most_common()
    return c[0][0] if len(c) == 1 or c[0][1] > c[1][1] else "other"
df["dom"] = df["labels"].map(dominant)
piv = df.pivot_table(index=["cid", "sid", "lang"], columns="model", values="dom", aggfunc="first")
models = list(piv.columns)
print("sections with a dominant label from every model:", int(piv.dropna().shape[0]))
for a, b in itertools.combinations(models, 2):
    both = piv[[a, b]].dropna()
    print(f"agreement {a.split('/')[-1]} vs {b.split('/')[-1]}: {(both[a] == both[b]).mean():.2f} on {len(both)} sections")
try:
    import krippendorff
    cats = {"naturalised": 0, "revealed": 1, "other": 2}
    mat = np.array([[cats.get(v, np.nan) if isinstance(v, str) else np.nan for v in piv[m]] for m in models], dtype=float)
    print("Krippendorff alpha (nominal, section-level dominant label, 3 emitters):", round(krippendorff.alpha(reliability_data=mat, level_of_measurement="nominal"), 3))
except Exception as e:  # noqa: BLE001
    print("alpha not computed:", type(e).__name__, str(e)[:120])
print("\\ndominant label by chapter type and model (share naturalised):")
display(df[df["dom"].notna()].assign(nat=lambda x: x["dom"] == "naturalised").pivot_table(index="chapter_type", columns="model", values="nat", aggfunc="mean").round(2))""")

md("""## 9 · Prompt-paraphrase sensitivity (first model, first `SENSITIVITY_N` sections)

Check 3 found that changing one sentence of the prompt flipped Qwen's label on Honduras §1594.
Here the **rules stay identical** and only their wording changes (paraphrase B); the same model
re-annotates the first `SENSITIVITY_N` sections under B and we count how often the dominant T5
label moves. A high flip rate means the label is partly an artefact of phrasing — something the
preregistration must state, and the codebook must tighten.""")
code("""SYSTEM_B = SYSTEM.replace(
    "label HOW each claim presents what it asserts, not whether it is true",
    "decide, for each claim, the manner in which it puts forward its content — never whether the content is correct").replace(
    "the trigger or situation is stated as a plain fact of the world, with no actor, assessment or check",
    "the triggering circumstance is written as something that simply obtains, without naming who establishes it, any assessment, or any review").replace(
    "the claim exposes its own act character — who declares, that an assessment is required, a procedure, a limit, a review, a consent",
    "the clause makes visible that an act is involved — the declaring authority, a required finding, a procedure, a limit, a review, a consent")
assert SYSTEM_B != SYSTEM
PROMPT_VERSION_B = "p1b-" + hashlib.sha256(SYSTEM_B.encode()).hexdigest()[:8]
print("paraphrase B:", PROMPT_VERSION_B)

sens = []
if SENSITIVITY_N and runs:
    model_id, kind = runs[0]
    free(); tok, model, grammar = load(model_id, kind)
    base_path = f"{OUT_DIR}/{slug(model_id)}.jsonl"
    base = {}
    with open(base_path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line); base[(r["constitution_id"], r["section_id"], r["lang"])] = r
    def messages_b(text):
        return [{"role": "system", "content": SYSTEM_B}, {"role": "user", "content": "Section:\\n\\n" + text + "\\n\\nReturn the JSON object."}]
    _orig = messages_for
    messages_for = messages_b  # generate() reads the module-level name
    for sec in sections[:SENSITIVITY_N]:
        key = (sec["constitution_id"], sec["section_id"], sec["lang"])
        raw, n_in, n_out, dt, stopped = generate(tok, model, kind, sec["text"], grammar=grammar)
        obj, verdict = parse(raw, sec["text"])
        d = make_record(sec, model_id, obj, verdict, raw, n_in, n_out, dt, stopped); d["prompt_version"] = PROMPT_VERSION_B
        with open(f"{OUT_DIR}/{slug(model_id)}.paraphraseB.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(d, ensure_ascii=False) + "\\n")
        a = base.get(key)
        dom_a = dominant([c["operator"] for c in a["output"]["t5"]]) if a and a["parse_ok"] else None
        dom_b = dominant([c["operator"] for c in d["output"]["t5"]]) if d["parse_ok"] else None
        sens.append({"cid": key[0], "sid": key[1], "lang": key[2], "A": dom_a, "B": dom_b, "same": dom_a == dom_b})
        print(f"{key[2]} {key[0]} §{key[1]}: A={dom_a} B={dom_b}")
    messages_for = _orig
    del model, tok, grammar; free()
    sdf = pd.DataFrame(sens)
    print(f"\\n{model_id}: dominant label unchanged under paraphrase B in {sdf['same'].mean():.2f} of {len(sdf)} sections")
else:
    print("sensitivity check skipped")""")

md("""## 10 · What this run establishes

Fill in after the run (numbers from §7–§9):

- Records: __ per model; valid __ / EOS __ / verbatim __; seconds per section (mean / p90): __.
- T5 label shares per model and language: __ (naturalised-heavy? revealed-heavy?).
- Section-level model–model agreement: pairwise __, α = __. Chapter types where the emitters disagree most: __.
- Paraphrase sensitivity (model __, N = __): dominant label unchanged in __ % of sections.
- Codebook v1.1 candidates surfaced by the disagreements (list section ids): __.
- GPU hours used: __ of the 30-hour weekly quota.

Everything here is amendable output of the pipeline (Table 1). The JSONL files are the first
machine-produced *inscriptions* of the project (weak documents, emitter = model, date = this run);
the `.offsets.jsonl` form is what can be published alongside the hash-only manifest.""")

nb["cells"] = C
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["language_info"] = {"name": "python"}
out = Path(__file__).with_name("02_stage1_llm_bakeoff.ipynb")
nbf.write(nb, out)
print("wrote", out, len(C), "cells")

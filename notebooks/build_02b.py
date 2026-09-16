"""Builds notebooks/02b_stage1_preamble_bakeoff.ipynb (campaign 1, preambles, codebook v2.0).
Run from the repo root: python notebooks/build_02b.py. Derived from build_02.py (the em bake-off, frozen)."""

from pathlib import Path

import nbformat as nbf
from _shared_cells import ENV_CELL, LOADER_CELL, PROMPT_CELL_Q1, TOKEN_CELL

nb = nbf.v4.new_notebook()
C: list = []
md, code = (lambda s: C.append(nbf.v4.new_markdown_cell(s))), (lambda s: C.append(nbf.v4.new_code_cell(s)))

md("""# 02b · Stage 1 bake-off on preambles — three open-weights models on the 100-preamble pilot (codebook v2.0, prompt q1) — v1.1

Campaign 1 of the New-Realism Analyzer (github.com/computational-ontology/model) after the pivot to
**preambles as the unit** (decisions D20–D23; codebook v2.0, release `v2.0.0`, Zenodo DOI
10.5281/zenodo.22784017). The three candidates fixed in D15 — Gemma-4-12B-it, Qwen3.5-9B,
EuroLLM-9B-Instruct-2512 — each annotate the **same 100 pilot preambles**
(`data/splits/pilot_preamble_100.json`, seed 20260916, stratified by language × length band)
under the **same prompt, grammar and decoding**: XGrammar-constrained compact JSON (D16), greedy,
one pass. Every output becomes a `Stage1Record` (preamble by id + hash, emitter = the model, date,
codebook and prompt version, decoding settings) and is written to JSONL as it is produced.

What changes against the `em` bake-off (notebook 02, v1–v2): the object (whole preambles, 200 to
20 000 characters), the codebook (T5 = `ground` + `frame` + `operator`, decided from the ground —
codebook §3), the prompt (`q1`, written for founding inscriptions with the D19 discipline: no
quotable example markers), `max_new_tokens` raised for long preambles, and the agreement section,
which now reports α on `operator`, `ground` and `frame` separately. What stays: loader, grammar,
EOS union, record envelope, offsets form, resume logic, the D18 measures.

What this notebook is **not**: it is not the evaluation. Model–human agreement needs the gold labels
of the annotation campaign, which starts only after the OSF preregistration. Three emitters agreeing
under one prompt is solidarity among emitters, not objectivity (*Manifiesto*, pp. 97–99).

Settings: Accelerator **GPU T4 ×2**, Internet **on**, secret `HF_TOKEN`, dataset
`luisdscientist/nra-snapshot-preamble`. Expected wall time: ~1–2.5 h per model (long preambles
cost more tokens) → run all three in one version or set `ONLY_MODEL` to split.

**v1.1 (retry of the capped preambles).** v1 (Versions 2–3, 16 Sep 2026) lost 4 (Gemma) and 6 (Qwen)
`long` preambles at the 3 072-token cap. v1.1 attaches the v1 output as an input, keeps every record
with `parse_ok=true`, drops the failed ones and regenerates them under `MAX_NEW_TOKENS=8192`
(`RETRY_FAILED`); the paraphrase-B file is carried forward unchanged. The analysis cells also report
`operator_from_ground` (the operator the codebook rule derives from the emitted `ground`) next to the
emitted operator, because v1 showed both models emitting `ground=act` with `operator=naturalised`.""")

md("""## 0 · Environment and run parameters

Same environment as `02a` v2.2. `ONLY_MODEL` restricts the run to one candidate (a version per
model keeps each run under two hours); `LIMIT` caps the number of sections (smoke test);
`SENSITIVITY_N` is the number of sections for the paraphrase check (0 disables it).""")
code(ENV_CELL + """

ONLY_MODEL = None        # e.g. "google/gemma-4-12B-it" — None runs all three
LIMIT = None             # e.g. 10 for a smoke test — None runs the whole pilot
SENSITIVITY_N = 0        # sections for the prompt-paraphrase check on the first model; 0 = skip (v1 did 20 on Gemma)
MAX_NEW_TOKENS = 8192    # v1 capped at 3072 and lost the longest preambles (~20 000 chars)
RETRY_FAILED = True      # seed OUT_DIR from an attached previous output, dropping parse_ok=false records
PREV_GLOB = "/kaggle/input/**/stage1_preamble"   # where an attached notebook output mounts (any version)
OUT_DIR = "/kaggle/working/stage1_preamble"   # em records live in data/annotations/stage1*/ — never mixed
import os as _os; _os.makedirs(OUT_DIR, exist_ok=True)
print("params:", dict(ONLY_MODEL=ONLY_MODEL, LIMIT=LIMIT, SENSITIVITY_N=SENSITIVITY_N, MAX_NEW_TOKENS=MAX_NEW_TOKENS, RETRY_FAILED=RETRY_FAILED, OUT_DIR=OUT_DIR))""")

md("""## 1 · Hugging Face token""")
code(TOKEN_CELL)

md("""## 2 · The pilot: 100 preambles, hash-verified

The draw is fetched from the repository at `main`; every text is read from the mounted snapshot
(the dataset was uploaded as a folder, so the `.txt` directory is resolved by walking the mount —
lesson of notebook 01b) and its SHA-256 checked against the manifest hash before use. A mismatch
stops the run: the record must be the record.""")
code("""import requests, hashlib, unicodedata
MOUNT = "/kaggle/input/datasets/luisdscientist/nra-snapshot-preamble"
ROOT = next((os.path.join(d, "") for d, _, f in os.walk(MOUNT) if any(x.endswith(".txt") for x in f)), MOUNT).rstrip("/")
RAW = "https://raw.githubusercontent.com/computational-ontology/model/main/"
pilot_meta = requests.get(RAW + "data/splits/pilot_preamble_100.json", timeout=30).json()
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
print(len(sections), "preambles verified at", ROOT, "|", dict(collections.Counter((s["lang"], s["length_band"]) for s in sections)),
      "| seed", pilot_meta["seed"], "| chars: min", min(len(s["text"]) for s in sections),
      "median", sorted(len(s["text"]) for s in sections)[len(sections)//2], "max", max(len(s["text"]) for s in sections))""")

md("""## 3 · Schema and prompt (q1, frozen)

`PROMPT_CELL_Q1` in `notebooks/_shared_cells.py` is the codebook v2.0 §3 test in prompt form: the
T2 rules, the `ground` and `frame` value definitions (kinds of words, never quoted phrases — D19),
the operator rule, the three-step test and the rules that go with it; markers are declared
quotations. Expected `PROMPT_VERSION = q1-f2f23d89` (computed locally against schema v2.0; the cell
prints it — if it differs, the schema or the wording changed and the run is not the preregistered
one). The grammar is compiled from the v2.0 schema, so every claim carries `frame` and `ground`.""")
code(PROMPT_CELL_Q1)

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

from nra.schema import CODEBOOK_VERSION   # "2.0" from the installed package, never typed here
assert CODEBOOK_VERSION == "2.0", CODEBOOK_VERSION
DECODING = {"grammar": True, "decoder": "xgrammar", "do_sample": False, "max_new_tokens": MAX_NEW_TOKENS}

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
    bad = check_verbatim(obj, sec["text"]) if obj is not None else []
    soft = [s for s in bad if _norm(s) not in _norm(sec["text"])]   # still missing after normalisation
    d["run"] = {"n_in": n_in, "n_out": n_out, "sec": round(dt, 1), "stopped_by_eos": stopped,
                "verdict": verdict, "length_band": sec["length_band"], "n_dup_removed": _ndup(verdict),
                "n_nonverbatim": len(bad), "n_nonverbatim_after_norm": len(soft)}
    if obj is None:
        d["raw_head"] = raw[:400]  # private file only; helps diagnose the failure
    return d

from nra.schema import Claim
# Stage1Record requires an output; a failed parse gets this sentinel and parse_ok=False.
FAILED_OUTPUT = Stage1Output(t2=[], t5=[Claim(claim="<parse failed>", operator="other", markers=[], frame="none", ground="none")], notes="parse failed")

import re as _re, unicodedata as _ud
def _norm(s):
    # case, whitespace and punctuation folded; accents kept (they are part of the record)
    s = _ud.normalize("NFC", s).casefold()
    return _re.sub("[\\\\s.,;:()\\\\[\\\\]«»\\"'“”‘’]+", " ", s).strip()

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

md("""## 5b · Resume from an attached previous output (v1.1)

If a previous version's output is attached as an input, its `stage1_preamble/` files are copied into
`OUT_DIR` so that §6 skips the sections already done and §7–§9 read the complete set. With
`RETRY_FAILED`, records with `parse_ok=false` (the 3 072-token cap in v1) are dropped from both the
span and the offsets file, so §6 regenerates exactly those; the paraphrase-B file is copied whole.
A record is never overwritten: the new attempt is a new inscription with its own `emitted_at`.""")
code("""import glob, shutil
prev_dirs = sorted(set(glob.glob(PREV_GLOB, recursive=True)))
print("previous outputs found:", prev_dirs or "none")
for pdir in prev_dirs:
    for src in sorted(glob.glob(f"{pdir}/*.jsonl")):
        name = os.path.basename(src)
        dst = f"{OUT_DIR}/{name}"
        if os.path.exists(dst):
            print(f"  {name}: already in OUT_DIR, left as is"); continue
        if "paraphrase" in name or not RETRY_FAILED:
            shutil.copy(src, dst); print(f"  {name}: copied"); continue
        kept = dropped = 0
        with open(src, encoding="utf-8") as fi, open(dst, "w", encoding="utf-8") as fo:
            for line in fi:
                r = json.loads(line)
                if r["parse_ok"]:
                    fo.write(line if line.endswith("\\n") else line + "\\n"); kept += 1
                else:
                    dropped += 1; print(f"    retry: {r['annotator']} {r['constitution_id']} ({r['lang']}) — {r['run']['verdict'][:60]}")
        print(f"  {name}: {kept} kept, {dropped} dropped for retry")""")

md("""## 6 · Run: every candidate over the pilot preambles

One model at a time. Per section: generate under the grammar, parse, build the record, append
both files, print one status line. A failed generation is recorded with `parse_ok=false` and the
exception, never skipped silently. GPUs are freed between models.""")
code("""import traceback
runs = [c for c in CANDIDATES if ONLY_MODEL is None or c[0] == ONLY_MODEL]
timing = {}
for model_id, kind in runs:
    print("=" * 100); print(model_id, "|", len(sections), "preambles")
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
            raw, n_in, n_out, dt, stopped = generate(tok, model, kind, sec["text"], grammar=grammar, max_new_tokens=MAX_NEW_TOKENS)
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
        grounds = [c["ground"] for c in d["output"]["t5"]] if d["parse_ok"] else []
        print(f"[{i:3d}/{len(sections)}] {sec['lang']} {sec['constitution_id']} {sec['length_band']} | {n_out} tok {dt:.0f}s eos={stopped} | {verdict[:50]} | op={dict(collections.Counter(labels))} ground={collections.Counter(grounds).most_common(3)}")
    timing[model_id] = round(time.time() - t_model, 1)
    print(f"-- {model_id}: {n_done} new records, {n_ok} valid, {n_verb} verbatim, {timing[model_id]} s")
    del model, tok, grammar; free()
print("timing (s):", timing)""")

md("""## 7 · Format discipline and throughput per model

Reads the JSONL files back (so this cell works on an attached previous output too) and reports,
per model: records, valid, EOS-terminated, fully verbatim, duplicates removed, tokens and seconds
per preamble, claims per preamble, and the distributions of `operator`, `ground` and `frame` per
language. These are properties of the *emitters*, not measures of correctness. Two consistency
checks on the v2.0 rule "operator is decided from the ground": how often a model's operator
contradicts its own ground, per model.""")
code("""import glob, pandas as pd
from nra.schema import NATURALISING_GROUNDS
def rule_operator(ground):   # codebook v2.0 §3: the operator is decided from the ground
    return "naturalised" if ground in {g.value for g in NATURALISING_GROUNDS} else "revealed" if ground == "act" else "other"
rows = []
for path in sorted(glob.glob(f"{OUT_DIR}/*.jsonl")):
    if path.endswith(".offsets.jsonl") or "paraphrase" in path:
        continue   # paraphrase-B records carry the same annotator; they belong to §9 only
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            rows.append({"model": r["annotator"], "lang": r["lang"], "cid": r["constitution_id"], "sid": r["section_id"],
                         "length_band": r["run"]["length_band"], "parse_ok": r["parse_ok"], "verbatim_ok": bool(r["verbatim_ok"]),
                         "eos": r["run"]["stopped_by_eos"], "n_out": r["run"]["n_out"], "sec": r["run"]["sec"],
                         "n_dup": r["run"]["n_dup_removed"], "n_t2": len(r["output"]["t2"]), "n_t5": len(r["output"]["t5"]),
                         "n_nonverb": r["run"].get("n_nonverbatim", 0), "n_nonverb_norm": r["run"].get("n_nonverbatim_after_norm", 0),
                         "labels": [c["operator"] for c in r["output"]["t5"]] if r["parse_ok"] else [],
                         "grounds": [c["ground"] for c in r["output"]["t5"]] if r["parse_ok"] else [],
                         "frames": [c["frame"] for c in r["output"]["t5"]] if r["parse_ok"] else [],
                         "labels_fg": [rule_operator(c["ground"]) for c in r["output"]["t5"]] if r["parse_ok"] else [],
                         "claims": [(c["claim"], c["operator"], c["ground"], c["frame"], rule_operator(c["ground"])) for c in r["output"]["t5"]] if r["parse_ok"] else []})
df = pd.DataFrame(rows)
print(len(df), "records")
disc = df.groupby("model").agg(records=("cid", "size"), valid=("parse_ok", "mean"), eos=("eos", "mean"),
                               verbatim=("verbatim_ok", "mean"), nonverb_spans=("n_nonverb", "sum"), nonverb_after_norm=("n_nonverb_norm", "sum"), dup_per_sec=("n_dup", "mean"),
                               tok_mean=("n_out", "mean"), sec_mean=("sec", "mean"), sec_p90=("sec", lambda s: s.quantile(.9)),
                               t2_mean=("n_t2", "mean"), t5_mean=("n_t5", "mean")).round(2)
display(disc)
for col, title in (("labels", "operator"), ("labels_fg", "operator_from_ground"), ("grounds", "ground"), ("frames", "frame")):
    lab = df.explode(col).dropna(subset=[col]).groupby(["model", "lang", col]).size().unstack(fill_value=0)
    lab = lab.div(lab.sum(axis=1), axis=0).round(2)
    print(f"\\nT5 {title} shares per model and language (claim level):"); display(lab)
cons = {}
for m in sorted(df["model"].unique()):
    cl = [c for cs in df[df["model"] == m]["claims"] for c in cs]
    off = collections.Counter((g, op) for _, op, g, _, opg in cl if op != opg)
    cons[m.split("/")[-1]] = f"{sum(off.values())}/{len(cl)} claims where operator ≠ rule(ground); top {off.most_common(2)}"
print("\\nconsistency with the v2.0 rule (operator decided from ground):", cons)""")

md("""## 8 · Model–model agreement on operator, ground and frame (D18: three units, no synthetic labels)

Models segment claims differently, so there is no free alignment of units. Three measures, in
this order of authority: **(1) share of naturalised claims per section** — one number in [0, 1]
per emitter and section, Krippendorff's α at interval level; this is the magnitude the project
reports ("how much of this clause is presented as a fact of the world"); **(2) claim-level
agreement on aligned claims** — for each pair of emitters, claims of the same section are matched
greedily by character-offset overlap (Jaccard ≥ 0.5), and nominal α is computed on the matched
pairs; **(3) section dominant label with ties as missing** — kept only for comparison with the v1
figures. Measure (2) is computed for `operator`, `ground` (7 values) and `frame` (6 values)
separately. All are agreement between machines under one prompt: a diagnostic, not the reliability
of the task (that comes from the human campaign, D11 gates).""")
code("""import itertools, numpy as np, krippendorff
CATS = {"naturalised": 0, "revealed": 1, "other": 2}
GCATS = {g: i for i, g in enumerate(["nature", "history", "god", "spirit", "doctrine", "act", "none"])}
FCATS = {f: i for i, f in enumerate(["attitude", "will", "procedure", "invocation", "narrative", "none"])}

def alpha(mat, level):
    # krippendorff raises on a degenerate domain (one value, or fewer than two units); report n/a instead of dying
    try:
        return f"{krippendorff.alpha(reliability_data=mat, level_of_measurement=level):.3f}"
    except ValueError as e:
        return f"n/a ({str(e)[:40]})"

def share_nat(labels):
    return sum(l == "naturalised" for l in labels) / len(labels) if labels else np.nan

def dominant(labels):
    # ties → missing (v1 mapped ties to "other": a synthetic label no claim carried — abandoned, D18)
    if not labels:
        return None
    c = collections.Counter(labels).most_common()
    return c[0][0] if len(c) == 1 or c[0][1] > c[1][1] else None

df["share_nat"] = df["labels"].map(share_nat)
df["dom"] = df["labels"].map(dominant)
models = sorted(df["model"].unique())
short = lambda m: m.split("/")[-1]

# (1) primary: interval alpha on the share of naturalised claims
piv_s = df.pivot_table(index=["cid", "sid", "lang"], columns="model", values="share_nat", aggfunc="first")
mat = np.array([piv_s[m].to_numpy(dtype=float) for m in models])
print(f"(1) share of naturalised claims per preamble — interval alpha, {len(models)} emitters: {alpha(mat, 'interval')}")
for lang in ("en", "es"):
    sub = piv_s[piv_s.index.get_level_values('lang') == lang]
    m2 = np.array([sub[m].to_numpy(dtype=float) for m in models])
    print(f"    {lang}: {alpha(m2, 'interval')} on {len(sub)} preambles")

# (2) secondary: claim-level agreement on offset-aligned claims
text_of = {(s["constitution_id"], s["section_id"], s["lang"]): s["text"] for s in sections}
def spans(claims, text):
    out = []
    for c, op, g, fr, opg in claims:
        i = text.find(c)
        out.append(((i, i + len(c)) if i >= 0 else None, (op, g, fr, opg)))
    return out
def jaccard(a, b):
    if a is None or b is None:
        return 0.0
    inter = max(0, min(a[1], b[1]) - max(a[0], b[0])); union = (a[1] - a[0]) + (b[1] - b[0]) - inter
    return inter / union if union else 0.0
def align(ca, cb):
    pairs, used = [], set()
    for ia, (sa, oa) in enumerate(ca):
        best, bj = 0.5, None
        for ib, (sb, ob) in enumerate(cb):
            if ib in used:
                continue
            j = jaccard(sa, sb)
            if j >= best:
                best, bj = j, ib
        if bj is not None:
            used.add(bj); pairs.append((oa, cb[bj][1]))
    return pairs
claims_by = {(r.cid, r.sid, r.lang, r.model): r.claims for r in df.itertuples()}
print("(2) claim-level agreement on offset-aligned claims (Jaccard ≥ 0.5), pairwise:")
for a, b in itertools.combinations(models, 2):
    pairs = []
    for key, text in text_of.items():
        ca, cb = claims_by.get(key + (a,), []), claims_by.get(key + (b,), [])
        pairs += align(spans(ca, text), spans(cb, text))
    if not pairs:
        print(f"    {short(a)} vs {short(b)}: no aligned claims"); continue
    n_a = sum(len(v) for k, v in claims_by.items() if k[3] == a)
    line = f"    {short(a)} vs {short(b)}: {len(pairs)} aligned claims ({len(pairs)/max(n_a,1):.0%} of {short(a)}'s)"
    for name, cats, idx in (("operator", CATS, 0), ("ground", GCATS, 1), ("frame", FCATS, 2), ("operator_from_ground", CATS, 3)):
        m2 = np.array([[cats[x[idx]] for x, _ in pairs], [cats[y[idx]] for _, y in pairs]], dtype=float)
        agree = np.mean([x[idx] == y[idx] for x, y in pairs])
        line += f" | {name}: raw {agree:.2f} α {alpha(m2, 'nominal')}"
    print(line)

# (3) comparison with v1: section dominant label, ties as missing
piv = df.pivot_table(index=["cid", "sid", "lang"], columns="model", values="dom", aggfunc="first")
print("(3) section dominant label, ties → missing (v1 comparison only):")
print("    tied sections per model:", {short(m): int(((df["model"] == m) & df["dom"].isna() & (df["labels"].map(len) > 0)).sum()) for m in models})
for a, b in itertools.combinations(models, 2):
    both = piv[[a, b]].dropna()
    print(f"    {short(a)} vs {short(b)}: {(both[a] == both[b]).mean():.2f} on {len(both)} sections")
mat = np.array([[CATS.get(v, np.nan) if isinstance(v, str) else np.nan for v in piv[m]] for m in models], dtype=float)
print(f"    nominal alpha: {alpha(mat, 'nominal')}")

print("\\nmean share of naturalised claims by language × length band and model:")
display(df.pivot_table(index=["lang", "length_band"], columns="model", values="share_nat", aggfunc="mean").round(2))
print("\\nground shares by language × length band (all models pooled):")
g = df.explode("grounds").dropna(subset=["grounds"]).groupby(["lang", "length_band", "grounds"]).size().unstack(fill_value=0)
display(g.div(g.sum(axis=1), axis=0).round(2))""")

md("""## 9 · Prompt-paraphrase sensitivity (first model, first `SENSITIVITY_N` preambles)

The em runs showed that wording alone moves labels (p1 → p2: interval α 0.39 → 0.04). Here the
**rules stay identical** and only their wording changes (paraphrase B of three sentences); the
same model re-annotates the first `SENSITIVITY_N` preambles under B and we count how often the
share of naturalised claims and the dominant label move. A high flip rate means the label is
partly an artefact of phrasing — something the preregistration must state.""")
code("""_edits = [
    ("the act is made to rest on something presented as existing before and independently of any act",
     "the act is grounded in something put forward as already there, prior to and apart from any act"),
    ("the act rests on an inscribed act that anyone can ask about and check",
     "the act is grounded in another act that has been recorded and can be asked about and verified"),
    ("an attitude frame never changes the ground",
     "the frame of attitude leaves the ground exactly as it is"),
]
SYSTEM_B = SYSTEM
for _a, _b in _edits:
    assert _a in SYSTEM_B, _a[:40]
    SYSTEM_B = SYSTEM_B.replace(_a, _b)
assert SYSTEM_B != SYSTEM
PROMPT_VERSION_B = "q1b-" + hashlib.sha256(SYSTEM_B.encode()).hexdigest()[:8]
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
        return [{"role": "system", "content": SYSTEM_B}, {"role": "user", "content": "Preamble:\\n\\n" + text + "\\n\\nReturn the JSON object."}]
    _orig = messages_for
    messages_for = messages_b  # generate() reads the module-level name
    for sec in sections[:SENSITIVITY_N]:
        key = (sec["constitution_id"], sec["section_id"], sec["lang"])
        raw, n_in, n_out, dt, stopped = generate(tok, model, kind, sec["text"], grammar=grammar, max_new_tokens=MAX_NEW_TOKENS)
        obj, verdict = parse(raw, sec["text"])
        d = make_record(sec, model_id, obj, verdict, raw, n_in, n_out, dt, stopped); d["prompt_version"] = PROMPT_VERSION_B
        with open(f"{OUT_DIR}/{slug(model_id)}.paraphraseB.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(d, ensure_ascii=False) + "\\n")
        a = base.get(key)
        la = [c["operator"] for c in a["output"]["t5"]] if a and a["parse_ok"] else []
        lb = [c["operator"] for c in d["output"]["t5"]] if d["parse_ok"] else []
        dom_a, dom_b = dominant(la), dominant(lb)
        sens.append({"cid": key[0], "sid": key[1], "lang": key[2], "A": dom_a, "B": dom_b,
                     "same": (dom_a == dom_b) if (dom_a and dom_b) else np.nan, "nat_A": share_nat(la), "nat_B": share_nat(lb)})
        print(f"{key[2]} {key[0]}: A={dom_a} B={dom_b} | share naturalised {share_nat(la):.2f} → {share_nat(lb):.2f}")
    messages_for = _orig
    del model, tok, grammar; free()
    sdf = pd.DataFrame(sens)
    ab = np.array([sdf["nat_A"].to_numpy(dtype=float), sdf["nat_B"].to_numpy(dtype=float)])
    print(f"\\n{model_id}: dominant label unchanged under paraphrase B in {sdf['same'].mean():.2f} of {int(sdf['same'].notna().sum())} sections with a label in both; "
          f"interval alpha A vs B on share naturalised = {alpha(ab, 'interval')}")
else:
    print("sensitivity check skipped")""")

md("""## 10 · What this run establishes

Fill in after the run (numbers from §7–§9):

- Records: __ per model; valid __ / EOS __ / verbatim __; cap hits at 3072 tokens __; seconds per preamble (mean / p90): __.
- Operator, ground and frame shares per model and language: __. Consistency operator = rule(ground): __ violations per model (the grammar cannot enforce the rule; a violation is a reading error of the model).
- Agreement: interval α on share naturalised = __; claim-level aligned α per pair on operator / ground / frame = __; dominant label (ties missing) α = __. Language × length band where the emitters disagree most: __.
- Paraphrase sensitivity (model __, N = __): dominant label unchanged in __ %; interval α A vs B = __.
- Codebook v2.1 candidates surfaced by the disagreements (constitution ids): __.
- GPU hours used: __ of the 30-hour weekly quota.

Everything here is amendable output of the pipeline (Table 1). The JSONL files are machine-produced
*inscriptions* (weak documents, emitter = model, date = this run; an act between an instrument and
a person, *Manifiesto* p. 78); the `.offsets.jsonl` form is what can be published alongside the
hash-only manifest.""")

nb["cells"] = C
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["language_info"] = {"name": "python"}
out = Path(__file__).with_name("02b_stage1_preamble_bakeoff.ipynb")
nbf.write(nb, out)
print("wrote", out, len(C), "cells")

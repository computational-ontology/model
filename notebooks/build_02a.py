"""Builds notebooks/02a_stage1_load_check.ipynb. Run: python notebooks/build_02a.py"""

from pathlib import Path

import nbformat as nbf
from _shared_cells import ENV_CELL, LOADER_CELL, PROMPT_CELL, TOKEN_CELL

nb = nbf.v4.new_notebook()  # run from the repo root: python notebooks/build_02a.py
C: list = []
md, code = (lambda s: C.append(nbf.v4.new_markdown_cell(s))), (lambda s: C.append(nbf.v4.new_code_cell(s)))

md("""# 02a · Stage 1 load check — three candidates on 2×T4 (v2.2: constrained decoding, stop tokens)

Checks 2 and 3 of sprint 0 for the New-Realism Analyzer (github.com/computational-ontology/model).
Question: do the three bake-off candidates fixed in decision D15 load in fp16 across Kaggle's two
T4 GPUs and return one parseable `Stage1Output` JSON for one EN and one ES pilot section?

Nothing here is a result. No metric is computed; a single generation per model only tells us
whether the machinery works (memory, dtype, chat template, thinking switch, JSON discipline).

v1 (Version 1, 959 s) showed: all three load in fp16 without anomalies; two of six generations
were cut off at 900 tokens because the models pretty-print the JSON. v2 therefore decodes under
the JSON Schema with **XGrammar** (decision D16): the grammar forbids anything but a compact,
schema-valid object, so no fence, no indentation, no invented keys — and the budget goes to
content. Each model runs twice per section, free and constrained, so the two can be compared.

v2.1 (Version 3, 1652 s) ran end-to-end: 6/6 constrained outputs schema-valid vs 4/6 free. But Qwen3.5
never stopped under the grammar (both runs hit the 1600-token cap with the JSON already complete):
its `config.json` declares `<|endoftext|>` (248044) as EOS while the chat template ends turns with
`<|im_end|>` (248046) — the grammar allows only the tokenizer's EOS after the object closes,
`generate` waits for the config's. v2.2 passes the **union of all EOS ids** to both XGrammar and
`generate`, dedupes exact duplicate mentions in the harness, and records the decoding settings per row.

Settings: Accelerator **GPU T4 ×2**, Internet **on**, secret `HF_TOKEN` attached, dataset
`luisdscientist/nra-snapshot-em` attached.""")

md("""## 0 · Environment

Installs the current `transformers` (Gemma 4 and Qwen3.5 use `AutoModelForMultimodalLM`, which
older versions lack), `xgrammar` (the constrained decoder, Apache-2.0, the same backend vLLM
uses), the project package straight from GitHub so `nra.schema` is the code CI tests, and the
`flash-linear-attention` kernel Qwen3.5 warned about in v1 (`causal-conv1d` needs a CUDA build and is skipped). Then prints the GPUs. T4s have no native bf16, so everything below
is loaded in **float16**.""")
code(ENV_CELL)

md("""## 1 · Hugging Face token

Read from Kaggle Secrets, never typed here. None of the four candidate repos is gated
(`gated: false` on the HF API, checked 2026-09-14); the token only lifts anonymous download limits.""")
code(TOKEN_CELL)

md("""## 2 · Two pilot sections

The pilot draw (`data/splits/pilot_100.json`, seed 20260914) is fetched from the repository; the
texts come from the mounted snapshot. We take the first EN and the first ES section of the draw
and verify their SHA-256 against the manifest hash before using them — the record must be the
record.""")
code("""import requests, hashlib, unicodedata
ROOT = "/kaggle/input/datasets/luisdscientist/nra-snapshot-em"
RAW = "https://raw.githubusercontent.com/computational-ontology/model/main/"
pilot = requests.get(RAW + "data/splits/pilot_100.json", timeout=30).json()["sections"]

def fname(cid, sid, lang):
    return f"{cid}__{sid.replace('/', '_')}__{lang}.txt"

def sha256_text(text):
    return hashlib.sha256(unicodedata.normalize("NFC", text).strip().encode("utf-8")).hexdigest()

samples = []
for lang in ["en", "es"]:
    rec = next(r for r in pilot if r["lang"] == lang)
    text = open(f"{ROOT}/{fname(rec['constitution_id'], rec['section_id'], lang)}", encoding="utf-8").read()
    assert sha256_text(text) == rec["sha256"], "hash mismatch — snapshot and pilot disagree"
    samples.append({**rec, "text": text})
    print(f"[{lang}] {rec['constitution_id']} §{rec['section_id']} ({rec['chapter_type']}) — {len(text)} chars")
    print("   ", text[:200].replace("\\n", " "), "…")""")

md("""## 3 · The output schema and the prompt

`Stage1Output` is the only thing the model emits (T2 mentions, T5 claims, notes); ids, dates and
versions are added by the harness, never by the model. The system prompt is a compact rendering
of codebook v1.0 §2–§3 plus the JSON Schema. `PROMPT_VERSION` is the hash of that prompt so
every record can say which wording produced it.""")
code(PROMPT_CELL)

md("""## 4 · Loader and one-shot generator

Gemma 4 and Qwen3.5 are multimodal checkpoints (`AutoModelForMultimodalLM` + `AutoProcessor`)
with a thinking mode that is switched **off** through the chat template; EuroLLM is a plain
causal LM. All three load with `dtype=torch.float16, device_map="auto"`, which shards layers
across the two T4s. Decoding is greedy (`do_sample=False`) so the run is reproducible. `compile_grammar` turns the
schema into an XGrammar grammar for that model's tokenizer (compact JSON, strict); passing it as
a `LogitsProcessor` masks every token that would leave the grammar. A fresh processor is built
per call because it carries the matcher state. `eos_ids` collects every EOS id the model, its
text config and its tokenizer declare, and hands the union to both the grammar (`stop_token_ids`)
and `generate` (`eos_token_id`), so the turn can end whichever token the model prefers. The output
is parsed (any fence stripped, for the free run), exact duplicate mentions are removed harness-side
and counted, the object is validated against `Stage1Output`, and its spans are checked to be verbatim.""")
code(LOADER_CELL)

md("""## 5 · Run the three candidates

One model at a time: load, compile its grammar, then for each sample generate twice —
**constrained** (grammar on) and **free** (grammar off, the model merely asked for one-line JSON)
— print the raw answer and the verdict, then free both GPUs before the next. Expect roughly 24 GB (Gemma) / 19 GB (Qwen) /
18 GB (EuroLLM) of weights plus the KV cache. If a model overflows in fp16 (NaN logits, empty or
garbage output), that is exactly what this check is for — see §6.""")
code("""results = []
for model_id, kind in CANDIDATES:
    print("=" * 100); print(model_id)
    free()
    try:
        tok, model, grammar = load(model_id, kind)
    except Exception as e:  # noqa: BLE001
        print("LOAD FAILED:", type(e).__name__, str(e)[:300])
        results.append({"model": model_id, "loaded": False, "error": str(e)[:200]}); continue
    for s in samples:
        for mode, g in (("constrained", grammar), ("free", None)):
            try:
                raw, n_in, n_out, dt, stopped = generate(tok, model, kind, s["text"], grammar=g)
            except Exception as e:  # noqa: BLE001
                print(f"\\n[{s['lang']}] {mode}: GENERATION FAILED {type(e).__name__}: {str(e)[:300]}")
                results.append({"model": model_id, "loaded": True, "lang": s["lang"], "mode": mode, "error": str(e)[:200]}); continue
            obj, verdict = parse(raw, s["text"])
            print(f"\\n[{s['lang']}] {s['constitution_id']} §{s['section_id']} | {mode} | {n_in} in → {n_out} out | {dt:.0f}s | stopped by EOS: {stopped} | {verdict}")
            print(raw[:1200])
            results.append({"model": model_id, "loaded": True, "lang": s["lang"], "mode": mode, "in": n_in, "out": n_out,
                            "sec": round(dt, 1), "tok_s": round(n_out / dt, 1), "stopped_by_eos": stopped, "parsed": obj is not None,
                            "decoding": {"grammar": g is not None, "decoder": "xgrammar", "do_sample": False, "max_new_tokens": 1600, "prompt_version": PROMPT_VERSION},
                            "n_t2": len(obj.t2) if obj else None, "n_t5": len(obj.t5) if obj else None,
                            "labels": [c.operator.value for c in obj.t5] if obj else None,
                            "verdict": verdict, "mem": gpu_mem()})
    del model, tok, grammar; free()
    print("freed:", gpu_mem())""")

md("""## 6 · Summary table

One row per (model, sample, mode). `parsed` = valid `Stage1Output`; `verdict` = verbatim check;
`labels` = the T5 operators in order, so the constrained and free runs can be compared claim by claim.
Copy this table into the sprint log; it is the input to check 3 (which constrained decoder) and
to the bake-off protocol (D6).""")
code("""import pandas as pd
pd.set_option("display.max_colwidth", 80)
df = pd.DataFrame(results)
display(df)
print("prompt version:", PROMPT_VERSION)""")

md("""## 7 · What this notebook establishes

Fill in after the run:

- Loads in fp16 on 2×T4: Gemma-4-12B-it __ · Qwen3.5-9B __ · EuroLLM-9B __ (time, memory per GPU).
- Constrained runs: valid `Stage1Output` __/6, verbatim spans __/6, tokens saved vs. free __.
- Free runs (one-line instruction): valid __/6, verbatim __/6.
- Did the grammar change the labels vs. the free run on the same section? __ (if yes, note where).
- Qwen3.5 stopped by EOS under the grammar: __ (v2.1: no, both runs hit the cap).
- fp16 anomalies (NaN, empty, repeated tokens): __ → if any, rerun that model in 4-bit
  (`BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)`) and note it.
- Tokens per generation and seconds per section → budget for 100 sections × 3 models × 3 seeds
  against the 30 GPU-hours/week quota.

Everything above is amendable output of the pipeline (Table 1); the two sections it read are
identified by hash and were not modified.""")

nb["cells"] = C
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["language_info"] = {"name": "python"}
out = Path(__file__).with_name("02a_stage1_load_check.ipynb")
nbf.write(nb, out)
print("wrote", out, len(C), "cells")

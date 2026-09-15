# data/annotations/stage1/ — Stage 1 silver annotations (model emitters)

Output of `notebooks/02_stage1_llm_bakeoff.ipynb`, Kaggle `luisdscientist/02-stage1-llm-bakeoff` **Version 2** (15 Sep 2026, 13 152 s on 2×T4): the three D15 candidates annotate the 100-section pilot (`data/splits/pilot_100.json`) under one frozen prompt (`p1-e482d89f`), greedy decoding, XGrammar-constrained JSON (D16).

One `Stage1Record` per line (`nra.schema`), in the **releasable offsets form**: every `mention`, `claim` and marker is a `[start, end]` character offset into the section text identified by `constitution_id + section_id + lang + sha256` — never the text itself (Constitute texts are CC BY-NC 3.0, see `../../../NOTICE`). `null` = the span the model emitted is not a verbatim substring of the section (`run.verdict` lists these fragments). The span form and the paraphrase-B file (`gemma-4-12B-it.paraphraseB.jsonl`) are kept privately; `output.notes` is the model's free-text commentary.

| File | emitter (`annotator`) | records | valid | fully verbatim |
|---|---|---|---|---|
| `gemma-4-12B-it.offsets.jsonl` | google/gemma-4-12B-it | 100 | 100 | 90 |
| `Qwen3.5-9B.offsets.jsonl` | Qwen/Qwen3.5-9B (thinking off) | 100 | 100 | 75 |
| `EuroLLM-9B-Instruct-2512.offsets.jsonl` | utter-project/EuroLLM-9B-Instruct-2512 | 100 | 95 | 36 |

These are **weak documents** in the sense of the codebook (emitter = model, date = `emitted_at`, decoder and prompt version recorded): amendable outputs of the pipeline, not gold labels. Model–model agreement on the section-level dominant T5 label is low (Krippendorff α = 0.27 with the notebook's tie rule, 0.38 with ties treated as missing; 0.39 interval α on the per-section share of naturalised claims) — see `notebooks/analyze_02.py` and the sprint log. The human campaign (D11 gates) decides what the task's reliability is.

Reproduce the figures: `python notebooks/analyze_02.py` (reads this directory).

# data/annotations/stage1_p2/ — Stage 1 silver annotations, prompt p2

Output of `notebooks/02_stage1_llm_bakeoff.ipynb` **v2** (`build_02.py` @ `6ea4d3f`), Kaggle `luisdscientist/02-stage1-llm-bakeoff` **Version 3** (15 Sep 2026, 13 305 s on 2×T4): the same three emitters on the same 100-section pilot as `../stage1/`, under prompt **`p2-b3707801`** (decision D19: the example markers of p1 removed, markers declared quotations; `max_new_tokens=2048`). Same record format and release rule as `../stage1/README.md` (offsets form only; span form and paraphrase-B file private).

| File | emitter | records | valid | fully verbatim |
|---|---|---|---|---|
| `gemma-4-12B-it.offsets.jsonl` | google/gemma-4-12B-it | 100 | 100 | 91 |
| `Qwen3.5-9B.offsets.jsonl` | Qwen/Qwen3.5-9B | 100 | 100 | 80 |
| `EuroLLM-9B-Instruct-2512.offsets.jsonl` | utter-project/EuroLLM-9B-Instruct-2512 | 100 | 97 | 51 |

What changed against p1 (`python notebooks/analyze_02.py --dir data/annotations/stage1_p2`): no prompt-example marker is echoed any more (p1: 43 hallucinated by EuroLLM), but the label distributions moved — Gemma's and Qwen's share of *naturalised* claims fell (0.38 → 0.24, 0.28 → 0.11) while EuroLLM's rose (0.36 → 0.63; all claims naturalised in 54 of 97 sections). Gemma–Qwen agreement rose (section label 0.78 → 0.83; claim-level raw 0.82) and three-emitter agreement collapsed (interval α 0.39 → 0.04). Both runs are kept because the pair is itself the prompt-sensitivity result: the p1 examples were anchoring the *naturalised* category (open decision O8).

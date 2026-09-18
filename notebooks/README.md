# notebooks/

Kaggle / Colab notebooks. The `.ipynb` files here are **generated** from the `build_*.py` scripts
(`python notebooks/build_02.py` from the repo root) and imported into Kaggle as files; nothing is
typed into Kaggle cells by hand. Cells shared between notebooks (environment, token, the frozen
prompt, the loader/generator) live in `_shared_cells.py`, so the prompt stays byte-identical and
`PROMPT_VERSION` comparable across notebooks.

Rules (docs/plan.md §5b):
- notebooks read the **frozen snapshot** from a private Kaggle Dataset — never the Constitute API — and verify every text's SHA-256 against the manifest before use;
- tokens (Hugging Face, Zenodo) come from Kaggle Secrets / Colab `userdata`, never from the notebook text;
- outputs are `Stage1Record` JSONL (`nra.schema`); the `*.offsets.jsonl` form (spans replaced by character offsets) is the releasable one, the span form stays private (Constitute texts are CC BY-NC).

| Notebook | Kaggle | Purpose | State |
|---|---|---|---|
| `01_snapshot_check.ipynb` | `luisdscientist/01-snapshot-check` v2 | first read of the frozen corpus: mount path, manifests, per-constitution counts, lengths, chapter-type classifier | done (14 Sep 2026) |
| `01b_preamble_check.ipynb` (`build_01b.py`) | — | campaign 1 after D20: mount check of `nra-snapshot-preamble`, corpus filter (190 kept / 19 excluded), hash verification, length and paragraph profile, co-occurring topic keys, pilot check, first read of six preambles for codebook v2.0 | ready to run |
| `02a_stage1_load_check.ipynb` (`build_02a.py`) | `luisdscientist/02a-stage1-load-check` v4 = v2.2 | checks 2–3: the three D15 candidates load in fp16 on 2×T4; XGrammar-constrained JSON (D16) vs free; EOS union; dedupe | done (14 Sep 2026) |
| `02_stage1_llm_bakeoff.ipynb` v1 (`build_02.py` @ `a7e42f2`) | `luisdscientist/02-stage1-llm-bakeoff` v2 (full run, 13 152 s) | prompt `p1-e482d89f`, `max_new_tokens=1600`, section label with ties → other | done (15 Sep 2026) — outputs in `data/annotations/stage1/` (offsets form) |
| `02_stage1_llm_bakeoff.ipynb` **v2** (`build_02.py`) | — | prompt **`p2-b3707801`** (example markers removed, markers = quotations; D19), `max_new_tokens=2048`, agreement per D18 (interval α on share naturalised; claim-level α on offset-aligned claims; section label only with ties missing), normalised second pass on non-verbatim spans; writes to `stage1_p2/` | done (15 Sep 2026, Kaggle v3, 13 305 s) — outputs in `data/annotations/stage1_p2/` |
| `02b_stage1_preamble_bakeoff.ipynb` (`build_02b.py`) | `02b-stage1-preamble-bakeoff` | campaign 1 bake-off on the 100-preamble pilot (`pilot_preamble_100.json`), codebook v2.0, prompt `q1-f2f23d89` (`PROMPT_CELL_Q1`: T5 = ground + frame + operator, no quotable markers), grammar from schema v2.0, `max_new_tokens=3072` (v1) → 8192 (v1.1); §5b resumes from an attached previous output and, with `RETRY_FAILED`, regenerates only the `parse_ok=false` records; §7 adds ground/frame shares, `operator_from_ground` and the operator = rule(ground) consistency check; §8 α on operator, ground, frame and operator_from_ground on aligned claims; §9 paraphrase `q1b-`; writes to `stage1_preamble/` | v1: Version 2 (Gemma, 18 213 s) + Version 3 (Qwen), 16 Sep 2026; v1.1: Version 4 (Qwen) + Version 5 (Gemma) retries, 16 Sep; **Version 6 (EuroLLM, single run at 8192, 39 885 s, 17 Sep): 90/100 valid, ten degenerate loops** — all in `data/annotations/stage1_preamble/` (commits `126d7ab`, `29858b5`, `382f281`) |
| `analyze_02.py` (script, no Kaggle) | — | recomputes §7–§8 from `data/annotations/stage1*/` (`--dir`; tolerates a missing model); `--private DIR` adds the checks that need the span form (marker echo, paraphrase B) | done |
| `align_claims.py` (script, no Kaggle) | — | claim-level agreement on the offsets form: greedy span alignment (IoU ≥ `--iou`, default 0.5), Krippendorff α on operator, ground, frame and `operator_from_ground`, per language and per length band; per-model operator = rule(ground) check; confusion table | done (16 Sep 2026; bands + operator_from_ground 18 Sep) |

02 v1 resolved section-level ties to `other` (20 % of Gemma's sections); v2 and `analyze_02.py` follow D18 instead (interval α on the share of naturalised claims as primary measure, ties as missing). The p1 prompt cell stays in `_shared_cells.py` unchanged (02a and the v1 records depend on it); p2 is derived from it by three asserted edits.

`02b` is derived from `build_02.py` (frozen for the em runs) with asserted replacements; `analyze_02.py` reads both em (`chapter_type`) and preamble (`length_band`) records and prints ground/frame shares for v2.0 records.

Optional, not scheduled: a `02b` v1.2 with a loop guard (`repetition_penalty` or an n-gram repetition detector) to recover the ten EuroLLM preambles that looped under the grammar; not needed for campaign 1 (gold labels are human, D11; EuroLLM's silver is reported as a finding, D25).

Planned: `03_finetune_T2.ipynb`, `04_finetune_T5.ipynb`, `05_evaluate_vs_gold.ipynb` (after the annotation campaign).

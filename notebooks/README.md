# notebooks/

Kaggle / Colab notebooks, exported here after each run (the notebook is part of the record).

Rules (docs/plan.md §5b):
- notebooks read the **frozen snapshot** from a private Kaggle Dataset / Drive folder — never the Constitute API;
- tokens (Hugging Face, Zenodo) come from Kaggle Secrets / Colab `userdata`, never from the notebook text;
- every experiment appends one row to `runs.csv` (task, model, seed, split hash, macro-F1 per language, date);
- checkpoints every N steps so a fold finishes inside one session.

Planned: `00_snapshot_check.ipynb`, `01_stage1_llm_bakeoff.ipynb`, `02_finetune_T2.ipynb`, `03_finetune_T5.ipynb`, `04_evaluate_vs_gold.ipynb`.

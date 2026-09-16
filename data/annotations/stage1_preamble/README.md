# data/annotations/stage1_preamble/ — Stage 1 silver annotations, preamble pilot, codebook v2.0

Output of `notebooks/02b_stage1_preamble_bakeoff.ipynb` v1 (`build_02b.py` @ `9b3e8d1`), Kaggle
`luisdscientist/02b-stage1-preamble-bakeoff` **Version 2** (Gemma, 16 Sep 2026, 18 213 s on 2xT4) and
**Version 3** (Qwen, 16 Sep 2026): the 100-preamble pilot (`data/splits/pilot_preamble_100.json`, 78 EN + 22 ES)
under prompt **`q1-f2f23d89`** (codebook v2.0: fields `ground` and `frame`, decisions D22-D23; grammar-constrained
decoding, `max_new_tokens=3072`). Same record format and release rule as `../stage1/README.md`: offsets form only;
the span form and the paraphrase-B file (`q1b-56f00c68`, Gemma, 20 EN preambles) stay in `data/private/` (never
committed). EuroLLM is pending the weekly GPU quota.

| File | emitter | records | valid | fully verbatim | failed at the 3072-token cap |
|---|---|---|---|---|---|
| `gemma-4-12B-it.offsets.jsonl` | google/gemma-4-12B-it | 100 | 96 | 86 | Cameroon_2008, Peoples_Republic_of_Korea_2016, Algeria_2020, China_2004 (es) |
| `Qwen3.5-9B.offsets.jsonl` | Qwen/Qwen3.5-9B | 100 | 94 | 74 | the same four + Hungary_2016, Cuba_2019 (es) |

First reading (`python notebooks/analyze_02.py --dir data/annotations/stage1_preamble` and
`python notebooks/align_claims.py`; all of it amendable, Table 1):

- Claim level, 717 claims aligned by span (IoU >= 0.5; 68 % of Gemma's 1 103, 92 % of Qwen's 780): Krippendorff
  nominal alpha **operator 0.46** (EN 0.42, ES 0.62), **ground 0.49**, **frame 0.53**; raw agreement 0.61-0.65.
- Section level (dominant label, ties -> missing): alpha 0.06. The gap to the claim level is segmentation: Gemma
  cuts 11.7 claims per preamble, Qwen 8.7, and half of Gemma's claims carry `ground=none` (Qwen: 0.27), so the
  dominant label of a preamble is decided by how many "other" clauses each model chooses to cut.
- The single largest disagreement is Gemma `other` vs Qwen `naturalised` (151 of 717 aligned claims): the
  boundary between an attitude frame without a ground and a clause that rests on spirit/history. This is the
  boundary the human campaign must adjudicate first (D11, O10).
- Rule check `operator = rule(ground)` (codebook v2.0 section 3): Gemma 0.98, Qwen 0.93; almost every violation is
  `ground=act` with `operator=naturalised` (23 and 50). The grammar constrains each field, not their joint rule;
  the analysis should report `operator_from_ground` alongside the emitted operator.
- Format discipline: Gemma leaves `markers` empty in 242 of 1 121 claims; Qwen never, but 284 duplicate T2
  mentions were removed and its `secondary` field is used freely (aggregation 78, naturalisation 89, revelation 53).
- Paraphrase sensitivity (Gemma, 20 EN preambles): dominant label unchanged in 10 of 12 defined cases; interval
  alpha on the share of naturalised claims A vs B = 0.60; three preambles swing by > 0.2 (Russia_2014,
  Kazakhstan_2026, Equatorial_Guinea_2012).
- No prompt-example marker is echoed by either model (D19 discipline holds under q1).

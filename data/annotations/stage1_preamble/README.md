# data/annotations/stage1_preamble/ — Stage 1 silver annotations, preamble pilot, codebook v2.0

Output of `notebooks/02b_stage1_preamble_bakeoff.ipynb`, Kaggle `luisdscientist/02b-stage1-preamble-bakeoff`:
**v1** (`build_02b.py` @ `9b3e8d1`; Version 2 Gemma, 18 213 s on 2xT4; Version 3 Qwen; 16 Sep 2026) under
prompt **`q1-f2f23d89`** (codebook v2.0: fields `ground` and `frame`, decisions D22-D23; grammar-constrained decoding,
`max_new_tokens=3072`), completed by **v1.1** (`build_02b.py` @ `f1e8352`; Version 4 Qwen 3 090 s, Version 5 Gemma;
16 Sep 2026), which re-generated only the `parse_ok=false` records of v1 (the preambles that hit the 3 072-token
cap) under `max_new_tokens=8192`, seeded from the v1 output (Version 3 attached as input for Qwen; the private
Kaggle dataset `nra-02b-v1-gemma`, created from the Version 2 output, for Gemma). Each record carries its own
`decoding.max_new_tokens` and `emitted_at`, so the two attempts are distinguishable. The 100-preamble pilot is
`data/splits/pilot_preamble_100.json` (78 EN + 22 ES). Same record format and release rule as `../stage1/README.md`:
offsets form only; the span form and the paraphrase-B file (`q1b-56f00c68`, Gemma, 20 EN preambles) stay in
`data/private/` (never committed). **EuroLLM** ran as **v1.1 Version 6** (no previous output, `ONLY_MODEL` EuroLLM,
`max_new_tokens=8192`; 39 885 s on 2xT4, 17 Sep 2026): 100 records, 90 valid; the 10 failures are degenerate loops
under the grammar (8 192 tokens, no EOS, ~1 900-2 260 s each), not cap hits on long inputs — six of the ten are
`medium` or `short` preambles.

| File | emitter | records | valid | fully verbatim | re-generated in v1.1 (8192 tokens) |
|---|---|---|---|---|---|
| `gemma-4-12B-it.offsets.jsonl` | google/gemma-4-12B-it | 100 | 100 | 88 | Cameroon_2008, Peoples_Republic_of_Korea_2016, Algeria_2020, China_2004 (es) |
| `Qwen3.5-9B.offsets.jsonl` | Qwen/Qwen3.5-9B | 100 | 100 | 74 | the same four + Hungary_2016, Cuba_2019 (es) |
| `EuroLLM-9B-Instruct-2512.offsets.jsonl` | utter-project/EuroLLM-9B-Instruct-2512 | 100 | 90 | 36 | single run at 8192 (Version 6); loops: Papua_New_Guinea_2016, South_Sudan_2013, Socialist_Republic_of_Vietnam_2013, Hungary_2016, Cameroon_2008, Algeria_2020, Serbia_2006, Russia_2014 (es), Poland_2009 (es), Philippines_1987 (es) |

Reading on the complete pilot (`python notebooks/analyze_02.py --dir data/annotations/stage1_preamble` and
`python notebooks/align_claims.py`; all of it amendable, Table 1):

- Claim level, 847 claims aligned by span (IoU >= 0.5; 64 % of Gemma's 1 319 located claims, 92 % of Qwen's 920):
  Krippendorff nominal alpha **operator 0.47** (EN 0.41, ES 0.68; short 0.63, medium 0.50, long 0.39),
  **ground 0.47**, **frame 0.53**, operator_from_ground 0.46; raw agreement 0.60-0.66. Agreement falls with
  length: the long preambles are where the two emitters read the same clauses most differently.
- Section level (dominant label, ties -> missing): alpha 0.08; interval alpha on the share of naturalised claims
  0.09 (EN 0.00, ES 0.54). The gap to the claim level is segmentation: Gemma cuts 13.4 claims per preamble,
  Qwen 10.0, and half of Gemma's claims carry `ground=none` (Qwen 0.26).
- The single largest disagreement is Gemma `other` vs Qwen `naturalised` (175 of 847 aligned claims): the
  boundary between an attitude frame without a ground and a clause that rests on spirit/history. This is the
  boundary the human campaign must adjudicate first (D11, O10).
- Rule check `operator = rule(ground)` (codebook v2.0 section 3): Gemma 0.97, Qwen 0.91; almost every violation is
  `ground=act` with `operator=naturalised` (36 and 80). The grammar constrains each field, not their joint rule.
- Format discipline: Gemma leaves `markers` empty in 274 of 1 337 claims; Qwen never, but 425 duplicate T2 mentions
  were removed and its `secondary` field is used freely (aggregation 116, naturalisation 106, revelation 56).
  On the long preambles Qwen quotes non-verbatim (5-29 unlocatable spans per preamble in the six re-generated
  ones; 76 claims without a located span in total vs 18 for Gemma).
- Paraphrase sensitivity (Gemma, 20 EN preambles): dominant label unchanged in 10 of 12 defined cases; interval
  alpha on the share of naturalised claims A vs B = 0.60; swings > 0.2 in Russia_2014, Kazakhstan_2026,
  Equatorial_Guinea_2012.
- No prompt-example marker is echoed by either model (D19 discipline holds under q1).

EuroLLM added (three emitters; same scripts, 17 Sep 2026):

- Claim level: EuroLLM agrees with neither of the other two — operator alpha **0.12** vs Gemma (521 aligned
  claims) and **0.17** vs Qwen (524); ground 0.16 / 0.15, frame 0.17 / 0.09; raw agreement about 0.50. The
  Gemma-Qwen pair is unchanged (0.47).
- Section level, three emitters: dominant label (ties -> missing) alpha 0.09; interval alpha on the share of
  naturalised claims **0.09** (EN 0.08, ES 0.15); 19 of 100 preambles unanimous (12 `other`, 7 `naturalised`).
- Rule check `operator = rule(ground)`: EuroLLM **0.79** (134 of 645 claims violate it; `act`->naturalised 46,
  `none`->revealed 30, `none`->naturalised 23), against 0.97 and 0.91. Its emitted operator and the operator
  derived from its ground are different readings; the derived one is the one comparable across emitters.
- Reading profile: 7.2 claims per preamble; `ground=none` 0.68 and `frame=none` 0.67 (whole preambles read as
  `other`: China_2004 es 41 claims, Burundi_2018 17, Nicaragua_2014 14-15); the six-operator `secondary` field is
  filled almost always (implication 390 of 645). Only 36 of 90 valid records are fully verbatim (Bolivia_2009 es 36
  non-verbatim spans, Angola_2010 25); 52 claims without a located span. T2: 2 353 mentions, physical only 53.
- Cost: the ten loops took about 5.5 of the 11 GPU-hours. A v1.2 with a loop guard (`repetition_penalty` or an
  n-gram detector) would be needed to complete the ten; it is not required for campaign 1, where the gold
  labels are human (D11) and EuroLLM's silver is reported as a finding, not used as a candidate.

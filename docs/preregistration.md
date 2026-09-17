# Preregistration — Can naturalisation be annotated? Inter-annotator reliability of New-Realist operators in constitutional preambles (campaign 1)

Template: **OSF Preregistration** (standard). Draft v0.3, 17 Sep 2026 (EuroLLM frozen at commit `382f281`), to be pasted section by section into
the OSF form and sealed **before** any human annotation starts. Canonical language: English (D10). Every
artefact named here is frozen and citable at the moment of sealing.

---

## Study Information

### Title

Can naturalisation be annotated? Inter-annotator reliability of New-Realist operators (naturalisation ↓,
revelation ✦) and ontological entity types in the preambles of in-force constitutions — campaign 1 of the
New-Realism Analyzer.

### Authors

Luis Felipe Bourguet González (LabOnt – Center for Ontology, University of Turin; Complex Systems Science
Laboratory, Hiroshima University) and Jimmy Hernández Marcelo (author of the introductory study that anchors the
project's frame: «La filosofía de la tecnología desde el Nuevo realismo», in M. Ferraris, *Metafísica de la Web*,
Dykinson, 2020). The two authors are the two annotators. Adjudication: see *Study design*.

### Description

The New-Realism Analyzer (github.com/computational-ontology/model; concept DOI 10.5281/zenodo.22748194) is a
semantic-NLP pipeline built on Maurizio Ferraris's New Realism (documentality: *Object = Inscribed Act*;
unamendable record vs amendable model). Its central operational claim is that the *naturalisation* of a social
object — the presentation of an inscribed act as if it were an unamendable fact of the world — is a property of
inscriptions that trained readers can identify reliably. Campaign 1 tests that claim on the object where a
constitution naturalises itself most visibly: its **preamble**, read as a founding inscription.

Two annotation tasks are studied. **T2 — ontological typing of entities** (physical / ideal / social, Ferraris's
three-way ontology). **T5 — ground, frame and operator of each claim**: what the clause makes the founding act
rest on (`ground` ∈ {nature, history, god, spirit, doctrine, act, none}), how the enunciator relates the clause to
itself (`frame` ∈ {attitude, will, procedure, invocation, narrative, none}), and the operator decided from the
ground (`naturalised` ↓ for nature/history/god/spirit/doctrine, `revealed` ✦ for act, `other` for none).
Codebook v2.0 defines both tasks (Zenodo DOI **10.5281/zenodo.22784017**, release `v2.0.0`, 16 Sep 2026).

The study has two parts: (A) an inter-annotator reliability study on a stratified pilot of 100 preambles, with a
preregistered agreement gate; (B) a computational evaluation comparing three open-weights language models —
whose annotations of the same 100 preambles already exist (see *Existing data*) — against the adjudicated human
gold. Part (C), the extension to the whole population of 190 preambles, is conditional on the gate.

### Hypotheses

Confirmatory (H1–H6); exploratory (E1–E3). α is Krippendorff's alpha; "claim level" means the unit fixed by the
adjudicated segmentation (see *Analysis plan*).

- **H1 (task order).** α(T2 entity type, nominal, 3 classes) > α(T5 operator, nominal, 3 classes). T2 follows an
  explicit ontology; T5 requires a judgement about how a clause grounds an act.
- **H2 (gate).** α(T5 operator) ≥ 0.67 on the pilot. We do not predict ≥ 0.80.
- **H3 (coarsening).** α(T5 ground, 7 classes) ≤ α(T5 operator, 3 classes), because the operator is a
  deterministic coarsening of the ground (codebook v2.0 §3).
- **H4 (models vs humans).** For each of the three emitters, agreement with the adjudicated gold is lower on T5
  operator than on T2, and **no emitter reaches α ≥ 0.67 against gold on T5 operator**. This prediction is derived
  from the model–model agreement already observed (α 0.47 on 847 aligned claims, commit `29858b5`); it is
  registered here as a falsifiable claim about model–human agreement, which has not been measured.
- **H5 (language, non-inferiority).** α(T5 operator) on the Spanish preambles is not lower than on the English
  preambles by more than 0.10. (Model–model agreement was higher in Spanish, 0.68 vs 0.41; we register only the
  weaker, non-inferiority form for humans.)
- **H6 (length).** α(T5 operator) decreases monotonically across length bands: short > medium > long. Derived
  from the model–model result (0.63 / 0.50 / 0.39); registered as a directional prediction for humans.
- **E1 (the boundary).** Among adjudicated T5 disagreements, the single most frequent class will be
  *attitude frame without ground* (`other`) vs *spirit/history as ground* (`naturalised`). Exploratory: it
  characterises where the codebook is thinnest.
- **E2 (grounds across traditions).** The distribution of `ground` values differs across regions and
  constitutional traditions (e.g. `history` and `spirit` denser in post-revolutionary and post-colonial
  preambles; `act` and `none` denser in procedural preambles). Exploratory; no test is fixed.
- **E3 (the six-operator set).** The exploratory secondary label (⇒ ⊕ ↓ ∅ ✦ ∥) is recorded and its agreement
  reported without a gate.

---

## Design Plan

### Study type

Observational annotation study (inter-annotator reliability) with a computational evaluation of pre-existing
model outputs. No experimental manipulation.

### Blinding

Annotators are blind to each other's labels and to the language-model outputs throughout annotation. The
annotators, during adjudication, see each other's labels but not the model outputs. Model outputs are frozen
(git commit, hash) before annotation starts and are compared with gold only after adjudication is complete.

### Is there any additional blinding in this study?

No.

### Study design

Each of the 100 pilot preambles is annotated independently by the two annotators under codebook v2.0. All
reliability indices (H1–H6) are computed on the **independent** labels, before adjudication, so adjudication
cannot inflate them. Disagreements are then adjudicated jointly by the two annotators in a recorded session: for
each disagreement the resolving codebook rule (or a new rule, dated) is written down; where no rule decides, the
claim is marked *unresolved* and excluded from the gold (counted and reported). The adjudicated set is the gold
used for the model comparison (H4). No third person is involved; this is declared as a limitation. Annotation is at claim level inside the
preamble (the preamble is one inscribed act, thesis 5; claims are its clauses). Segmentation into claims is part
of the task: annotators mark claim spans; the adjudicated segmentation becomes the gold unit. Three language
models (see *Existing data*) have annotated the same preambles once each under the same codebook, a fixed prompt
(`q1-f2f23d89`) and grammar-constrained decoding.

### Randomization

None (no assignment). The pilot itself was drawn by stratified random sampling (seed 20260916; see *Sampling
plan*). The order of preambles is shuffled per annotator with a recorded seed to avoid order effects.

---

## Sampling Plan

### Existing data

**Registration prior to analysis of the data.** The texts exist and are frozen; the human annotations do not exist.
Model annotations of the pilot exist and *have* been analysed for model–model agreement (not against any human
label); that analysis is disclosed here and its results were used to formulate H4–H6 and E1.

### Explanation of existing data

- **Corpus.** Preambles of in-force constitutions, English and Spanish, fetched from the Constitute Project
  (topic key `preamble`; snapshot dump date 2026-09-16; parser and filter `nra.preamble.is_preamble`, repository
  commit `fa63b02`): 209 sections fetched, **190 preambles kept** (EN 150, ES 40; 37 EN/ES translation pairs),
  19 excluded by rule (statute preambles in compilations, schedules). Every text is identified by
  `(constitution_id, section_id, lang)` and a SHA-256 hash recorded in hash-only manifests
  (`data/snapshot_manifest_preamble_{en,es}.json`); the texts themselves are CC BY-NC 3.0 (Constitute) and are
  not redistributed — they are held in a versioned, write-once object store (S3 Object Lock, compliance mode,
  365 days; decision D24) and verified against the manifests before every run.
- **Pilot.** `data/splits/pilot_preamble_100.json`: 100 preambles drawn from the 190 with seed 20260916,
  stratified by language × length band (short < 600 < medium < 2 000 < long characters): EN 14/42/22,
  ES 5/12/5; 9 translation pairs.
- **Model annotations (silver).** Three open-weights emitters (decision D15), each annotating the 100 pilot
  preambles once under codebook v2.0, prompt `q1-f2f23d89`, XGrammar-constrained JSON, greedy decoding:
  `google/gemma-4-12B-it`, `Qwen/Qwen3.5-9B` (thinking off) — complete, 100/100 valid, released as offsets
  (`data/annotations/stage1_preamble/`, commit `29858b5`) — and `utter-project/EuroLLM-9B-Instruct-2512`
  (Kaggle Version 6, 90/100 valid: ten records failed by degenerate looping under the grammar and are absent;
  released as offsets in commit `382f281`, which freezes all model annotations). Model–model results seen
  before sealing: Gemma–Qwen claim-level α operator 0.47 (EN 0.41, ES 0.68; short 0.63, medium 0.50, long 0.39),
  ground 0.47, frame 0.53; EuroLLM α operator 0.12 vs Gemma and 0.17 vs Qwen; three-emitter section-level
  interval α 0.09; largest confusion `other` vs `naturalised`; details in the README of that directory.
- **Earlier exploratory work.** Two full runs of the same emitters on 100 *emergency-provision* sections
  (codebook v1.0, prompts p1 and p2) are published as an exploratory prompt-sensitivity study
  (`data/annotations/stage1/`, `stage1_p2/`; decisions D19–D20). No human annotation was done on them; they
  are not part of this registration's tests.

### Data collection procedures

Human annotation is collected in a spreadsheet/JSON form keyed to `(constitution_id, section_id, lang)` and
character offsets, never to redistributed text; annotators read the texts from the verified snapshot. Training:
one session on codebook v2.0 §§1–5 and its worked examples (Taiwan, Madagascar, Azerbaijan, Ireland, South
Africa, India, Greece; Costa Rica, Spain, Bolivia, China), then a calibration set of 6 preambles outside the pilot
(`data/splits/calibration_preamble_6.json`, seed 20260917, stratified as the pilot: Palau_1992, Zimbabwe_2021,
Uzbekistan_2023, East_Timor_2002 in English; Equatorial_Guinea_2012, Iran_1989 in Spanish), discussed jointly;
calibration items are not scored and are excluded from Part C's reliability estimates. There is no payment or contract of any kind for annotation; the annotators are the two authors, their
participation is stated in every publication of the campaign, and co-authorship of the resulting paper is
foreseen.

### Sample size

Part A: **100 preambles** (fixed by the pilot draw). Part B: the same 100. Part C (conditional): the remaining 90
of the 190, so that the population is complete.

### Sample size rationale

The pilot is the smallest stratified draw that keeps ≥ 5 items in every language × length stratum and includes
translation pairs; with two annotators and ~10–13 claims per preamble it yields roughly 1 000–1 300 claim
units per annotator, sufficient for bootstrap confidence intervals on α of width ≈ ±0.05 at the values expected.
Part C is the complete population, which removes sampling error from the population estimates.

### Stopping rule

Part A stops when all 100 preambles are doubly annotated and adjudicated. No interim analysis of α is used to
stop, extend or re-draw the pilot. Part C starts only if H2 holds (α(T5 operator) ≥ 0.67) and stops at 190.

---

## Variables

### Manipulated variables

None.

### Measured variables

Per claim: span (character offsets), `operator` (3), `ground` (7), `frame` (6), `markers` (quoted spans),
exploratory `secondary` (6 operators or null); per mention: `type` (physical / ideal / social); per preamble:
language, length band, constitution id, region and constitutional tradition (from the Constitute metadata and
the Comparative Constitutions Project where available), translation-pair id, annotator ids, adjudication rule
id per disagreement. Per model annotation: the same fields plus emitter, prompt version, decoding settings and
timestamp (`Stage1Record`, schema v2.0).

### Indices

Krippendorff's α (nominal for operator/ground/frame/type; interval for the share of naturalised claims per
preamble), computed with the `krippendorff` package; raw agreement; per-emitter α against gold; macro-F1
against gold per task and language; bootstrap 95 % confidence intervals (1 000 resamples over preambles).

---

## Analysis Plan

### Statistical models

Reliability is estimated with Krippendorff's α, three units in a fixed order of authority (decision D18):
(1) **primary** — the share of naturalised claims per preamble, one number per annotator and preamble, α at
interval level; (2) **secondary** — claim-level nominal α on `operator`, `ground`, `frame` and `type` over the
adjudicated segmentation (for the two humans: claims aligned to the gold spans by character-offset overlap,
Jaccard ≥ 0.5; for the models: their claims aligned to gold the same way; unaligned claims are missing, and
their rate is reported); (3) a preamble-level dominant label, ties treated as missing, reported for comparison
only. **"Ties → other" is not used** (D18). H1, H3, H5, H6 are tested by comparing α values with bootstrap CIs;
H2 by the point estimate against 0.67 with its CI; H4 per emitter by paired comparison of α(model, gold) across
tasks and against 0.67. E1 is a frequency count over adjudication rule ids; E2 a descriptive cross-tabulation.

### Transformations

Operator is derived from ground by the codebook rule and is also recorded as emitted; both are reported, and
`operator_from_ground` is the value used for H2–H6 when the two differ (the emitted operator is a consistency
check, reported separately). Length bands as defined in the pilot file.

### Inference criteria

Two-sided 95 % bootstrap CIs; a hypothesis stated as an inequality is supported when the CI of the difference
excludes zero in the predicted direction (H1, H3, H6) or, for non-inferiority (H5), when the CI of the difference
lies above −0.10. H2 is supported when the point estimate is ≥ 0.67 and the lower CI bound is ≥ 0.60 (reported
as "gate passed"); the D11 gate itself uses the point estimate.

### Data exclusion

No preamble is excluded. A claim is excluded from a task only when adjudication marks it as not annotatable
under codebook v2.0 (recorded with a rule id); such claims are counted and reported.

### Missing data

A claim not aligned to any gold span is missing for the claim-level indices; the primary interval index has no
missing values by construction. Annotator drop-out before completion: the remaining annotator's labels are kept,
the missing annotator is replaced, and the replacement's calibration is reported.

### Exploratory analysis

E1–E3 above; prompt-paraphrase sensitivity of the models (paraphrase B, 20 preambles) already in the repository;
per-region and per-tradition profiles of `ground`; the relation between `frame` and `ground`; the effect of
translation (EN/ES pairs) on human labels.

---

## Other

- **Frozen materials at sealing.** Codebook v2.0 (DOI 10.5281/zenodo.22784017); prompt `q1-f2f23d89` and
  paraphrase `q1b-56f00c68` (`notebooks/_shared_cells.py`); schema v2.0; pilot draw; hash manifests; model
  annotations (commit `382f281`); notebooks 02b v1/v1.1 and their Kaggle version ids
  (2, 3, 4, 5, 6); analysis scripts `analyze_02.py`, `align_claims.py`.
- **What this study is not.** Three emitters agreeing under one prompt is solidarity among emitters, not
  objectivity (Ferraris, *Manifiesto*, pp. 97–99); model outputs are inscriptions (emitter = model, date =
  run) and are treated as such. The reliability claim of this study rests on the human annotation only.
- **Limitation declared.** With two annotators who are also the authors, adjudication is by the same two
  people; the design protects the reliability estimate (computed before adjudication) but not the independence of
  the gold from the authors' reading. A third, independent annotator on a subset is planned for campaign 2.
- **Amendments.** Any change after sealing is recorded as an OSF update with the reason; rules born in
  adjudication go into codebook v2.1 (dated) and do not alter the v2.0 labels already given.
- **Open decisions declared.** O9 (paragraph-level pre-segmentation for long preambles) is not adopted in
  campaign 1; O10 (adding `auth`/`motive` sections for constitutions without a formal preamble) is deferred to
  campaign 2; O3 (T1 inscribed-act slots) is not part of this registration.

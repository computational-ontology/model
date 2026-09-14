# PLAN_MODELO — New-Realism Analyzer: model plan, timeline and preregistration skeleton (v0.1, 2026-09-14)

Companion to `claude/INSTRUCCIONES_PROYECTO.md` (axioms, tables, vocabulary). Diagram: artifact "New-Realism Analyzer Blueprint". Language of this doc: English (the working language of the code, model cards and OSF record); the codebook will be trilingual.

---

## 1. What is being built

A website (working name **new-realism**) with a structured analyzer: a user pastes a text and receives a card per stratum (E1 Record · E2 Enunciation · E3 Mediation), a JSON-LD export against the project ontology, and an optional chat explanation grounded in the card. Behind it, a pipeline in which most components are rules and three are learned models. Everything is published Gold Route: GitHub (code, codebook, ontology), OSF (preregistration), Zenodo (DOIs for codebook, dataset, evaluation set, model weights mirror), Hugging Face Hub (models and dataset cards).

## 2. Tasks: what is learned, what is a rule

| ID | Task | Stratum | Type | Learned? | Output label set | Data source |
|---|---|---|---|---|---|---|
| T0 | Freeze input (hash, date, source), provenance tags, reflexive log | E1/E3 | metadata | No — rule | emendable / in-emendable | — |
| T1 | Segment text into inscribed acts (who · act · support · date) | E1 | structured extraction | Stage 1 LLM → Stage 3 sequence labelling | act spans + 4 slots | own annotation |
| T2 | Ontological entity typing | E1 | span classification | Yes | physical · ideal · social (+ 3 coordinates) | NER spans + own type annotation |
| T3 | Strong vs. weak document | E1 | segment classification | Yes (+ genre rule) | strong (act) · weak (record) | silver from genre; gold subset |
| T4 | Claim / frame / stance per social object | E2 | extraction + classification | Stage 1 LLM → distilled encoder | claim span, frame, stance {for, against, neutral} | bootstrap from public claim datasets; own gold |
| **T5** | **Operator on each claim** | E2 | classification | **Yes — novel task** | ↓ naturalised · ✦ revealed · other (v1; six operators later) | **own annotation only** |
| T6 | Ideological signature: projection on M = C×S | E2 | multi-label (20 cells) | LLM-only until annotated | cells of the matrix (from `manifest.json`) | own annotation (campaign 2) |
| T7 | Community of inscription + timeline + hysteresis | E2 | graph + rules | No — rules | community id, trajectory, persistence measures | derived |
| T8 | Card, JSON-LD, explanation | E3 | rendering + LLM | explanation only | — | — |

Design rule (from axiom 10): a component is promoted from "LLM-only, flagged" to "learned model" only after passing the agreement gate in §5.

## 3. Stack — verified against official documentation (2026-09-14)

| Component | Library | Version seen | License | Verified fact that matters here | Decision |
|---|---|---|---|---|---|
| Fine-tuning encoders (T2, T3, T4, T5) | `transformers` | 5.17.0 | Apache-2.0 | Trainer API for token and sequence classification; subword alignment via `word_ids()`, `-100` on non-first subwords | **Adopt** |
| Base encoders | `FacebookAI/xlm-roberta-large`, `microsoft/mdeberta-v3-base` | — | MIT / MIT | Both on the Hub with permissive licenses; multilingual (CC100 / CommonCrawl) | **Adopt both as candidates**; pick per task by dev-set F1 |
| Sentence segmentation, base NER | spaCy | 3.8.16 | MIT (library) | Model packages differ: `en_core_web_lg` MIT, **`es_core_news_lg` GPL-3.0**, **`it_core_news_lg` CC BY-NC-SA 3.0** | Library OK. **Do not vendor ES/IT models** in the Apache-2.0 release; load them as external runtime dependencies, and evaluate an Apache/MIT-licensed multilingual NER from the Hub as replacement (open flag F1) |
| Communities (T7) | python-igraph | 1.0.0 | GPL | `Graph.community_leiden(...)` and `community_multilevel(...)` native | **Adopt igraph for Leiden** (NetworkX 3.6.1 exposes Leiden only via a backend). GPL is acceptable for an unmodified dependency; do not fork it |
| Topology (E3, only if claimed) | ripser.py | 0.6.15 | MIT | Actively maintained (2026-05 release) | **Adopt**; giotto-tda (0.6.2, AGPL-3.0, last release 2024-05) rejected on license and maintenance |
| Ontology, JSON-LD (T8) | rdflib | 7.6.0 | BSD-3 | JSON-LD serializer built in (`format="json-ld"`); SKOS/OWL as namespaces, no reasoning | **Adopt** for export; Owlready2 (0.51, LGPL) only if OWL reasoning is ever needed |
| LLM serving (Stage 1, T8) | vLLM / Ollama | 0.29.0 / 0.34.0 | Apache-2.0 / MIT | Both accept a full JSON Schema for constrained output (vLLM `response_format` json_schema; Ollama `format`) | **vLLM for the deployed site; in Kaggle/Colab notebooks use the constrained-decoding option verified at S1 (§5b)** |
| API | FastAPI | 0.141.1 | MIT | — | **Adopt** |
| Agreement (gate) | `krippendorff` | 0.8.2 | GPL-3.0 | `alpha(reliability_data, level_of_measurement="nominal")` | **Adopt** in analysis scripts only |
| Releases → DOI | Zenodo–GitHub | — | — | Each GitHub release ingested as a version DOI under one concept DOI; metadata via `CITATION.cff` or `.zenodo.json` | **Adopt**; add `CITATION.cff` in sprint 0 |
| Preregistration | OSF "OSF Preregistration" template | — | — | Created from the project's Registrations tab; embargo up to four years | **Adopt**; no embargo (Gold Route) |
| Model / dataset cards | HF Hub docs; `datasets` 5.0.1 | — | Apache-2.0 | README.md with YAML front matter (`license`, `language`, `datasets`, `base_model`) | **Adopt**; mirror weights on Zenodo |

Open flags from verification: **F1** ES/IT spaCy model licenses vs. Apache-2.0 redistribution (decide by sprint 1); **F2** the open-weights instruction model itself is not yet chosen — its license must permit research redistribution of outputs, and its version must be pinned and hashed.

## 4. Timeline (Oct 2026 – Jun 2027; fits the Hiroshima stay ending May 2027)

| Sprint | Dates | Deliverable | Gate to pass |
|---|---|---|---|
| S0 · Ground | 15 Sep – 12 Oct 2026 | Repo skeleton (Apache-2.0 + CC BY 4.0), `CITATION.cff`, Zenodo link, codebook v1.0 draft (trilingual), JSON schema derived from the ontology, pilot corpus chosen (comparative constitutions via Constitute API, social object = emergency provisions, topic key `em`, EN first, ES second; other datasets listed; F3 done) | Codebook v1.0 frozen → Zenodo DOI |
| S1 · Stage 1 MVP | 13 Oct – 16 Nov 2026 | LLM pipeline with constrained JSON, E1–E3 cards, FastAPI backend, minimal front end, reflexive log; internal alpha of the site | 50 texts run end-to-end; every output carries hash + date |
| S2 · Prereg | 17 – 30 Nov 2026 | OSF preregistration sealed (skeleton in §6), annotator training, pilot annotation of 100 segments, codebook v1.1 if needed | Pilot α reported; prereg sealed **before** the main campaign |
| S3 · Annotation campaign 1 | 1 Dec 2026 – 31 Jan 2027 | ~2 000 article-level segments from ≥ 12 constitutions, 4 expert annotators, T2 + T5 (T3 is a rule on this corpus; T1 slots on a 500-segment subset); EN texts first, ES originals as second track; adjudicated gold set | α per task computed; gate decisions recorded |
| S4 · Evaluation of Stage 1 | 1 – 21 Feb 2027 | LLM vs. gold on every gated task; calibration and abstention analysis; adversarial ↓/✦ flip test | Evaluation report v1 (Zenodo) |
| S5 · Stage 3 models | 22 Feb – 4 Apr 2027 | Fine-tuned encoders for tasks that passed the gate; silver filtering; per-language metrics; model cards | Dev-set macro-F1 beats LLM baseline, or task stays LLM-only |
| S6 · Deploy + dataset release | 5 Apr – 2 May 2027 | Models in production; LLM demoted to explanation; dataset v1 (annotations keyed to open-licensed texts) on Zenodo + HF; public beta of the site | Datasheet + model cards published |
| S7 · Campaign 2 (T6) | May – Jun 2027 | Ideological-signature annotation on M = C×S; α gate; report | Decision: T6 learned or LLM-only |
| S8 · Paper | Jun 2027 | Methods paper: "Can naturalization be annotated? An inter-annotator study of ↓/✦ …" (working title) | Preregistered hypotheses answered |

Effort assumption: Luis + 4 annotators (budgeted in SPReAD) + lab GPU access. If annotators start later than December, S3–S6 shift one-for-one; S1 and S2 do not depend on them.

## 5a. Acquisition rule: API as channel, frozen text as data

Models are trained on **text**, never "on the API". The API is the acquisition channel and is preferred over scraping because it returns article-level sections with stable identifiers (constitution id + section id), topic keys (free silver labels for filtering), language and per-record copyright/translator metadata. But every training and evaluation run reads from a **frozen local snapshot** (dump date, per-section hash, API version noted in the datasheet) — the in-emendable record of axiom 1 — never from live calls, because live output can change between runs and would make the evaluation set unreproducible. The public analyzer may call the API live only for the *explanation* of a user text, never for the gold set.

## 5b. Compute: Kaggle / Colab for training and model exploration (decision 2026-09-14)

Training and the model bake-off run on **Kaggle Notebooks and Google Colab**, not on a lab server. What the official pages confirm (Colab FAQ, 2026-09-14): free runtimes last at most 12 h and idle runtimes are terminated; GPU types vary and are not guaranteed; Pro+ allows background execution up to 24 h with compute units; Drive mounting works; outbound internet is allowed, so `push_to_hub` works. Kaggle's docs pages are JS-gated and could not be read; the commonly cited 30 GPU-hours/week, T4×2 / P100, 12 h sessions and the "Internet" toggle are **unverified** and must be checked in the Kaggle UI at S1; the Hugging Face token via Kaggle "Add-ons › Secrets" is confirmed by HF's official blog.

Working rules that follow from those limits:
- Every training script is **resumable** (checkpoint to Drive or a Kaggle Dataset every N steps) and finishes a fold inside one 12 h session; encoders of the XLM-R-base / mDeBERTa-base size on ~2 000 segments fit comfortably, XLM-R-large is the upper bound.
- The frozen snapshot (§5a) is uploaded once as a **private Kaggle Dataset / Drive folder** with its hash; notebooks never call the Constitute API.
- Secrets (HF token, Zenodo token) go in Kaggle Secrets / Colab `userdata`, never in the notebook.
- Each experiment logs config + metrics to a `runs.csv` committed to GitHub; the winning run's weights go to the HF Hub with a model card; the notebook itself is exported to the repo (`notebooks/`).
- Model exploration = a fixed bake-off protocol, not ad-hoc trials: same frozen train/dev split, same seeds (3), same metric (macro-F1 per task per language); candidates in order: mDeBERTa-v3-base, XLM-R-base, XLM-R-large, plus one legal-domain multilingual encoder if one with a permissive licence is found.
- The Stage 1 LLM bake-off (open-weights instruction models with JSON-schema output) also runs here, quantised to fit a T4; vLLM is replaced in-notebook by `transformers` + an outlines/xgrammar-style constrained decoder, or by Ollama on Colab, whichever the docs support at S1 — verify before use.

## 5. Gates and metrics

- **Agreement gate:** Krippendorff's α (nominal) ≥ 0.67 on the adjudicated pilot for a task to be trained; α ≥ 0.80 is the target for reporting a task as reliably annotatable. Below 0.67 the task stays LLM-only, is shown with a warning label, and the result is reported as a finding.
- **Model gate:** macro-F1 on the held-out gold set, per language; a fine-tuned encoder replaces the LLM for a task only if it beats the LLM baseline on that task's gold set.
- **Axiom checks:** calibration (ECE) and abstention rate; adversarial flip test for T5 (same claim rewritten as fact vs. as position must flip the label); ablation for T6 (signature must not be predictable from source/genre alone).
- **Reproducibility:** frozen evaluation set with DOI; pinned model versions and hashes; one command reruns the evaluation.

## 6. Preregistration skeleton (OSF Preregistration template)

**Study information.** Title: *Annotating naturalization: inter-annotator reliability of New-Realist operators and ontological entity types in comparative constitutional texts.* Authors: L. F. Bourguet González (LabOnt, UniTo; CSS Lab, Hiroshima) and annotators. Description: an annotation-reliability study and a model-evaluation study for tasks T2 and T5 on a comparative-constitutions corpus (campaign 1).

**Hypotheses.**
- H1 (reliability, ordered): α(T2 entity typing) > α(T5 operator). Rationale: T2 follows an explicit three-way ontology; T5 requires a pragmatic judgment about how a claim is presented.
- H2 (threshold): α(T5) ≥ 0.67 when the label set is collapsed to {↓, ✦, other}; we do not predict the six-operator set reaches the threshold in campaign 1.
- H3 (model vs. humans): the Stage 1 LLM's agreement with the adjudicated gold is lower on T5 than on T2.
- H4 (legal family): α(T5) does not differ by more than 0.10 between constitutions of different legal families / regions (Latin America vs. Spain vs. English-language translations), i.e., naturalisation is annotatable across constitutional traditions.
- H5 (language / translation): α(T5) on Spanish originals is not lower than on the English texts by more than 0.10.
- H6 (competing realities, exploratory): emergency provisions receive different operator profiles (↓ vs. ✦ proportions) across constitutions and legal families — e.g. clauses that state the triggering threat as a fact ("in case of grave disturbance of public order") vs. clauses that expose it as a declared, reviewable act — the empirical signature the analyzer is meant to surface.

**Design plan.** Study type: observational annotation study with a computational evaluation. Blinding: annotators blind to each other and to LLM output. Design: each segment annotated independently by 3 of 4 annotators (rotating), adjudication by the 4th; the LLM annotates all segments once, version pinned.

**Sampling plan.** Existing data: none of the target texts have been annotated; the LLM outputs on them will not be inspected before the preregistration is sealed. Data source: constitutional texts retrieved via the Comparative Constitutions Project / Constitute APIs (English), plus other constitutional datasets named in the sealed record (API terms and licences recorded), segmented at article level and restricted to sections tagged with topic key `em` (Emergency provisions) via `sectionstopicsearch`, plus their immediately adjacent sections as controls. Sample size: 2 000 article-level segments (≈ 1 300 English, ≈ 700 Spanish originals; balanced across at least 12 constitutions); rationale: pilot-based estimate for a 95 % CI half-width of about 0.03 on α at the expected level. Stopping rule: fixed N.

**Variables.** Manipulated: none. Measured: T2 label (3 classes), T5 label (3), language (EN / ES original), constitution id, CCP variables where relevant, legal family/region, annotator id, LLM label per task. Indices: α per task × language × legal family; LLM–gold agreement (α and macro-F1).

**Analysis plan.** α with the `krippendorff` package (nominal); bootstrap CIs (1 000 resamples) over segments; H1–H2 by CI comparison; H3 by paired comparison of LLM–gold vs. human–gold agreement; H4–H5 by α differences with bootstrap CIs. Inference criteria: CI-based, α = .05 two-sided. Data exclusion: segments flagged as non-textual or duplicated; annotator drop-out handled by the rotation. Missing data: segment excluded from the affected task only. Exploratory: six-operator labels, confusion patterns between ↓ and "other".

**Other.** Codebook v1.0 DOI, ontology DOI and pinned LLM version are attached at sealing. Enforced order: freeze codebook → Zenodo DOI → seal OSF → start campaign.

## 7. Website scope for the public beta

Structured analyzer first, chat second. The pasted text is not stored unless the user opts in; opted-in texts join a documented corpus with a stated license. Every card shows the emendable / in-emendable tag, the model version and the date. No "verdict" language: the interface says what is inscribed, what is claimed, and how it is presented (↓ / ✦), never what is true.

## 8. Decisions

**Closed on 2026-09-14 (Luis):**

- D1 · Pilot corpus: **comparative constitutions** (decision of 2026-09-14, replacing an earlier single-reform proposal that was discarded). The corpus is a set of constitutional texts — strong documents by definition (founding inscriptions) — and the "competing realities" are the different constructions of the *same* social object across constitutions and legal families (candidates for the pilot object: *the people / pueblo*, *sovereignty*, *emergency powers*, *the Other / foreigner*; choose one in S0). **English first**, retrieved through the Comparative Constitutions Project / Constitute APIs (English texts and translations, plus CCP's coded variables), complemented by other constitutional datasets to be listed in S0; Spanish originals (Latin America + Spain) second, as a validation track. **API terms and text licence to be verified in S0 before any redistribution** (open flag F3). Consequences: the strong/weak distinction (T3) is no longer a learned task in campaign 1 — the whole corpus is strong — so T3 becomes a rule (document type = constitution) and the released annotation budget goes to T5 and T2; the weak side (press, debates) can be added as a later campaign if a comparison act-vs-record is wanted.
- D2 · Operator task T5 starts with **three labels {↓ naturalised, ✦ revealed, other}**; the six-operator set is exploratory in campaign 1 and becomes a gated task only once α on the three-label set is known.

**Still open:**

1. The open-weights instruction model (license, size, ES/IT quality) — pick in S1 after a 3-model bake-off on 50 texts.
2. ES/IT NER replacement (flag F1).
3. Whether campaign 1 includes T1 slots on the full set or only a 500-segment subset (current plan: subset).
4. **F3 — verified 2026-09-14 (official pages).** Constitute texts are **CC BY-NC 3.0 Unported** (About page); the Terms page adds "commercial use is expressly prohibited". Third-party texts (HeinOnline, OUP, IDEA Arabic) keep their own copyright — the API's per-constitution `copyright` and `translator` fields must be checked record by record. The CCP coded dataset v5.0 (Feb 2025) states **no explicit licence**, only a required citation (Elkins & Ginsburg 2025) — ask CCP before redistributing it. **Consequence:** texts are *not* shipped inside the CC BY 4.0 dataset release; the release contains annotations keyed to `constitution id + section id`, plus a fetch script against the documented API (`https://www.constituteproject.org/service/`: `constitutions`, `topics`, `sectionstopicsearch`, `textsearch`, `html`; `lang=en|es|ar`; JSON). robots.txt disallows automated `/constitutions` and `/service/constopicsearch` — the fetcher respects it and uses the documented endpoints and the XML dumps. The non-commercial clause also means the public analyzer must not be monetised while it serves Constitute text. Same check pending for every other dataset added.
5. **Pilot social object — coverage counted 2026-09-14; decided as D3** from `/service/topics` (`count` = constitutions in the whole corpus, historical included; in-force counts still to be pulled via `constopicsearch` in a compliant client):
   - *Emergency powers* → one clean topic key, **`em` "Emergency provisions", 390**.
   - *The people / popular sovereignty* → no literal topic; closest **`auth` "Source of constitutional authority", 320**, plus `referen` 317, `initiat` 116.
   - *Sovereignty* → no topic; scattered across `system` 379, `intlaw` 384, `access` 108, `seccess` 47.
   - *The Other / foreigner* → scattered: `resenex` 124, `equalgr2` 76, `citizen` 348, `natcit` 282, `citrev` 291, `citdep` 106.
   **D3 — decided 2026-09-14 (Luis): pilot on `em` Emergency provisions.** Single topic key, widest coverage, and the passage type where naturalisation (↓) is expected to be densest ("when public order is threatened…"). `auth` (the people as inscribed source of authority) is reserved as the second social object for a later campaign.
6. **Spanish track confirmed:** `lang=es` returns ~80 constitutions (Spanish Constitute, 2024, with Dejusticia and Universidad de los Andes); whether each is an original or a translation is per record (`translator` field).

## Self-audit

Versions and licenses in §3 come from official pages read on 2026-09-14 and can change; re-check at S0. The α thresholds (0.67 / 0.80) are Krippendorff's conventional tentative cut-offs, not project-validated values. The sample-size rationale in §6 is an assumption pending the pilot; recompute after S2 and record the change in the OSF record before sealing. The timeline assumes annotators from December; that dependency is the main schedule risk.

# Codebook — v0.1 (scaffold, not yet frozen)

Licence: CC BY 4.0. The codebook is frozen at v1.0, deposited on Zenodo (DOI), and only then is the OSF preregistration sealed and annotation started. Changes after freezing produce v1.x with a changelog; the sealed registration names the exact version used.

Pilot corpus: sections tagged `em` (Emergency provisions) on Constitute, in-force constitutions, English first, Spanish originals second. Unit of annotation: **one section** (article or numbered paragraph as delivered by the API), read together with its adjacent sections for context.

## Tasks annotated in campaign 1

### T2 — Ontological entity typing
Every entity mention in the section receives exactly one type from Ferraris's table (Hernández Marcelo 2020, p. 21):

| Type | In space | In time | Depends on subjects | Constitutional examples (to be filled with real passages) |
|---|---|---|---|---|
| physical | yes | yes | no | territory, persons, buildings, weapons |
| ideal | no | no | no | numbers, time limits as quantities, logical relations |
| social | yes | yes | **yes** | the state of siege, the President, Congress, the decree, public order, the nation |

Decision rules, boundary cases and counter-examples: *to be written from the pilot (S2)*.

### T5 — Operator on each claim (three labels in campaign 1)
Each claim in the section is labelled by **how it presents what it asserts**, not by whether it is true:

- **↓ naturalised** — the claim presents a socially inscribed state of affairs as a plain fact, with no marker that it is declared, assessed, or reviewable (e.g. the triggering threat stated as given: "in case of grave disturbance of public order").
- **✦ revealed** — the claim exposes its own act character: who declares, under what assessment, subject to what review or limit (e.g. "the President may, upon assessment by the Council and subject to ratification by Congress, declare…").
- **other** — claims where neither reading applies or the section is purely procedural.

The six-operator set (⇒ ⊕ ↓ ∅ ✦ ∥) is recorded as an **exploratory** secondary label and is not gated in campaign 1.

Decision rules, examples per label from ≥ 4 constitutions, and the adjudication protocol: *to be written (S0–S2)*.

## Agreement gate
Krippendorff's α (nominal) ≥ 0.67 for a task to be trained; ≥ 0.80 reported as reliable. Below 0.67 the task stays LLM-only with a warning label and the result is reported.

## Versions
- v0.1 — 2026-09-14 — scaffold.

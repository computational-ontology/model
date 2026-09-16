# Stage 1 output schema

`stage1_output.schema.json` is generated from `nra.schema.Stage1Output` (`python -m nra.schema`)
and is the grammar handed to the constrained decoder in the Stage 1 notebooks. Do not edit the
JSON by hand; change the pydantic model and regenerate.

## Two layers

| Layer | Class | Who produces it | Contents |
|---|---|---|---|
| Model output | `Stage1Output` | the LLM (or a human, in the annotation tool) | `t2` mentions typed physical / ideal / social; `t5` claims labelled naturalised / revealed / other, with verbatim `markers`, the v2.0 `frame` and `ground` fields and an optional exploratory `secondary` operator; `notes` |
| Record | `Stage1Record` | the harness | section identity by `constitution_id` + `section_id` + `sha256` (never the text), `annotator`, `emitter_kind`, `emitted_at` (timezone-aware), `codebook_version`, `prompt_version`, `decoding` parameters, `parse_ok`, `verbatim_ok`, and the `output` |

The model never sees or emits identifiers, dates or versions — it cannot get them wrong if it
never produces them. Every span it emits (`mention`, `claim`, `markers`) must be a verbatim
substring of the section; `nra.schema.check_verbatim` enforces this after decoding and the result
is stored in `verbatim_ok`, so paraphrase is measured, not silently accepted.

## Placement in the project tables

A record is the inscription of an act of labelling — who, what act, on which support, when
(thesis 5). When the emitter is a model it is a weak document whose emitter is the model and whose
date is the run (thesis 9; plan §C.4). Everything in the record is amendable (Table 1); the
section it points to, fixed by its hash in the snapshot manifest, is not.

## Label sets

- `type`: `physical`, `ideal`, `social` (codebook §2).
- `operator`: `naturalised` (↓), `revealed` (✦), `other` (codebook §3, decision D2).
- `ground` (v2.0, decision D22): `nature`, `history`, `god`, `spirit`, `doctrine` (naturalising
  grounds), `act` (revealing ground), `none` — what the clause makes the founding act rest on
  (codebook §3.1). The operator is decided from it (§3.3).
- `frame` (v2.0): `attitude`, `will`, `procedure`, `invocation`, `narrative`, `none` — how the
  enunciator relates the clause to itself (codebook §3.2); never changes the ground.
- `secondary` (exploratory, not gated): `implication` ⇒, `aggregation` ⊕, `naturalisation` ↓,
  `erasure` ∅, `revelation` ✦, `parallel` ∥ — the six operators of *Ideological Architectures*.
  English names are provisional; the symbols are canonical.

## Example (Ireland, art. 28.3.2º — codebook §3)

```json
{
  "t2": [
    {"mention": "actual invasion", "type": "physical"},
    {"mention": "the Government", "type": "social"},
    {"mention": "Dáil Éireann", "type": "social"}
  ],
  "t5": [
    {"claim": "In the case of actual invasion", "operator": "naturalised", "markers": ["In the case of"], "secondary": "naturalisation"},
    {"claim": "the Government may take whatever steps they may consider necessary", "operator": "revealed", "markers": ["may take", "may consider"], "secondary": "revelation"}
  ],
  "notes": ""
}
```

# Codebook — v0.2 (scaffold with worked examples; not yet frozen)

Licence: CC BY 4.0. The codebook is frozen at v1.0, deposited on Zenodo (DOI), and only then is
the OSF preregistration sealed and annotation started. Changes after freezing produce v1.x with
a changelog; the sealed registration names the exact version used.

Corpus: every section tagged `em` (Emergency provisions) on Constitute for in-force constitutions,
snapshot of 2026-09-14 (740 EN + 180 ES sections). Unit of annotation: **one section** as
delivered by the API, read with its chapter/article breadcrumb. Strata: `chapter_type`
(see `nra.strata`). Pilot: `data/splits/pilot_100.json`.

Worked examples below quote official constitutional texts in their original language, from
Constitute records with no copyright or translator field (India, Kenya, Liberia, Antigua and
Barbuda, Dominica, Fiji, Ireland, Namibia, Nigeria, Gambia, Ghana, Sierra Leone; Bolivia, Chile,
Argentina, Dominican Republic). Cite: Elkins, Ginsburg & Melton, *Constitute*, constituteproject.org.
Readings marked **[proposed]** are the drafter's proposals and become rules only when the
annotation lead confirms them.

---

## 0 · What we annotate and why

The analyzer follows Ferraris: a constitution is a *strong document*, the inscription of an act.
Its emergency provisions are where a constitution says how the ordinary order may be
suspended. We annotate two things in each section:

- **T2 — what kind of things the section talks about** (physical, ideal, social objects), so the
  pipeline can catalogue the life-world the clause presupposes;
- **T5 — how each claim presents what it asserts**: as a plain fact of the world (naturalised,
  ↓), as the outcome of a declared, assessed or reviewable act (revealed, ✦), or neither.

The T5 contrast is the empirical core of the project: the same social object — "a threat to
public order", "a state of emergency" — is inscribed either as something that simply *is the
case* or as something someone *declares, assesses and can be checked on*. Nothing here judges
whether a clause is good or true; only how it is written.

## 1 · Unit, granularity, workflow

- **Section** = the record as delivered (one file in the snapshot). Never edit the text.
- **Claim** = a clause that asserts, permits, obliges or defines something; a section has one or
  more claims. Enumerated items ("1.", "a.") are separate claims. T5 is labelled **per claim**;
  T2 **per entity mention**.
- Each annotator works alone from the codebook; no LLM output is shown during annotation.
- Output format: one JSON line per section — `{"constitution_id", "section_id", "lang",
  "annotator", "t2": [{"mention", "type"}], "t5": [{"claim", "operator", "markers"}], "notes"}`.
- Doubt goes in `notes`; never leave a claim unlabelled ("other" exists for that).

## 2 · T2 — Ontological entity typing

Ferraris's three types (Hernández Marcelo 2020, p. 21), with the three coordinates:

| Type | In space | In time | Depends on subjects | Constitutional examples |
|---|---|---|---|---|
| **physical** | yes | yes | no | territory, persons (as bodies), buildings, weapons, natural disasters |
| **ideal** | no | no | no | numbers, time limits as quantities ("six months"), logical relations |
| **social** | yes | yes | **yes** | the State, the President (as office), Parliament, a proclamation, a state of emergency, public order, war (as a legal status), a right |

Decision rules **[proposed]**:

1. Type the *referent as used in the clause*, not the word. "War" in "Sierra Leone is at war" is a
   social object (a legal status that exists only because it is declared and recognised); "armed
   rebellion" in "threatened by armed rebellion" is physical (bodies and weapons in a territory).
   Where both readings are live, choose social and note it.
2. Offices are social; the human who holds one is physical. "The President" in a competence clause
   is social; "any person" in a rights clause is physical.
3. Rights, guarantees, duties, powers and competences are social objects.
4. Durations, thresholds and counts are ideal ("four years", "two-thirds").
5. Territory and "any part thereof" are physical; "the Republic", "the State", "the Federation"
   are social.

Worked examples (mention → type):

- *India, art. 352 Explanation*: "security of India" → social · "territory thereof" → physical ·
  "war", "external aggression" → social **[proposed: social, as legal statuses]** · "armed
  rebellion" → physical · "the President" → social · "imminent danger" → social
  **[proposed; the danger is an assessed condition, not a body]**.
- *Kenya, art. 29(b)*: "every person" → physical · "right to freedom and security of the person"
  → social · "state of emergency" → social · "Article 58" → social (an inscription).
- *Bolivia, art. 137*: "seguridad del Estado" → social · "amenaza externa" → social · "conmoción
  interna" → social · "desastre natural" → physical · "la Presidenta o el Presidente" → social ·
  "territorio" → physical · "derechos fundamentales", "debido proceso" → social.
- *Nigeria, s. 64(3)*: "the Federation" → social · "territory of Nigeria" → physical · "the
  President" → social · "four years", "six months" → ideal · "elections" → social.

Boundary cases to settle in the pilot: "the nation" (social) vs. "the people" (social, but often
used as bodies); "public order"; "calamidad pública" (physical event vs. declared status).

## 3 · T5 — Operator on each claim (three labels in campaign 1)

Label each claim by **how it presents what it asserts**, not by whether it is true or desirable.

| Label | Definition | Typical markers |
|---|---|---|
| **↓ naturalised** | The claim presents a socially inscribed state of affairs as a plain fact of the world: the trigger, threat or situation is *given*, with no marker of who declares it, on what assessment, or under what check | "in case of", "when X threatens", "during any period of public emergency", "the situation that exists", "en caso de", "cuando afecten gravemente" |
| **✦ revealed** | The claim exposes its own act character: it names who declares, that an assessment or satisfaction is required, a procedure, a limit, a review or a consent | "if the President is satisfied", "may declare", "subject to Article 58", "with the consent of the Senate", "reasonably justifiable" only when tied to a reviewer, "con acuerdo del Senado", "aprobar", definitions of the emergency *as* a proclamation |
| **other** | Purely procedural or definitional claims that neither state a situation as fact nor expose an act (e.g. summoning rules with no trigger), or claims where neither reading applies | — |

Decision test **[proposed]**: for the state of affairs the claim relies on, ask *"who says so, and
could anyone check?"*. If the clause answers (an actor, an assessment, a limit, a review), ✦.
If the clause treats it as simply existing, ↓. If the clause relies on no such state of affairs,
*other*. A section usually mixes both: **label at claim level and let the mix be the datum**.

Worked examples (claim → label → why):

- *India, art. 352 Explanation*: "a proclamation … may be made before the actual occurrence of war
  … if the President is satisfied that there is imminent danger" → **✦** (declaring actor +
  explicit satisfaction test). Inside it, "the security of India … is threatened by war or by
  external aggression or by armed rebellion" is quoted as the *content* of the proclamation, so it
  is not a separate naturalised claim **[proposed]**.
- *Antigua and Barbuda, s. 16* and *Dominica, s. 14* (near-identical): "measures that are
  reasonably justifiable for dealing with the situation that exists … during that period" →
  **↓**: the "situation that exists" is given; "reasonably justifiable" names a standard but no
  reviewer **[proposed; alternative reading: ✦ because "reasonably justifiable" is justiciable —
  decide in the pilot; this is the kind of case that fixes the rule]**.
- *Kenya, art. 29(b)*: "detained without trial, except during a state of emergency, in which case
  the detention is subject to Article 58" → **✦** (the exception is tied to a review regime).
- *Sierra Leone, s. 171*: "'Public Emergency' includes any period during which … there is in force
  a Proclamation issued by the President … or a Resolution of Parliament" → **✦** in its purest
  form: the emergency is *defined as* the existence of an inscribed act. Item (a) "Sierra Leone is
  at war" → **↓**.
- *Ireland, art. 28.3.2º*: "In the case of actual invasion" → **↓** (given fact); "the Government
  may take whatever steps they may consider necessary … and Dáil Éireann … shall be summoned" →
  **✦** (actor, discretion, summoning).
- *Nigeria, s. 64(3)*: "If the Federation is at war in which the territory … is physically
  involved" → **↓**; "the President considers that it is not practicable to hold elections, the
  National Assembly may by resolution extend … no such extension shall exceed six months" → **✦**.
- *Chile, art. 39*: "sólo puede ser afectado bajo las siguientes situaciones de excepción: guerra
  externa o interna, conmoción interior, emergencia y calamidad pública, cuando afecten gravemente
  el normal desenvolvimiento de las instituciones" → **↓** (situations listed as conditions of the
  world; no actor in this clause) **[proposed]**.
- *Argentina, art. 23*: "En caso de conmoción interior o de ataque exterior que pongan en peligro el
  ejercicio de esta Constitución … se declarará en estado de sitio" → **↓** for the trigger
  (impersonal "se declarará", danger given); "no podrá el presidente … condenar por sí ni aplicar
  penas. Su poder se limitará …" → **✦** (limits on the actor). *Argentina, art. 99.16*: "Declara
  en estado de sitio … con acuerdo del Senado … El presidente la ejerce con las limitaciones
  prescriptas en el artículo 23" → **✦**. *Argentina, art. 61*: Senate authorises → **✦**.
- *Bolivia, art. 137*: "En caso de peligro para la seguridad del Estado, amenaza externa, conmoción
  interna o desastre natural" → **↓**; "la Presidenta o el Presidente … tendrá la potestad de
  declarar … La declaración … no podrá en ningún caso suspender …" → **✦**. *Art. 172.26* and
  *art. 158.6* (declare / approve the state of exception) → **✦**.
- *Gambia, s. 96(2)*, *Ghana, art. 113(3)*, *Dominica, s. 54(5)*: summoning Parliament "in the
  event of a declaration of a public emergency" → **✦** where the trigger is *a declaration*;
  Ghana's "the President is satisfied that owing to the existence of a state of war … it is
  necessary" mixes an assessment (✦) with "the existence of a state of war" (↓).
- *Dominican Republic, art. 51.1*: "En caso de declaratoria de Estado de Emergencia o de Defensa, la
  indemnización podrá no ser previa" → **✦** (trigger is the *declaratoria*).
- *Namibia, art. 32(3)(f)*: "declare martial law or, if it is necessary for the defence of the
  nation, declare that a state of national defence exists … subject to Article 26(7)" → **✦**;
  note the phrase "declare that a state … exists": an act that inscribes a fact — the revealed
  form of naturalisation, worth a note in every such case.

The six-operator set (⇒ ⊕ ↓ ∅ ✦ ∥) is recorded as an **exploratory** secondary label and is not
gated in campaign 1.

## 4 · Adjudication and the agreement gate

- Pilot: 100 sections (`pilot_100.json`), each annotated independently by 3 of 4 annotators;
  the 4th adjudicates disagreements and records the rule that resolves each one. Rules born in
  adjudication go into v1.1 of this codebook, dated.
- Krippendorff's α (nominal) is computed per task and language on the pilot: **≥ 0.67** to train a
  task, **≥ 0.80** reported as reliable; below 0.67 the task stays LLM-only with a warning label and
  the result is reported as a finding.
- The main campaign covers the whole population (920 sections) with the same rotation.

## 5 · Versions

- v0.1 — 2026-09-14 — scaffold.
- v0.2 — 2026-09-14 — worked examples from 17 original-language constitutions; proposed decision
  rules and boundary cases; output format; adjudication protocol.
- v1.0 — *pending*: rules confirmed by the annotation lead; frozen; Zenodo DOI.

# Codebook — v2.0 (founding inscriptions)

Licence: CC BY 4.0. v2.0 is frozen, released on GitHub and deposited on Zenodo (DOI), and only then
is the OSF preregistration sealed and annotation started. Changes after freezing produce v2.x with
a changelog; the sealed registration names the exact version used. v1.0 (emergency provisions) is
archived at tag `v1.0.0`; its T2 rules carry over unchanged, its T5 test does not (§3, §6).

Corpus (campaign 1, decision D20): the **preamble** of every in-force constitution tagged `preamble`
on Constitute, snapshot of 2026-09-16 (EN 150 + ES 40 records after the `nra.preamble` filter; 37
translation pairs). Unit of annotation: **one preamble** as delivered by the API (one record, its
paragraphs recoverable as `section/N` offsets). Strata: language × length band (`short` < 600 <
`medium` < 2 000 < `long` characters). Pilot: `data/splits/pilot_preamble_100.json` (seed 20260916).

Worked examples below quote short phrases of constitutional texts from Constitute records with no
copyright or translator field (Azerbaijan 2016, Ireland 2019, South Africa 2012, India 2023, Greece
2019 in English; Costa Rica 2020, Spain 2011, Bolivia 2009, China 2004 in the Spanish record). Two
pilot preambles whose English records are copyrighted translations (Taiwan 2005, © OUP / Max Planck;
Madagascar 2010, © Hein) are cited by paragraph with fragments of a few words only. Cite: Elkins,
Ginsburg & Melton, *Constitute*, constituteproject.org (CC BY-NC 3.0; texts are never shipped with
the annotations, decision D4). Decision rules and readings were confirmed by the
annotation lead (L. F. Bourguet González) on 2026-09-16 (decisions D21–D23). Rules born in pilot
adjudication go into v2.1.

---

## 0 · What we annotate and why

A constitution is a *strong document* — the inscription of an act (Ferraris, *Documentalidad*,
pp. 365–367; thesis 9). Its preamble is where the constitution inscribes the conditions of its own
genesis: who enacts it, by what title, and on what it rests. Ferraris names the two ways this can
be done: *foundation according to the spirit* — the people, the nation, its roots, its history —
and *foundation according to the letter* — treaties, edicts, procedures, prior documents
(*Documentalidad*, pp. 353–355). We annotate two things in each preamble:

- **T2 — what kind of things the preamble talks about** (physical/natural, ideal, social objects),
  so the pipeline can catalogue the life-world the founding act presupposes;
- **T5 — what each claim makes the founding act rest on**: on something presented as existing
  before and independently of any act (naturalised, ↓), on an act — a procedure, a mandate, a prior
  inscription, the subject's own declared will (revealed, ✦), or on nothing (other).

The T5 contrast is the empirical core of the project. Nothing here judges whether a preamble is
good, or whether what it says is true — the past events a preamble cites are irrevocable
(*Manifiesto*, pp. 69–71). ↓ labels the *derivation* of the act from a ground, never the ground.

## 1 · Unit, granularity, workflow

- **Preamble** = the record as delivered (one file in the snapshot). Never edit the text.
- **Claim** = a clause that offers a ground, a purpose, an attitude, an invocation or the enacting
  formula. A preamble is usually one sentence unfolded in participial clauses ("Recognising …",
  "Convinced that …", "Wishing …", "We … adopt"): **each such clause is a claim**; each item of an
  enumerated purpose list is a claim; each paragraph of a narrative preamble (China, Bolivia) is one
  or more claims, split at sentence boundaries. When one clause coordinates several grounds
  ("cumpliendo el mandato de nuestros pueblos, con la fortaleza de nuestra Pachamama y gracias a
  Dios"), split it into one claim per ground.
- T5 is labelled **per claim**, with three fields (§3): `operator`, `frame`, `ground`; T2 **per
  entity mention**.
- Each annotator works alone from the codebook; no LLM output is shown during annotation.
- Output format: one JSON line per preamble — `{"constitution_id", "section_id", "lang",
  "annotator", "t2": [{"mention", "type"}], "t5": [{"claim", "operator", "markers", "frame",
  "ground"}], "notes"}`. Every `claim`, `mention` and marker is a verbatim substring of the record.
- Doubt goes in `notes`; never leave a claim unlabelled ("other" exists for that).

## 2 · T2 — Ontological entity typing (unchanged from v1.0)

Ferraris's three types (Hernández Marcelo 2020, p. 21; *Documentalidad*, thesis 2, p. 423, where
the first type is called *natural* — `physical` in this codebook is the same type):

| Type | In space | In time | Depends on subjects | Preamble examples |
|---|---|---|---|---|
| **physical** (natural) | yes | yes | no | territory, mountains, rivers, natural resources, persons as bodies, "our fathers" |
| **ideal** | no | no | no | numbers, dates as quantities ("1949", "this twenty-sixth day of November"), logical relations |
| **social** | yes | yes | **yes** | the people, the Nation, the State, the Republic, the Constituent Assembly, a referendum, a mandate, a prior constitution or charter, rights, democracy, the Party, a tradition |

Decision rules (confirmed in v1.0, kept):

1. Type the *referent as used in the clause*, not the word. "Territory" as land is physical;
   "territorial integrity" is social (a legal status).
2. Offices and collective subjects are social; the humans who fill them are physical. "The people"
   as the constituent subject is social; "our fathers" as those who struggled are physical.
3. Rights, guarantees, duties, powers, competences and values named as objects ("justice",
   "democracy") are social.
4. Durations, thresholds, counts and dates are ideal.
5. Territory and its parts are physical; "the Republic", "the State", "the Nation" are social.
6. References to other inscriptions ("the Constitutional Act on State Independence", "the
   International Charter of the Rights of Man", "this Constitution") are social.

Worked examples (mention → type):

- *Azerbaijan 2016*: "The Azerbaijan people" → social · "the Constitutional Act on the State
  Independence" → social · "the territorial integrity" → social · "a nationwide referendum" → social.
- *Madagascar 2010*: the fauna, flora and mining resources → physical · the Fokonolona → social ·
  the Malagasy fanahy → social (a tradition) · the International Charter → social.
- *Bolivia 2009*: "montañas", "ríos", "lagos" → physical · "el pueblo boliviano" → social · "la
  Asamblea Constituyente" → social · "nuestros mártires" → physical.
- *China 2004 (ES)*: "1840", "1949" → ideal · "el Partido Comunista de China" → social · "Mao
  Zedong" → physical · "la dictadura democrática popular" → social.

Boundary cases to settle in the pilot: divine names ("God", "the Most Holy Trinity",
"Andriamanitra", "Pachamama") — provisional rule: type as **social** when used as a source of
authority or as an addressee of the act, and always note it; "Madre Tierra" / "sagrada Madre
Tierra" (physical land under a sacralising description — provisionally physical, note it).

## 3 · T5 — Operator, frame and ground (three labels in campaign 1)

Label each claim by **what it makes the founding act rest on**, not by whether it is true or
desirable. Two auxiliary fields are recorded for every claim and the operator is decided from them.

### 3.1 Ground — what the clause offers as that on which the act rests

| `ground` | The act is made to rest on … | Examples |
|---|---|---|
| `nature` | territory, land, resources, human nature, a "sacred" land | "se erigieron montañas, se desplazaron ríos" (Bolivia); "the wealth of the fauna … with which nature has provided Madagascar" |
| `history` | past events, struggles, sufferings, a founding date stated as fact | "the injustices of our past" (South Africa); "En 1949 … fundó la República Popular China" |
| `god` | a divinity as source of authority, as agent in history, or as fact | "from Whom is all authority" (Ireland); "gracias a Dios" (Bolivia) |
| `spirit` | the people, the nation, its traditions, character, roots, heritage, presented as prior to the act | "continuing the traditions of many centuries of their Statehood" (Azerbaijan); "its originality, its authenticity and its Malagasy character"; "the teachings bequeathed by Dr. Sun Yat-sen" |
| `doctrine` | a general truth or theory asserted (about society, development, classes, essence) | "la lucha de clases continuará dentro de ciertos límites" (China); "the development of the personality … is the essential factor of the durable and full development" (Madagascar) |
| `act` | a procedure, an election, a referendum, a mandate, a title, a prior inscription, the subject's own decision or will | "by virtue of the mandate received from the whole body of citizens" (Taiwan); "las Cortes aprueban y el pueblo español ratifica"; "adopted through a nationwide referendum"; "making its own … the Conventions" (Madagascar) |
| `none` | no ground offered: a purpose, a value, a faith, an obligation, a bare invocation | "to establish justice, freedom, security"; "reiterando nuestra fe en la Democracia"; "In the name of the Holy … Trinity" (Greece) |

### 3.2 Frame — how the enunciator relates the clause to itself

| `frame` | Marker type | Examples |
|---|---|---|
| `attitude` | a mental-state verb or participle | "Convinced that", "Recognising", "Conscious that", "Affirming its belief in", "being aware of" |
| `will` | a volitional verb, or the enacting formula in the subject's own name | "wishing", "deseando", "Resolute to", "proclama su voluntad de", "do hereby adopt, enact and give to ourselves" |
| `procedure` | a stated title or procedure of the enunciator | "through our freely elected representatives", "libremente elegidos Diputados a la Asamblea Nacional Constituyente", "IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949", "by referendum" |
| `invocation` | the act placed under a name | "In the name of", "invocando el nombre de Dios" |
| `narrative` | a bare third-person statement; the enunciator is erased | "A partir de 1840, la China feudal se fue convirtiendo …"; "En tiempos inmemoriales se erigieron montañas" |
| `none` | purpose infinitives, definitions, obligations, lists | "to protect the independence …"; "deben tomar la Constitución como norma básica de conducta" |

The frame is a constative element inside a performative document (*Documentalidad*, p. 367: weak
and strong documents "are so easily confused"). **It never changes the ground.** "Convinced that
the Fokonolona constitutes a framework of life" attributes the conviction, but the Fokonolona is
still offered as something that exists before the act: the ground is `spirit`.

### 3.3 Operator — decided from the ground

| Label | Rule |
|---|---|
| **↓ naturalised** | `ground` ∈ {`nature`, `history`, `god`, `spirit`, `doctrine`}: the act is made to rest on something presented as existing before and independently of any act — Ferraris's foundation according to the spirit |
| **✦ revealed** | `ground` = `act`: the act rests on an inscribed act — a procedure, a mandate, a prior inscription, the subject's own declared will — foundation according to the letter; legitimacy "by appeal to other inscriptions held valid" (*Documentalidad*, p. 333 n. 8) |
| **other** | `ground` = `none`: the clause offers no ground (purpose, value, faith, obligation, bare invocation, definition) |

**Decision test (confirmed).** For each claim ask, in order:

1. *Does the clause offer something the founding act rests on* — a reason, a cause, a source of
   authority, a title, a premise? If it only states a purpose ("in order to …", "to secure …"), a
   value, a faith ("belief in God", "fe en la Democracia"), an obligation, or names the act without
   a ground ("In the name of …") → **other**, `ground = none`.
2. *Is that ground itself an inscribed act* — an election, a referendum, a mandate, a Constituent
   Assembly, a prior document, the enunciator's own will or decision stated in its own name →
   **✦**, `ground = act`.
3. *Is the ground presented as prior to and independent of any act* — nature, God as authority or
   as fact, past events stated as facts, the people/nation/tradition/character, a doctrine →
   **↓**, with the matching `ground`.

Rules that go with the test:

- **Attitude frames do not convert.** "Recognising the injustices of our past" is ↓ (`history`,
  frame `attitude`): the past is offered as what the act rests on ("We therefore … adopt"). Only
  a frame that introduces an act distinct from the enunciation — a procedure, a verifiable title, an
  actor that could not have concurred — makes the ground an act.
- **Attitude toward a value or a faith is not a ground.** "Affirming its belief in Andriamanitra"
  (Madagascar), "reiterando nuestra fe en la Democracia" (Costa Rica), "Believe that South Africa
  belongs to all who live in it" → **other**: the complement names the subject's own belief or a
  value, not a state of affairs the act rests on. Note such cases: they are where annotators will
  disagree.
- **Invocation without derivation is other; invocation with derivation is ↓.** "In the name of the
  Holy and Consubstantial and Indivisible Trinity" (Greece) → **other**, `frame = invocation`,
  `ground = none`. "In the Name of the Most Holy Trinity, from Whom is all authority" (Ireland) →
  **↓**, `ground = god`: authority is derived from the invoked name.
- **Historical facts are ↓ for how they ground, not for what they say.** "En 1949 … fundó la
  República Popular China" is ↓ (`history`) because the constitution rests its authority on it
  ("La presente Constitución reafirma los frutos de la lucha"); whether the event took place is
  not the annotator's question (*Manifiesto*, pp. 69–71).
- **The enacting formula.** With the subject's title or procedure stated → ✦ `procedure`
  ("through our freely elected representatives, adopt"; "IN OUR CONSTITUENT ASSEMBLY … do HEREBY
  ADOPT"). In the subject's own name, as its will, without procedure ("We, the people of Éire …
  give to ourselves this Constitution"; "proclama su voluntad de") → ✦ `will`, `ground = act`
  (the subject names itself as the source). With the enunciator erased ("this Constitution shall
  be adopted", "se decreta") → **other**, `frame = narrative`, unless a procedure is named
  ("adopted through a nationwide referendum" → ✦).
- **Purpose lists** are other, item by item, even when a purpose presupposes a ground ("to
  recover its originality" presupposes it exists): a presupposition inside a purpose is not
  offered as a ground. If the annotator judges the presupposition to be the point of the clause,
  label ↓ and note it.
- **Mixed clauses** are split (§1). "Cumpliendo el mandato de nuestros pueblos" → ✦ `act`; "con
  la fortaleza de nuestra Pachamama" → ↓ `nature`; "gracias a Dios" → ↓ `god`.
- **Markers** are the exact words of the clause that carry the ground or the frame (the verb, the
  "by virtue of", the "from Whom"). Never write a marker that is not in the text.

### 3.4 Worked examples (claim → operator · frame · ground · why)

- *Taiwan 2005* (one sentence, four claims): the Assembly acts "by virtue of the mandate received"
  from the citizens → **✦** · `procedure` · `act` (a title); "in accordance with the teachings
  bequeathed by" the founder → **↓** · `none` · `spirit` (a founder's teachings as prior
  authority); the "in order to" purposes → **other** · `none` · `none`; "do hereby adopt" → **✦** ·
  `will` · `act`.
- *Azerbaijan 2016*: "continuing the traditions of many centuries of their Statehood" → **↓** ·
  `narrative` · `spirit`. "guided by the principles which are reflected in the Constitutional Act on
  the State Independence" → **✦** · `none` · `act` (a prior inscription). "wishing to provide
  welfare for all" → **other** · `will` · `none`. "being aware of their responsibility before past,
  present, and future generations" → **other** · `attitude` · `none` (a value). "exercise their
  sovereign right by solemnly declaring the following goals" → **✦** · `will` · `act`. Each goal →
  **other**. "this Constitution shall be adopted through a nationwide referendum" → **✦** ·
  `procedure` · `act`.
- *Madagascar 2010* (by paragraph): ¶2, the people "Affirming its belief in" a divinity → **other**
  · `attitude` · `none`. ¶4, "Convinced of the necessity" for society to recover its "Malagasy
  character" and traditional values → **↓** · `attitude` · `spirit`. ¶6, "Convinced that the
  Fokonolona" constitutes a framework of life → **↓** · `attitude` · `spirit`. ¶7, "Persuaded of
  the exceptional importance" of the resources "with which nature has provided" the country → **↓**
  · `attitude` · `nature`. ¶8, "Declaring that" disrespect for the Constitution is the cause of
  "the cyclical crises" → **↓** · `attitude` · `history` (a causal claim about the past as fact).
  ¶9, "making its own" the International Charter and the Conventions → **✦** · `none` · `act`.
  ¶10, "Considering that" the development of personality "is the essential factor" of durable
  development → **↓** · `attitude` · `doctrine`. ¶5, "Conscious that it is indispensable" to
  implement reconciliation → **other** · `attitude` · `none` (a purpose stated as necessary; note
  it — boundary case with `doctrine`).
- *Ireland 2019*: "In the Name of the Most Holy Trinity, from Whom is all authority" → **↓** ·
  `invocation` · `god`. "Humbly acknowledging all our obligations to our Divine Lord, Jesus Christ,
  Who sustained our fathers through centuries of trial" → **↓** · `attitude` · `god`. "Gratefully
  remembering their heroic and unremitting struggle to regain the rightful independence of our
  Nation" → **↓** · `attitude` · `history`. "seeking to promote the common good …" → **other** ·
  `will` · `none`. "We, the people of Éire … Do hereby adopt, enact, and give to ourselves this
  Constitution" → **✦** · `will` · `act`.
- *South Africa 2012*: "Recognise the injustices of our past" → **↓** · `attitude` · `history`.
  "Honour those who suffered for justice and freedom in our land" → **↓** · `attitude` · `history`.
  "Believe that South Africa belongs to all who live in it, united in our diversity" → **other** ·
  `attitude` · `none` (a value; note it). "We therefore, through our freely elected representatives,
  adopt this Constitution as the supreme law of the Republic" → **✦** · `procedure` · `act`. "so as
  to Heal the divisions of the past …" (each item) → **other**. "May God protect our people" →
  **other** · `invocation` · `none`.
- *India 2023*: "WE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a
  SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC" → **✦** · `will` · `act`. "and to secure to all
  its citizens: JUSTICE … LIBERTY … EQUALITY … FRATERNITY" → **other** (purposes). "IN OUR
  CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949, do HEREBY ADOPT, ENACT AND GIVE TO
  OURSELVES THIS CONSTITUTION" → **✦** · `procedure` · `act`.
- *Greece 2019* (the whole preamble): "In the name of the Holy and Consubstantial and Indivisible
  Trinity" → **other** · `invocation` · `none`.
- *Costa Rica 2020 (ES)*: "Nosotros, los Representantes del pueblo de Costa Rica, libremente
  elegidos Diputados a la Asamblea Nacional Constituyente" → **✦** · `procedure` · `act`.
  "invocando el nombre de Dios" → **other** · `invocation` · `none`. "reiterando nuestra fe en la
  Democracia" → **other** · `attitude` · `none`. "decretamos y sancionamos la siguiente" → **✦** ·
  `will` · `act`.
- *Spain 2011 (ES)*: "La Nación española, deseando establecer la justicia, la libertad y la
  seguridad" → **other** · `will` · `none`. "en uso de su soberanía, proclama su voluntad de" →
  **✦** · `will` · `act` (a title and a declared will). Each "Garantizar … Consolidar … Proteger
  …" → **other**. "En consecuencia, las Cortes aprueban y el pueblo español ratifica la siguiente"
  → **✦** · `procedure` · `act`.
- *Bolivia 2009 (ES)*: "En tiempos inmemoriales se erigieron montañas, se desplazaron ríos, se
  formaron lagos" → **↓** · `narrative` · `nature`. "Poblamos esta sagrada Madre Tierra con rostros
  diferentes, y comprendimos desde entonces la pluralidad vigente de todas las cosas" → **↓** ·
  `narrative` · `history`. "El pueblo boliviano … desde la profundidad de la historia, inspirado en
  las luchas del pasado … construimos un nuevo Estado" → **↓** · `narrative` · `history`.
  "Nosotros, mujeres y hombres, a través de la Asamblea Constituyente y con el poder originario del
  pueblo, manifestamos nuestro compromiso" → **✦** · `procedure` · `act`. "Cumpliendo el mandato de
  nuestros pueblos" → **✦** · `none` · `act`; "con la fortaleza de nuestra Pachamama" → **↓** ·
  `none` · `nature`; "gracias a Dios, refundamos Bolivia" → **↓** · `none` · `god`.
- *China 2004 (ES)*: "China es uno de los países de más larga historia del mundo" → **↓** ·
  `narrative` · `history`. "A partir de 1840, la China feudal se fue convirtiendo gradualmente en un
  país semicolonial y semifeudal" → **↓** · `narrative` · `history`. "Las clases explotadas como tal
  han sido eliminadas en nuestro país. Sin embargo, la lucha de clases continuará" → **↓** ·
  `narrative` · `doctrine`. "Taiwán es parte del sagrado territorio de la República Popular China"
  → **↓** · `narrative` · `nature` (a sacralised territory; note it). "La presente Constitución
  reafirma los frutos de la lucha del pueblo chino … es la ley fundamental del Estado y tiene la
  máxima autoridad jurídica" → **↓** · `narrative` · `history` (the constitution rests its authority
  on the struggle). "El pueblo de las diversas nacionalidades … deben tomar la Constitución como
  norma básica de conducta" → **other** · `none` · `none` (an obligation).

The six-operator set (⇒ ⊕ ↓ ∅ ✦ ∥) is recorded as an **exploratory** secondary label and is not
gated in campaign 1. An erased enunciator (`frame = narrative`) is the natural place for ∅.

## 4 · Adjudication and the agreement gate

- Pilot: 100 preambles (`pilot_preamble_100.json`), each annotated independently by 2 annotators
  (a 3rd adjudicates disagreements and records the rule that resolves each one). Rules born in
  adjudication go into v2.1 of this codebook, dated.
- Agreement (decision D18): **primary** — share of naturalised claims per preamble, Krippendorff's
  α (interval); **secondary** — claim-level nominal α on claims aligned by character-offset overlap
  (Jaccard ≥ 0.5), and, once human annotation fixes the segmentation, plain claim-level α on
  `operator`, `ground` and `frame` separately. A preamble-level dominant label is reported only with
  ties as missing.
- Gate (decision D11): **≥ 0.67** to train a task, **≥ 0.80** reported as reliable; below 0.67 the
  task stays LLM-only with a warning label and the result is reported as a finding.
- The main campaign covers the whole population (190 records) with the same rotation.

## 5 · What ↓ and ✦ mean here (for annotators, one paragraph)

Ferraris distinguishes what is *unamendable* — what cannot be corrected by thought alone: the
world, the past — from what is *amendable* — what we know and decide, always correctable
(*Manifiesto*, p. 48). A constitution is a decision. A preamble that rests the decision on nature,
God, history or the spirit of a people presents a decision as if it were part of the unamendable
world; that is naturalisation, and its self-description is the famous "when we act we create our
own reality" (*Manifiesto*, p. 22). A preamble that rests the decision on a mandate, an election, a
referendum or a prior document keeps the decision visible as a decision — anyone can ask who
decided and check the title; that is revelation. Ferraris's own contrast is *foundation according
to the spirit* versus *foundation according to the letter* (*Documentalidad*, pp. 353–355); his
verdict on the first — that it "has never taken place" — is not part of the annotation.

## 6 · Versions

- v0.1 — 2026-09-14 — scaffold.
- v0.2 — 2026-09-14 — worked examples from 17 original-language constitutions (emergency
  provisions); proposed decision rules and boundary cases; output format; adjudication protocol.
- v1.0 — 2026-09-14 — decision rules, decision test ("who says so, and could anyone check?") and
  example readings confirmed by the annotation lead; frozen for the `em` pilot; tag `v1.0.0` →
  Zenodo DOI 10.5281/zenodo.22748195. The `em` campaign was closed as an exploratory study (D20);
  its v1.0 T5 test presupposes a factual trigger separable from the act and is not applicable to
  founding clauses (D21).
- v2.0 — 2026-09-16 — founding inscriptions (preambles) as the unit; T5 reformulated as ground +
  frame + operator with the three-step decision test (§3), grounded in *Documentalidad* (pp. 223,
  333, 353–355, 365–367) and the *Manifiesto* (pp. 22, 48, 63–71, 78–83); worked examples from
  eleven preambles; T2 rules unchanged plus rule 6 and preamble boundary cases; agreement measures
  per D18. Decisions D21–D23.

# Computational-Ontology Model — Project instructions (v0.3, "stabilising the ground")

Anchor source: Jimmy Hernández Marcelo, «La filosofía de la tecnología desde el Nuevo realismo», introductory study to M. Ferraris, *Metafísica de la Web* (Madrid, Dykinson, 2020), pp. 9-33. The three tables in that text (pp. 18, 21 and 29) and the eleven theses of documentality (pp. 22-24) are the frame for everything below.

Changes since v0.2: English is the canonical language of this document and of the stratum names (Record · Enunciation · Mediation); content unchanged.

---

## PART A — Project instructions (text to paste into "Project instructions")

### A.1 Purpose

This project designs, implements and validates a **computational-ontology model** (a semantic-NLP pipeline) that maps *competing realities* in textual corpora without reducing the analysis to sentiment polarity. The philosophical frame is **Maurizio Ferraris's New Realism** (LabOnt, Turin): the ontology/epistemology distinction, unamendability, documentality ("Object = Inscribed Act"), documediality and hysteresis. "Competing realities" are operationalised as **ideological signatures** over one and the same social object (A.2.11, C.4). Markus Gabriel's fields-of-sense realism is used only as an auxiliary resource and is always labelled as such.

### A.2 Design axioms (non-negotiable)

1. **Ontology / epistemology separated in every layer.** Every artefact of the pipeline is tagged with its column of Table 1: *unamendable* (record, inscription, frozen corpus) or *amendable* (model, embedding, cluster, interpretation). An amendable output is never presented as unamendable.
2. **No transcendental fallacy.** It is never claimed that what the model "knows" (embeddings, attention, clusters) determines what *there is* in the corpus. Clusters are conceptual schemes; inscriptions are the world. Every visualisation carries the warning "scheme, not reality".
3. **Mandatory ontological typing of entities** (Table 2): every detected entity is classed as *physical*, *ideal* or *social*, with its three coordinates (space, time, dependence on consciousness). No entity stays untyped.
4. **Nothing social exists outside the text (thesis 6).** The pipeline works on *inscriptions*; what is not inscribed is not a computable social object. No "latent", unattested social objects are inferred. The corpus is an archive of records, not "communication".
5. **The algorithm is thirdness (Table 3).** Technology — this pipeline included — is a *factor of truth* mediating between ontology and epistemology. The project documents its own effects reflexively (which facts it produces, which interpretations it enables); it never presents itself as a neutral mirror.
6. **Emergentist realism.** Competing realities are modelled as *emergence* from many non-programmatic inscriptions (Copernicanism of the Web, point 5), not as deliberate constructions by a subject.
7. **Individuation by signature/style (thesis 11).** The identity of an emitter or a discursive community is tracked through stylometric traits, not only through metadata.
8. **Strong document ≠ weak document (thesis 9).** Inscriptions of acts (constitutions, statutes, rulings, contracts) and records of facts (press, social media, testimony) form separate sub-corpora with separate treatments; they are never mixed in one model without saying so.
9. **Temporality and hysteresis.** Every social object is tracked as a dated trajectory; the persistence of frames after the causal event, and their decay, are measured. There is no purely synchronic analysis.
10. **No interpretability by decree.** No component (attention heads, matrix factors, dimensionality-reduction axes) is declared a "perspective axis" without empirical validation: human annotation, robustness, ablations, contrast with known communities.
11. **Perspectives are inscribed ideologies.** A "perspective" is not a mental state but a social object (thesis 4): an ideological signature recognisable in inscriptions, modelled with Romero's tuple and the hermeneutic operators already defined in the SOCE / *Ideological Architectures* ecosystem (C.4).

### A.3 Canonical vocabulary (always use these terms, in this sense)

| Term | Meaning in this project | Never used as a synonym of… |
|---|---|---|
| **Inscription / record** | A trace accessible to at least two people; the support of a social object | "raw data", "the text itself" |
| **Social object** | An inscribed act involving ≥2 subjects and depending on there being subjects who recognise it | "opinion", "sentiment" |
| **Unamendable** | What cannot be corrected by the mere force of thought (the record as it stands) | "true" |
| **Amendable** | What we know about what exists; correctable; the model and its outputs | "subjective" |
| **Reality** | The domain of individuals (ontology, firstness) | "truth" |
| **Truth** | The domain of objects of knowledge (epistemology, secondness) | "reality" |
| **Interpretation / fact** | The product of technological mediation (thirdness) | "opinion" |
| **Strong document** | The inscription of an *act* (statute, contract, constitution, ruling, promise) | — |
| **Weak document** | The record of a *fact* (news item, post, testimony, log) | — |
| **Community of inscription** | The set of emitters/supports sharing a signature (style + ideological signature) over a social object | "audience", "bubble" |
| **Ideology** | A technology of direction (Romero): the structural tuple I = ⟨C,S,D,G,B,A,P,V,I,O,M⟩ inscribed in documents; a social object | "bias", "political opinion" |
| **Ideological signature** | The pair ⟨ω_I, operator chain⟩ that individuates an ideology over the matrix M = C×S | "party label" |
| **Naturalisation (↓)** | The operator that presents an amendable scheme as unamendable reality ("beliefs wearing the costume of plain facts"; ontological mimicry) | "lie", "disinformation" |
| **Field of sense (Gabriel)** | The domain in which an object appears; auxiliary resource for modelling perspectives | "objective truth", "core truth" |
| **Hysteresis** | Persistence of an event's effects beyond its causes | "trend" |

### A.4 Working rules for Claude in this project

- **Language: multilingual, as Luis asks.** Reply in the language of the message (Spanish, English or Italian; Japanese only on explicit request). Mixed messages get the dominant language. Deliverables are produced in the language Luis names for that deliverable; otherwise in the language of the message. NLP terminology may stay in English in any language; Ferraris's terms are quoted in Italian/Spanish as in the source, with an equivalent in the language of the text. **English is the canonical language of the repository, the code, the model cards and the OSF record.**
- Before proposing any technical component, state (a) which row/column of Tables 1-3 it belongs to and (b) which thesis of documentality justifies or constrains it.
- Never mix Ferraris and Gabriel without marking it: when "field of sense" or *Sinnfeld* is used, prefix "(Gabriel, neutral realism)". Ferraris warns that this realism can revive the idea that man bestows sense on existence (p. 26).
- Never attribute ontological interpretability to attention heads, matrix factors or UMAP/t-SNE axes without explicit empirical validation (axiom 10).
- Every philosophical claim about Ferraris is cited with a page of the anchor PDF or of the original work; without a source it is marked "working hypothesis". The same for Romero, Gabriel and the project's own formalisms (SOCE, *Ideological Architectures*): cite `manifest.json` or the corresponding canonical document.
- Keep the separation between funding calls (SPReAD / MSCA) already established in the SOCE ecosystem: this project is shared infrastructure; no text is imported from one proposal into another.
- At the end of every task: self-audit (errors, unfounded assumptions, corrections) and a record of progress in the project (`claude/…`).
- Consult the official documentation of any platform/library before modifying or recommending it.
- Commits in `computational-ontology/model` are authored by Luis alone: no co-author trailers.

---

## PART B — The frame: the three tables and their computational translation

### Table 1 (p. 18) — Epistemology vs. Ontology → which pipeline layer belongs to which domain

| Ferraris | EPISTEMOLOGY (amendable) | ONTOLOGY (unamendable) |
|---|---|---|
| Science / Experience | linguistic, historical, free, infinite, teleological | not necessarily linguistic, not historical, not necessary, finite, not necessarily teleological |
| Truth / Reality | does not arise from experience; is teleologically oriented towards it | is not naturally oriented towards science |
| Inner / outer world | the conceptual scheme is in the head and speaks about the world → amendable | what is not amendable is in the world and cannot be changed by thought |
| **Pipeline translation** | Models, embeddings, factorisations, clusters, perspective/ideology labels, visualisations, metrics | Frozen corpus (hash, version, date), inscriptions as they stand, record metadata, documentary identity |

Derived rule: the corpus is *frozen* (versioned, checksummed, with provenance) before any modelling; nothing in the modelling writes back into the corpus. The only way to "amend" the corpus is a new inscription (a new version), consistent with thesis 5.

### Table 2 (p. 21) — Types of object → entity typing scheme (ontological NER)

| Type | Space | Time | Consciousness | Corpus examples | Modelling implication |
|---|---|---|---|---|---|
| **Physical** | exists in space | exists in time | independent | rivers, bodies, buildings, artefacts | Stable referents; *anchors* for aligning perspectives (everyone speaks about the same river) |
| **Ideal** | not in space | not in time | independent | numbers, theorems, logical relations | Socialised on publication (thesis 2); modelled as relations, not events |
| **Social** | exists in space | exists in time | **dependent** | statutes, money, promises, institutions, ideologies, "the Constitution", "the people" | Exist only as inscriptions; the objects whose *contested construction* the project is about |

Derived rule: the "Object A" of the original description (an event built into several frames) is almost always a **social object**; its unamendable core is not a "central truth" but the set of **dated inscriptions** that constitute it. Ideologies themselves are social objects of this table.

### Table 3 (p. 29) — Truth-bearers / Truth-makers / Truth-factors → three-stratum architecture

| Ferraris (Peirce) | Domain | Correlate | Unit | **Pipeline stratum** |
|---|---|---|---|---|
| Truth-bearers — *firstness* | Ontology | Reality | Individuals | **E1 · Record**: ingestion, freezing, ontological typing of entities and inscriptions, strong/weak classification |
| Truth-makers — *secondness* | Epistemology | Truth | Objects (relational concepts presupposing subjects) | **E2 · Enunciation**: propositions, claims, frames, stances, ideological signatures, contextual embeddings, temporal trajectory |
| Truth-factors — *thirdness* | Technology | Interpretation | Facts | **E3 · Mediation**: the algorithm itself, the visualisation, the production of "facts" and their reflexive documentation |

Derived rule: thirdness is transversal (a result already established in *Ideological Architectures*: technology is not a fifth subsystem but a transversal cultural product). The pipeline *produces facts* and must record how.

### The eleven theses of documentality as design constraints (pp. 22-24)

| Thesis | Computational constraint / opportunity |
|---|---|
| 1. Ontology catalogues the life-world | The main output is a **catalogue** (individuals → classes → instances), not a score |
| 2. Three types of object | Mandatory typing (Table 2) |
| 3. Ontology ≠ epistemology | Amendable/unamendable tag on every artefact (Table 1) |
| 4. Social objects depend on subjects but are not subjective | "Perspectives" are objective in so far as inscribed: modelled as *communities of inscription* with an ideological signature, not as mental states |
| 5. Object = Inscribed Act | Minimal unit of analysis: the **inscribed act** (who, which act, on which support, when), not the token |
| 6. Nothing social exists outside the text | No inscription, no social entity; inferring "latent" unattested social objects is forbidden |
| 7. Record, not communication | Archive structure (persistence, citability, versions) is privileged over diffusion metrics |
| 8. The mind is a tablet of inscriptions | The hierarchy trace → record → inscription is used as a hierarchy of evidence levels |
| 9. Strong vs. weak documents | Two sub-corpora: acts (performative) and records of facts (constative) |
| 10. The letter is the foundation of spirit | Institutions, art, religion, philosophy and ideologies are analysed as results of inscriptions, never as free-floating "ideas" |
| 11. Individuality shows in the signature | Stylometry module to individuate authors/communities; the ideological signature is its correlate at the level of content |

---

## PART C — Audit of the original text: errors, corrections applied, resulting architecture

### C.1 Register of errors and corrections (closed in v0.2)

| # | Error or weakness in the original text | Correction applied | Where it lives |
|---|---|---|---|
| 1 | Two new realisms conflated: the opening definition and the use of *Sinnfeld* are Gabriel's (neutral realism), not Ferraris's; the PDF (p. 26) records Ferraris's reservation | Ferraris as primary frame; Gabriel as declared, labelled auxiliary | A.1, A.3, A.4 |
| 2 | Layer 1, "ontological tokenisation establishes the independent objects that exist before interpretation": category error — parsing reaches inscriptions (social objects), not independent physical objects | Layer renamed **E1 · Record**; the unamendable item is the record as it stands; minimal unit = inscribed act | A.2.1, A.2.4, B-Table 3, C.2 |
| 3 | Layer 3, "separates core truths from subjective lenses": inverts Table 1 (truth is epistemological and amendable) and contradicts thesis 4 (perspectives are not subjective) | Replaced by **E2 · Enunciation**: objectively inscribed claims, frames and ideological signatures, grouped by community of inscription | A.2.11, A.3, C.2-C.3 |
| 4 | Attributes interpretability to attention heads / matrix factorisation as "viewpoint dimensions" without support | Axiom 10: nothing is a perspective axis without validation (human annotation, robustness, ablations) | A.2.10, C.3 phase 9 |
| 5 | UMAP/t-SNE presented as "the topology of collective reality": unfaithful reductions; reading them that way is the transcendental fallacy | UMAP only as an exploratory view with a warning; topology ⇒ TDA (persistent homology / Mapper); output always tagged amendable | A.2.2, C.3 phase 8 |
| 6 | Omits thirdness: the algorithm is a factor of truth producing facts | **E3 · Mediation**, reflexive; record of produced facts and assumptions | A.2.5, B-Table 3, C.2 |
| 7 | No strong/weak document distinction | Axiom 8; separate sub-corpora; phase 2 classifies them | A.2.8, C.3 phase 2 |
| 8 | Corpus treated as synchronic; no hysteresis | Axiom 9; phase 7 (trajectory and hysteresis) | A.2.9, C.3 phase 7 |
| 9 | "Competing realities" not operationalised | Defined as ideological signatures over one social object, tracked by community of inscription and over time | A.1, A.2.11, C.4 |
| 10 | *Sinnfeld* used as if it were the unit of perspective | Unit of perspective = community of inscription + ideological signature; *field of sense* kept as an auxiliary hypothesis to be tested | A.3, C.4 |

### C.2 Corrected architecture (replaces the original diagram)

```
[ Frozen corpus: dated, versioned inscriptions ]                 ← UNAMENDABLE
            │
            ▼
E1 · RECORD (firstness · ontology · individuals)
   1a. Segmentation into inscribed acts (who / which act / support / date)
   1b. Ontological typing of entities: physical · ideal · social
   1c. Document classification: strong (act) · weak (record of fact)
            │
            ▼
E2 · ENUNCIATION (secondness · epistemology · objects)          ← AMENDABLE
   2a. Contextual embeddings (transformers) tagged as conceptual scheme
   2b. Extraction of claims / frames / stances on each social object
   2c. Ideological signature: projection on M = C×S and operator detection (⇒ ⊕ ↓ ∅ ✦ ∥)
   2d. Grouping by community of inscription (stylometry + ideological signature)
   2e. Time axis: trajectory of each social object; hysteresis measures
            │
            ▼
E3 · MEDIATION (thirdness · technology · facts)                  ← AMENDABLE + REFLEXIVE
   3a. Catalogue of competing realities (the life-world catalogued)
   3b. Visualisation with the warning "scheme, not reality"; TDA if topology is claimed
   3c. Reflexive record: which facts the pipeline produces, under which assumptions, human validation
```

### C.3 Corrected phase table

| Phase | Technical mechanism | Objective in New-Realist terms (Ferraris) | Domain (Table 1) |
|---|---|---|---|
| 1. Freezing the corpus | Versioning, checksum, provenance, date of every inscription | Fix the unamendable: the record as it stands | Unamendable |
| 2. Segmentation into inscribed acts and strong/weak classification | Discourse segmentation + extraction of emitter, act (performative/constative), support, date | Minimal unit = Object = Inscribed Act (theses 5, 9) | Unamendable (identification) / amendable (labels) |
| 3. Ontological typing of entities | NER + physical/ideal/social classifier with Table 2's three coordinates | Catalogue the life-world (theses 1-2) | Amendable |
| 4. Contextual embedding | Multilingual encoders (Spanish/Italian/English) with a context window | Represent the conceptual scheme with which we *know* the record; never the record itself | Amendable |
| 5. Claim and frame extraction | Claim detection, frame/stance classification, argument mining, relations between typed entities | Secondness: objects of knowledge presuppose subjects | Amendable |
| 6. Ideological signature and communities of inscription | Projection on M = C×S; detection of hermeneutic operators; emitter–social object–frame graphs; community detection; stylometry (thesis 11) | Perspectives as social objects, not subjective lenses (thesis 4) | Amendable |
| 7. Temporal trajectory and hysteresis | Series per social object; persistence and decay of frames after the causal event | Effects survive their causes (*Metafísica de la Web*, p. 48) | Amendable |
| 8. Catalogue and visualisation | Structured catalogue; TDA (persistent homology / Mapper) if topology is claimed; UMAP exploratory only | Thirdness: the pipeline produces facts and interpretations and declares it | Amendable + reflexive |
| 9. Validation and reflexive record | Human annotation, robustness, ablations; report of assumptions | Avoid the transcendental fallacy; the model is amendable by design | — |

### C.4 Ideologies: how they enter the model (and what remains to decide)

**Bridging thesis.** In this frame an ideology is a social object (Table 2: in space and time, dependent on subjects) that exists only as inscription (thesis 6) and is individuated by its signature (thesis 11). It is not a "lens" or a "bias": it is a technology of direction (Romero) inscribed in strong and weak documents. The project's "competing realities" are therefore defined as **distinct ideological signatures over one and the same social object**.

**Bridge to Ferraris.** The *naturalisation* operator (↓) of the formal system in *Ideological Architectures* is, in Table 1 terms, the operation that presents an amendable scheme as unamendable reality — exactly the structure of the transcendental fallacy, but performed by a social actor upon a public. *Ontological mimicry* ("beliefs wearing the costume of plain facts", CPSS 2026) is its computational name. The *revelation* operator (✦) is the inverse operation. This turns Table 1 into a detection instrument: measuring how much of what a corpus presents as "fact" is a naturalised inscribed act.

**Formalisms already available in the ecosystem (do not reinvent):**

| Component | Origin | Use in this project |
|---|---|---|
| Tuple I = ⟨C,S,D,G,B,A,P,V,I,O,M⟩ (eleven components) | Romero, *Beyond Nature and Nurture* (Springer 2025); integrated in SOCE | Annotation scheme for the ideological signature per inscribed act |
| Matrix M = C×S (five existential conflicts × four material subsystems) | *Ideological Architectures* (`manifest.json` as single source of truth) | Space onto which claims are projected (phase 6) |
| Six hermeneutic operators ⇒ ⊕ ↓ ∅ ✦ ∥ | *Ideological Architectures* | Operation labels detectable in text; ↓ and ✦ connect with Table 1 |
| Ideological signature ⟨ω_I, operator chain⟩ | *Ideological Architectures* | Identifier of a competing "reality"; ω alone is insufficient (Accelerationism/Degrowth case) |
| Structural signature Φ = ⟨σ,V,E⟩ and topological families (τ₁, τ₂, τ₃, bridge, isolated) | SOCE | System level: how signatures assemble into an exclusion cycle; topological invariance (MAGA/MORENA) as a prediction to test |
| OWL/RDF/SKOS ontology of the CPSS 2026 paper | github.com/Luisbourguet/ideology-ontology | Formal vocabulary for the catalogue (E3) and for auditing LLMs as *emitters* of inscriptions |

**Open decisions (non-blocking):**

- Relation between "community of inscription", "ideological family" (eleven profiles) and "field of sense" (Gabriel): working hypothesis — the community of inscription is the empirical unit; the ideological family its class; the field of sense an auxiliary philosophical reading to be tested against data, not a unit of the pipeline.
- Granularity of operator detection: inscribed act, document or community? Initial proposal: inscribed act, aggregating upwards.
- LLMs as emitters: since the CPSS 2026 paper audits language models by perspective, this pipeline must be able to treat an LLM's output as an inscription (weak document, emitter = model, date = run) and apply the same ideological signature to it.
- Pilot corpus, stack and compute are decided in `plan.md` (D1–D3, §3, §5b).

---

## PART D — Self-audit of this document (v0.3)

- The anchor text is an introductory study by Hernández Marcelo, not a work by Ferraris; page citations refer to that study and, where relevant, to the original work cited in its notes. Before publishing, check against *Documentalità* (2009), *Manifesto del nuovo realismo* (2012) and *Metafisica della Web* (2020).
- Reading Tables 1-3 as pipeline strata is the project's own translation, not something Ferraris asserts; it stands as a working hypothesis.
- The bridge "naturalisation (↓) = the transcendental fallacy performed socially" is a **new theoretical proposal** of this document, not a published result; treat it as a conjecture until written up in an article and checked against Ferraris's text on the fallacy (*Il mondo esterno*, pp. 19-20, per the PDF).
- The C.4 components (Romero's tuple, matrix, operators, Φ, topological families) are cited according to the recorded state of the SOCE / *Ideological Architectures* ecosystem; if `manifest.json` or the codebook have changed, those canonical documents prevail.
- The relation between "field of sense" (Gabriel) and "community of inscription" (derived from Ferraris) is still unresolved; they may coincide operationally, but they should be kept separate until there is data. (Recommendation kept from v0.1; the C.4 working hypothesis does not close it.)
- The stack remains as verified in `plan.md` §3 (rule A.4).
- English terms for Ferraris's *emendabile / inemendabile*: this document uses *amendable / unamendable*, following the SUNY Press translation of the *Manifesto*; earlier drafts used "emendable / in-emendable" — the two are synonyms here, and the repository code keeps `emendable` as the field name.

# New-Realism Analyzer

Computational-ontology model for mapping *competing realities* in constitutional texts, built on Maurizio Ferraris's New Realism (ontology ≠ epistemology; documentality: *Object = Inscribed Act*). Part of the [Computational Ontology](https://computational-ontology.com/) ecosystem alongside `soce`, `constitutionsplus` and `herder-companion`.

The analyzer takes a text and returns a structured breakdown in three strata:

| Stratum | Ferraris / Peirce | What it produces |
|---|---|---|
| **E1 · Record** | firstness · ontology | the frozen inscription; inscribed acts; entities typed *physical / ideal / social*; document type |
| **E2 · Enunciation** | secondness · epistemology | claims and frames; the **operator** on each claim (↓ naturalised · ✦ revealed · other); ideological signature |
| **E3 · Mediation** | thirdness · technology | the card, a JSON-LD export against the project ontology, and a reflexive log (model version, date) |

Every model output is labelled **emendable** and carries a model hash and a date; the frozen input is the only **in-emendable** item and is never rewritten.

## Status

Sprint 0 (Sept–Oct 2026): repository skeleton, codebook v1.0 (emergency provisions, exploratory) and v2.0 (preambles), frozen corpus snapshots. See [`docs/plan.md`](docs/plan.md) for the full plan, timeline and preregistration skeleton, and [`docs/project-instructions.md`](docs/project-instructions.md) for the axioms, the three tables and the canonical vocabulary.

Pilot corpus: **emergency provisions** (Constitute topic key `em`) across in-force constitutions, English first, Spanish originals second.

## Layout

```
codebook/     annotation manual (CC BY 4.0) — the document that gets frozen and DOI'd first
ontology/     OWL / SKOS vocabulary used by the JSON-LD export (CC BY 4.0)
data/         NOT the texts (see data/README.md) — snapshot manifest, hashes, annotations keyed to constitution id + section id
docs/         plan, project instructions, datasheet and model cards
notebooks/    Kaggle / Colab notebooks (bake-off, fine-tuning), exported here after each run
src/nra/      pipeline code (fetch, freeze, E1–E3, evaluation)
tests/
```

## Licences

- Code (`src/`, `tests/`, `notebooks/`): **Apache License 2.0** — [`LICENSE`](LICENSE)
- Codebook, ontology and documentation (`codebook/`, `ontology/`, `docs/`): **CC BY 4.0** — [`LICENSE-DOCS`](LICENSE-DOCS)
- Constitutional texts are **not distributed** here. See [`NOTICE`](NOTICE).

## Open science

GitHub releases are archived on Zenodo under one concept DOI (`CITATION.cff` carries the metadata); the annotation study is preregistered on OSF before annotation starts; models and dataset cards go to the Hugging Face Hub with a Zenodo mirror. Enforced order: freeze codebook → Zenodo DOI → seal OSF → run.

## Citation

See [`CITATION.cff`](CITATION.cff). Constitute texts must be cited as: Elkins, Zachary, Tom Ginsburg, James Melton. *Constitute: The World's Constitutions to Read, Search, and Compare.* constituteproject.org.

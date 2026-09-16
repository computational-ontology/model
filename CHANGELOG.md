# Changelog

## 2.0.0 — 2026-09-16
- Codebook v2.0: founding inscriptions (preambles) as the unit (D20–D21); T5 reformulated as
  ground + frame + operator with a three-step decision test; worked examples from eleven preambles;
  T2 unchanged (+ rule 6 on references to inscriptions).
- `nra.schema`: `Claim.frame` and `Claim.ground` (D22), required by the decoder grammar, defaulting
  to `none` so v1.0 records still validate; `CODEBOOK_VERSION = "2.0"`; schema JSON regenerated.
- Project instructions v0.4: the ↓ / transcendental-fallacy bridge reformulated as a mirror image
  (D23); E3 grounded in *Manifiesto* pp. 78–99; vocabulary entries for ground, frame, natural.

## 0.0.1 — 2026-09-14
- Repository skeleton: licences (Apache-2.0 code, CC BY 4.0 docs), NOTICE on Constitute CC BY-NC texts, CITATION.cff, CI.
- Plan (`docs/plan.md`) and project instructions (`docs/project-instructions.md`).
- Codebook v0.1 scaffold (T2 entity typing, T5 operator with three labels).
- `nra.manifest` / `nra.fetch`: snapshot manifest (hashes only) and Constitute fetcher on documented endpoints.

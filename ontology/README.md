# ontology/

Licence: CC BY 4.0.

Vocabulary used by the analyzer's JSON-LD export (E3), serialised with `rdflib` (`format="json-ld"`). It extends the computational ontology of ideologies (`Luisbourguet/ideology-ontology`, OWL/RDF/SKOS) with the New-Realist classes needed here:

- `nr:Inscription` (the frozen record; in-emendable), `nr:InscribedAct` (who · act · support · date)
- `nr:PhysicalObject`, `nr:IdealObject`, `nr:SocialObject` (Ferraris's three types, with the three coordinates as datatype properties)
- `nr:Claim` with `nr:operator` ∈ {`nr:Naturalised`, `nr:Revealed`, `nr:Other`} (and the six-operator vocabulary as SKOS concepts)
- `nr:emendable` / `nr:inEmendable` provenance flags; `nr:modelVersion`, `nr:producedAt` on every model output (the reflexive log)

Files (to be added in S0–S1): `nr.ttl` (Turtle), `context.jsonld`, and the JSON Schema derived from them that constrains the Stage 1 LLM output.

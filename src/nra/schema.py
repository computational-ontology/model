"""Stage 1 output schema — what a model (or a human) says about one section.

Two layers, kept apart on purpose:

* ``Stage1Output`` is the *only* thing the model emits: T2 mentions, T5 claims, notes. It is
  the JSON Schema handed to the constrained decoder. No ids, no dates — the model cannot get
  those wrong if it never produces them.
* ``Stage1Record`` is the envelope the harness wraps around it: which section (by id + hash,
  never by text), which emitter, when, under which codebook and prompt version. This is the
  line written to the JSONL file and, later, published as an annotation.

Placement in the project tables: the record is an inscription of an *act of labelling*
(thesis 5: who / what act / support / date) and, when the emitter is a model, a weak document
(thesis 9). Everything in it is *amendable* (Table 1); the section it points to is not.

Field semantics follow codebook/README.md v2.0 §1 (output format), §2 (T2) and §3 (T5).

v2.0 (decisions D21, D22): a claim carries, besides its operator, the *frame* through which the
enunciator relates it to itself and the *ground* the clause makes the founding act rest on. The
operator is decided from the ground (codebook §3); v1.0 records, which have neither field, still
validate (both default to ``none``) but the decoder requires them.
"""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

CODEBOOK_VERSION = "2.0"


class EntityType(str, Enum):
    """Codebook §2, Ferraris's three object types (Hernández Marcelo 2020, p. 21)."""

    physical = "physical"
    ideal = "ideal"
    social = "social"


class Operator(str, Enum):
    """Codebook §3, the three campaign-1 labels (decision D2)."""

    naturalised = "naturalised"  # ↓
    revealed = "revealed"  # ✦
    other = "other"


class SecondaryOperator(str, Enum):
    """Exploratory six-operator set (⇒ ⊕ ↓ ∅ ✦ ∥); not gated in campaign 1."""

    implication = "implication"  # ⇒
    aggregation = "aggregation"  # ⊕
    naturalisation = "naturalisation"  # ↓
    erasure = "erasure"  # ∅
    revelation = "revelation"  # ✦
    parallel = "parallel"  # ∥


class Frame(str, Enum):
    """Codebook v2.0 §3: how the enunciator relates the clause to itself (constative layer)."""

    attitude = "attitude"  # convinced that, recognising, conscious of, affirming its belief
    will = "will"  # wishing, desiring, resolved to, proclaims its will, do hereby adopt
    procedure = "procedure"  # through elected representatives, by referendum, in Constituent Assembly
    invocation = "invocation"  # in the name of
    narrative = "narrative"  # bare third-person statement, enunciator erased
    none = "none"  # purpose lists, definitions, obligations — no framing of the enunciator


class Ground(str, Enum):
    """Codebook v2.0 §3: what the clause makes the founding act rest on (performative layer)."""

    nature = "nature"  # territory, resources, human nature, "sacred" land
    history = "history"  # past events and struggles stated as facts
    god = "god"  # a divinity as source of authority or as fact
    spirit = "spirit"  # the people, nation, tradition, character, roots presented as prior to the act
    doctrine = "doctrine"  # a general truth or theory asserted (class struggle, development, essence)
    act = "act"  # a procedure, mandate, election, referendum, prior inscription, the subject's own decision
    none = "none"  # no ground offered (bare performative, purpose, value, faith, obligation)


NATURALISING_GROUNDS = frozenset({Ground.nature, Ground.history, Ground.god, Ground.spirit, Ground.doctrine})


class Mention(BaseModel):
    """One entity mention, typed as used in the clause (codebook §2, rule 1)."""

    model_config = ConfigDict(extra="forbid")

    mention: str = Field(min_length=1, description="Verbatim span from the section text.")
    type: EntityType


class Claim(BaseModel):
    """One claim and how it presents what it asserts (codebook §3)."""

    model_config = ConfigDict(extra="forbid")

    claim: str = Field(min_length=1, description="Verbatim clause from the section text.")
    operator: Operator
    markers: list[str] = Field(
        default_factory=list,
        description="Verbatim words that triggered the label ('if the President is satisfied', 'en caso de').",
    )
    frame: Frame = Field(default=Frame.none, description="How the enunciator relates the clause to itself (v2.0).")
    ground: Ground = Field(default=Ground.none, description="What the clause makes the founding act rest on (v2.0).")
    secondary: SecondaryOperator | None = Field(
        default=None, description="Exploratory six-operator label; may be null."
    )


class Stage1Output(BaseModel):
    """What the model emits for one section. Nothing else."""

    model_config = ConfigDict(extra="forbid")

    t2: list[Mention] = Field(description="Every entity mention in the section, each typed.")
    t5: list[Claim] = Field(min_length=1, description="Every claim in the section, each labelled.")
    notes: str = Field(default="", description="Doubts, in one or two sentences; empty if none.")

    @classmethod
    def json_schema_for_decoder(cls) -> dict:
        """Strict JSON Schema for constrained decoding (enums inlined, no defaults, no titles)."""
        schema = cls.model_json_schema(mode="serialization")
        _strip(schema)
        # every key is required for the decoder, so all emitters produce the same shape
        schema["required"] = ["t2", "t5", "notes"]
        schema["$defs"]["Claim"]["required"] = ["claim", "operator", "markers", "frame", "ground", "secondary"]
        return schema


class Stage1Record(BaseModel):
    """The envelope: one JSONL line. Keys align with codebook §1 plus provenance."""

    model_config = ConfigDict(extra="forbid")

    constitution_id: str
    section_id: str
    lang: Literal["en", "es"]
    sha256: str = Field(min_length=64, max_length=64, description="Hash of the section text, from the manifest.")
    annotator: str = Field(description="Human annotator id, or the model id for a machine emitter.")
    emitter_kind: Literal["human", "model"]
    emitted_at: datetime
    codebook_version: str = CODEBOOK_VERSION
    prompt_version: str | None = Field(default=None, description="Prompt file hash/tag; null for humans.")
    decoding: dict[str, str | int | float | bool] | None = Field(
        default=None, description="seed, temperature, max_new_tokens, decoder — null for humans."
    )
    output: Stage1Output
    parse_ok: bool = True
    verbatim_ok: bool | None = Field(
        default=None, description="Set by the harness after checking every span is a substring of the text."
    )

    @field_validator("emitted_at")
    @classmethod
    def _aware(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("emitted_at must be timezone-aware")
        return v


def check_verbatim(output: Stage1Output, text: str) -> list[str]:
    """Return the spans (mentions, claims, markers) that are not substrings of the section text."""
    bad: list[str] = []
    for m in output.t2:
        if m.mention not in text:
            bad.append(m.mention)
    for c in output.t5:
        if c.claim not in text:
            bad.append(c.claim)
        bad.extend(mk for mk in c.markers if mk not in text)
    return bad


def _strip(node: object) -> None:
    """Remove keys that confuse grammar-based decoders and inline nothing else."""
    if isinstance(node, dict):
        for k in ("title", "default", "description"):
            node.pop(k, None)
        for v in node.values():
            _strip(v)
    elif isinstance(node, list):
        for v in node:
            _strip(v)


def export_schema(path: Path) -> None:
    path.write_text(json.dumps(Stage1Output.json_schema_for_decoder(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    export_schema(Path("schema/stage1_output.schema.json"))
    print(json.dumps(Stage1Output.json_schema_for_decoder(), indent=2, ensure_ascii=False))

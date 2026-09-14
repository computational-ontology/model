import json
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from nra.schema import Stage1Output, Stage1Record, check_verbatim

TEXT = "In case of actual invasion, the Government may take whatever steps they may consider necessary."

GOOD = {
    "t2": [{"mention": "actual invasion", "type": "physical"}, {"mention": "the Government", "type": "social"}],
    "t5": [
        {"claim": "In case of actual invasion", "operator": "naturalised", "markers": ["In case of"]},
        {
            "claim": "the Government may take whatever steps they may consider necessary",
            "operator": "revealed",
            "markers": ["may take", "may consider"],
            "secondary": "revelation",
        },
    ],
    "notes": "",
}


def test_valid_output_round_trips():
    out = Stage1Output.model_validate(GOOD)
    assert out.t5[0].operator.value == "naturalised"
    assert check_verbatim(out, TEXT) == []


def test_rejects_unknown_label_and_extra_keys():
    bad = json.loads(json.dumps(GOOD))
    bad["t5"][0]["operator"] = "naturalized"  # not in the enum
    with pytest.raises(ValidationError):
        Stage1Output.model_validate(bad)
    bad = json.loads(json.dumps(GOOD))
    bad["t2"][0]["confidence"] = 0.9  # models must not invent fields
    with pytest.raises(ValidationError):
        Stage1Output.model_validate(bad)


def test_t5_must_not_be_empty():
    with pytest.raises(ValidationError):
        Stage1Output.model_validate({"t2": [], "t5": [], "notes": ""})


def test_verbatim_check_flags_paraphrase():
    out = Stage1Output.model_validate(GOOD)
    out.t5[0].claim = "In the event of an invasion"
    assert check_verbatim(out, TEXT) == ["In the event of an invasion"]


def test_decoder_schema_is_strict_and_clean():
    s = Stage1Output.json_schema_for_decoder()
    assert s["additionalProperties"] is False
    assert set(s["required"]) >= {"t2", "t5"}
    dumped = json.dumps(s)
    assert '"title"' not in dumped and '"default"' not in dumped and '"description"' not in dumped
    assert s["$defs"]["Operator"]["enum"] == ["naturalised", "revealed", "other"]
    assert s["$defs"]["EntityType"]["enum"] == ["physical", "ideal", "social"]


def test_record_requires_aware_timestamp():
    base = dict(
        constitution_id="Ireland_2019", section_id="12345", lang="en", sha256="0" * 64,
        annotator="google/gemma-4-12B-it", emitter_kind="model", output=GOOD,
    )
    with pytest.raises(ValidationError):
        Stage1Record.model_validate({**base, "emitted_at": datetime(2026, 9, 14, 12, 0)})  # noqa: DTZ001 — naive on purpose
    rec = Stage1Record.model_validate({**base, "emitted_at": datetime(2026, 9, 14, 12, 0, tzinfo=timezone.utc)})
    assert rec.codebook_version == "1.0" and rec.verbatim_ok is None

"""Preamble corpus filter and pilot draw (synthetic manifest rows, no text)."""

from nra.preamble import is_preamble, length_band, stratified_pilot


def row(cid, lang="en", n=1000, article="Preamble", header="", sid="1"):
    return {"constitution_id": cid, "section_id": sid, "lang": lang, "n_chars": n, "article": article,
            "header": header, "sha256": "0" * 64, "topic_keys": ["preamble"]}


def test_is_preamble_filter():
    assert is_preamble(row("A"))
    assert is_preamble(row("B", lang="es", article="PREÁMBULO"))
    assert is_preamble(row("C", article="Preamble", header="Preamble"))
    assert is_preamble(row("D", article="", header="Preamble"))  # Bahrain-style: name only in the header
    assert not is_preamble(row("UK", article="Preamble", header="Magna Carta 1297"))  # statute inside a compilation
    assert not is_preamble(row("CA", article="CONSTITUTION ACT 1867", header="CONSTITUTION ACT 1867 > VII"))
    assert not is_preamble(row("TV", article="", header="SCHEDULE 1 (Section 4)"))


def test_length_bands():
    assert [length_band(n) for n in (0, 599, 600, 1999, 2000, 50000)] == ["short", "short", "medium", "medium", "long", "long"]


def test_pilot_is_deterministic_and_capped():
    rows = [row(f"C{i}", lang="en" if i % 4 else "es", n=300 + 40 * i) for i in range(60)]
    a = stratified_pilot(rows, n=30, seed=1)
    b = stratified_pilot(rows, n=30, seed=1)
    assert a == b and len(a) == 30
    assert len(stratified_pilot(rows, n=500, seed=1)) == 60  # never more than the population
    assert {r["length_band"] for r in a} <= {"short", "medium", "long"}

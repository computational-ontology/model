from datetime import date

from nra.manifest import SectionRecord, SnapshotManifest, sha256_text


def test_hash_is_stable_under_nfc_and_whitespace():
    a = sha256_text("  Artículo 29.\n")
    b = sha256_text("Artículo 29.")  # decomposed accent, no whitespace
    assert a == b


def test_manifest_roundtrip(tmp_path):
    m = SnapshotManifest(
        dump_date=date(2026, 9, 14),
        query={"key": "em", "lang": "en", "in_force": "true"},
        sections=[
            SectionRecord(
                constitution_id="Mexico_2015",
                section_id="s123",
                lang="en",
                topic_keys=["em"],
                sha256=sha256_text("SECRET-CLAUSE-TEXT"),
                n_chars=1,
            )
        ],
    )
    p = tmp_path / "m.json"
    m.save(p)
    assert SnapshotManifest.load(p) == m
    assert "SECRET-CLAUSE-TEXT" not in p.read_text()  # the manifest never contains text

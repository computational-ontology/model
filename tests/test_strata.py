from nra.strata import chapter_type, stratified_pilot, structural_path


def test_structural_path_drops_article_numbers():
    assert structural_path("PART 1 > CHAPTER I. RIGHTS > Article 23 > 1") == "CHAPTER I. RIGHTS"
    assert structural_path("Artículo 29") == ""
    assert structural_path("") == ""


def test_rule_order_emergency_before_rights():
    assert chapter_type("TITLE VII. GUARANTEES OF THE CONSTITUTION AND THE STATE OF EMERGENCY") == "emergency/defence chapter"
    assert chapter_type("CHAPTER II. FUNDAMENTAL RIGHTS > Article 15") == "rights catalogue"
    assert chapter_type("Chapter IV. Verkhovna Rada of Ukraine > Article 83") == "legislature"
    assert chapter_type("CHAPTER XIV. ALTERATION OF THE CONSTITUTION") == "judiciary / review / amendment"
    assert chapter_type("Part III") == "no heading"
    assert chapter_type("X. Finance") == "other"


def test_pilot_is_deterministic_and_stratified():
    rows = []
    for i in range(300):
        ct = ["CHAPTER I. STATE OF EMERGENCY", "CHAPTER II. RIGHTS", "CHAPTER III. THE PRESIDENT"][i % 3]
        rows.append({"constitution_id": f"C{i % 40}", "section_id": str(i), "lang": "en" if i % 4 else "es",
                     "header": ct, "sha256": "0" * 64})
    a = stratified_pilot(rows, n=30, seed=1)
    b = stratified_pilot(rows, n=30, seed=1)
    assert a == b and len(a) == 30
    assert len({(p["constitution_id"], p["section_id"]) for p in a}) == 30
    assert {p["chapter_type"] for p in a} == {"emergency/defence chapter", "rights catalogue", "executive/organisation of powers"}
    assert all(set(p) == {"constitution_id", "section_id", "lang", "chapter_type", "header", "article", "sha256"} for p in a)

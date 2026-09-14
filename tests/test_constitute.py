"""Parser tests on a synthetic snippet that mirrors the live API structure (no real text)."""

from nra.constitute import parse_result, parse_topic_search

SNIPPET = """
<div data-id="section/470" data-next-id="" class="section _result _result-title" data-topics="em">
<h4 class="article-header"><a class="article-header__link header-parts" href="/constitution/X_2000?lang=en#s471">
<span class="article-breadcrumb ng-binding ng-scope">Chapter IX.&nbsp;&nbsp;Emergency&nbsp;&gt;&nbsp;Article 9</span></a></h4>
<p class="content">Article 143</p>
<div data-id="section/471" data-next-id="" class="section _result _result-body">
<p class="content">FIRST PARAGRAPH.</p>
<div data-id="section/476" data-next-id="section/478" class="section _result _result-list _result-st-olist" style="display: list-item; margin-left: 3em; list-style-type: '1. '">ITEM ONE;</div>
<div data-id="section/478" data-next-id="" class="section _result _result-list _result-st-olist" style="list-style-type: '2. '" data-topics="em">ITEM TWO.</div>
</div>
</div>
"""


def test_parse_result_structure():
    s = parse_result(SNIPPET)
    assert s.section_id == "470"
    assert s.header == "Chapter IX. Emergency > Article 9"
    assert s.article == "Article 143"
    assert s.text.split("\n") == ["FIRST PARAGRAPH.", "1. ITEM ONE;", "2. ITEM TWO."]
    assert s.topic_hits == ["em"]


def test_parse_topic_search_payload():
    payload = {"X_2000": {"num_results": 1, "public": True, "results": [SNIPPET]}}
    out = parse_topic_search(payload, "X_2000")
    assert len(out) == 1 and out[0].section_id == "470"
    assert parse_topic_search(payload, "Y_1999") == []

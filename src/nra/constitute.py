"""Parsing of Constitute API responses.

`sectionstopicsearch` returns, per constitution id, a dict with `num_results`, `public` and
`results`: a list of HTML snippets. Each snippet is one matched section:

    <div data-id="section/470" class="section _result _result-title" data-topics="em">
      <h4 class="article-header"> ... <span class="article-breadcrumb">Chapter IX.  State of Emergency</span> ... </h4>
      <p class="content">Article 143</p>
      <div data-id="section/471" class="section _result _result-body">
        <p class="content">If because of war, ...</p>
        <div data-id="section/476" class="section _result _result-list ..." style="... list-style-type: '1. '">Clause two of Article 27;</div>
      </div>
    </div>

Shape observed live on 2026-09-14 (Afghanistan_2004, key=em, lang=en). Only the structure is
relied upon here; no constitutional text is stored in this repository.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup, Tag

_LIST_MARK = re.compile(r"list-style-type:\s*'([^']*)'")


@dataclass
class Section:
    section_id: str  # e.g. "470" (from data-id="section/470")
    header: str  # breadcrumb, e.g. "Chapter IX. State of Emergency > Article 64"
    article: str  # e.g. "Article 143" when present, else ""
    text: str  # normalised plain text of the body, list items prefixed with their markers
    topic_hits: list[str] = field(default_factory=list)  # data-topics values found inside


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def _body_text(node: Tag) -> list[str]:
    """Walk the body in document order; paragraphs and list items become lines."""
    lines: list[str] = []
    for el in node.descendants:
        if not isinstance(el, Tag):
            continue
        classes = el.get("class") or []
        if el.name == "p" and "content" in classes:
            t = _clean(el.get_text(" "))
            if t:
                lines.append(t)
        elif el.name == "div" and "_result-list" in classes:
            own = "".join(str(c) for c in el.contents if not isinstance(c, Tag))
            t = _clean(BeautifulSoup(own, "html.parser").get_text(" "))
            m = _LIST_MARK.search(el.get("style", "") or "")
            mark = m.group(1).strip() if m else ""
            if t:
                lines.append(f"{mark} {t}".strip())
    return lines


def parse_result(html: str) -> Section:
    soup = BeautifulSoup(html, "html.parser")
    outer = soup.find("div", attrs={"data-id": True})
    if outer is None:
        raise ValueError("no section div in result")
    sid = str(outer["data-id"]).split("/", 1)[-1]
    crumb = outer.find("span", class_="article-breadcrumb")
    header = _clean(crumb.get_text(" ")) if crumb else ""
    header = header.replace(" > ", " > ").replace("&gt;", ">")
    article = ""
    for child in outer.children:
        if isinstance(child, Tag) and child.name == "p" and "content" in (child.get("class") or []):
            article = _clean(child.get_text(" "))
            break
    body = outer.find("div", class_="_result-body") or outer
    lines = _body_text(body)
    tagged = [outer] if outer.has_attr("data-topics") else []
    tagged += outer.find_all(attrs={"data-topics": True})
    topics = sorted({str(t["data-topics"]) for t in tagged})
    return Section(section_id=sid, header=header, article=article, text="\n".join(lines), topic_hits=topics)


def parse_topic_search(payload: dict, cons_id: str) -> list[Section]:
    """Parse the JSON body of sectionstopicsearch for one constitution."""
    entry = payload.get(cons_id) or {}
    return [parse_result(h) for h in entry.get("results", [])]

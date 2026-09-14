"""Chapter-type strata for the `em` corpus (classifier v3) and the stratified pilot draw.

The breadcrumb delivered by Constitute ("PART 1 > CHAPTER I. RIGHTS > Article 23 > 1")
is reduced to its *structural* levels (article numbers and bare numerals dropped) and the
whole path is matched against ordered keyword rules. Order matters: the emergency rule
runs first so that "Guarantees of the Constitution and the Emergency" is not captured by
the rights rule. This is an *amendable* heuristic (a scheme, not the record); its residual
("other") is reported, never hidden.
"""

from __future__ import annotations

import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

CHAPTER_TYPES = [
    "emergency/defence chapter",
    "rights catalogue",
    "legislature",
    "judiciary / review / amendment",
    "executive/organisation of powers",
    "general / final provisions",
    "other",
    "no heading",
]

_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("emergency/defence chapter",
     re.compile(r"emergenc|exception|excepci|siege|sitio|defen[cs]|urgenc|extraordinar|\bwar\b|guerra|"
                r"crisis|martial|marcial|conmoci|calamid|catastro|disaster|securit|seguridad|\bpeace\b|\bpaz\b|armed forces|fuerzas armadas")),
    ("rights catalogue",
     re.compile(r"right|freedom|derecho|libertad|garant|individual|citizen|ciudadan|persona|dignit|"
                r"human|humano|liberties|civil|fundamental|bill of|declaration|declaraci")),
    ("legislature",
     re.compile(r"parliament|legislat|assembl|congres|senado|senate|c[aá]mara|chamber|national council|"
                r"diet|majlis|jirga|riigikogu|sejm|seimas|saeima|storting|folketing|riksdag|cortes|"
                r"knesset|duma|oireachtas|house of|bundestag|bundesrat|deputies|diputados|verkhovna rada|kurultai|dewan|"
                r"representative council|olbiil|jatiya|lok sabha|rajya sabha|majlis|shura|milli|legislaci[oó]n|opposition|oposici")),
    ("judiciary / review / amendment",
     re.compile(r"judic|court|tribunal|corte|review|revision|revisi[oó]n|reform|amend|enmienda|"
                r"supremacy|supremac|interpretation|interpretaci|constitutional guarantees|garant[ií]as constitucionales|"
                r"alteration|change of the constitution|constitutionality|constitucionalidad|legality|legalidad")),
    ("executive/organisation of powers",
     re.compile(r"president|executive|ejecutiv|government|gobierno|power|poder|instrument|authorit|"
                r"state power|organi[sz]ation of the state|organizaci[oó]n del estado|branches|king|crown|"
                r"monarch|head of state|jefe|cabinet|minister|ministr|administration|administraci|"
                r"structure of the state|estructura del estado|the state\b|el estado|the union|the federation|"
                r"federal|federaci|l[aä]nder|ruling system|the nation|la naci[oó]n|prime|council of|consejo|"
                r"public authorities|autoridades|emir|sultan|prince|regime|r[eé]gimen|institutions|instituciones|"
                r"organi[sz]ation and functions|organs|órganos|sovereign|soberan|territor|state of the|republic|rep[uú]blica|"
                r"presidency|royalty|realeza|throne")),
    ("general / final provisions",
     re.compile(r"general|final|miscellan|transitional|transitor|provisions|disposiciones|foundation|"
                r"principles|principios|preliminar|basic|b[aá]sic|fundamental principles|specific rules")),
]

_ORD = r"(?:[\divxlc]+[a-z]?|one|two|three|four|five|six|first|second|third|fourth|fifth|sixth|uno|dos|tres|primero|segundo|tercero|primera|segunda|tercera)"
_DROP = re.compile(
    r"^(article|art\.?|artículo|section|sec\.?|§|clause|paragraph|párrafo|num\.?|part|parte|title|título|titulo|chapter|capítulo|capitulo)?\s*"
    + _ORD + r"\.?:?$|^\W*$",
    re.I,
)


def structural_path(header: str) -> str:
    """Keep breadcrumb levels that name a division; drop article numbers and bare numerals."""
    parts = [p.strip() for p in (header or "").split(">")]
    keep = [p for p in parts if p and not _DROP.match(p)]
    return " > ".join(keep)


def chapter_type(header: str) -> str:
    path = structural_path(header).lower()
    if not path:
        return "no heading"
    for label, rx in _RULES:
        if rx.search(path):
            return label
    return "other"


def load_rows(data_dir: Path) -> list[dict]:
    rows: list[dict] = []
    for lang in ("en", "es"):
        p = data_dir / f"snapshot_manifest_{lang}.json"
        if p.exists():
            rows += json.loads(p.read_text(encoding="utf-8"))["sections"]
    return rows


def stratified_pilot(rows: list[dict], n: int = 100, seed: int = 20260914, min_per_stratum: int = 3) -> list[dict]:
    """Draw n sections stratified by (chapter_type, lang), proportional with a floor per stratum.

    Deterministic given the seed. Returns records with ids only (no text): the split is
    committed to the repository; the texts are fetched from the snapshot.
    """
    rng = random.Random(seed)
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rows:
        groups[(chapter_type(r.get("header", "")), r["lang"])].append(r)
    total = len(rows)
    alloc = {k: max(min_per_stratum, round(n * len(v) / total)) for k, v in groups.items()}
    alloc = {k: min(a, len(groups[k])) for k, a in alloc.items()}
    # trim / top up to exactly n, largest strata first
    order = sorted(groups, key=lambda k: -len(groups[k]))
    while sum(alloc.values()) > n:
        for k in order:
            if alloc[k] > min_per_stratum and sum(alloc.values()) > n:
                alloc[k] -= 1
    while sum(alloc.values()) < n:
        for k in order:
            if alloc[k] < len(groups[k]) and sum(alloc.values()) < n:
                alloc[k] += 1
    out: list[dict] = []
    for k in order:
        pool = sorted(groups[k], key=lambda r: (r["constitution_id"], r["section_id"]))
        for r in rng.sample(pool, alloc[k]):
            out.append({
                "constitution_id": r["constitution_id"], "section_id": r["section_id"], "lang": r["lang"],
                "chapter_type": k[0], "header": r.get("header", ""), "article": r.get("article", ""),
                "sha256": r["sha256"],
            })
    return out


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Report chapter-type strata and draw the stratified pilot.")
    ap.add_argument("--data", type=Path, default=Path("data"))
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20260914)
    ap.add_argument("--out", type=Path, default=Path("data/splits/pilot_100.json"))
    a = ap.parse_args(argv)
    rows = load_rows(a.data)
    types = [chapter_type(r.get("header", "")) for r in rows]
    by_cons: dict[str, set[str]] = defaultdict(set)
    for r, t in zip(rows, types):
        by_cons[t].add(r["constitution_id"])
    print("sections per chapter type:")
    for t, c in Counter(types).most_common():
        print(f"  {t:36s} {c:4d}  ({len(by_cons[t])} constitutions)")
    print(f"share 'other': {100 * types.count('other') / len(types):.1f} %")
    pilot = stratified_pilot(rows, a.n, a.seed)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps({"seed": a.seed, "n": len(pilot), "classifier": "chapter_type v3",
                                 "snapshot_dump_date": "2026-09-14",
                                 "note": "a section may appear in both languages (translation pair); the unit is (constitution_id, section_id, lang)",
                                 "sections": pilot},
                                indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"pilot: {len(pilot)} sections → {a.out}")
    print("pilot strata:", Counter((p["chapter_type"], p["lang"]) for p in pilot).most_common())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

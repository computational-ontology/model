"""Preamble corpus (campaign 1 after D20): filtering and the stratified pilot draw.

Constitute's `preamble` topic key returns, for most in-force constitutions, one section whose
`article` reads "Preamble" (EN) / "Preámbulo" (ES). A few compilations (United Kingdom, Canada,
Tuvalu) return statute preambles or schedules under the same key; they are kept out of the
corpus by the article filter below and listed in the report so the exclusion is visible.

Strata for the pilot: language × length band. Length is the only structural covariate every
preamble has; chapter type (the `em` stratifier) is meaningless here. Bands are fixed in
characters so that the draw is reproducible from the manifest alone (no text needed).
"""

from __future__ import annotations

import json
import random
import re
from collections import defaultdict
from pathlib import Path

PREAMBLE_ARTICLE = re.compile(r"^\s*(preamble|pre[aá]mbulo)\s*$", re.IGNORECASE)
LENGTH_BANDS = [("short", 0, 600), ("medium", 600, 2000), ("long", 2000, 10**9)]  # characters


def length_band(n_chars: int) -> str:
    for name, lo, hi in LENGTH_BANDS:
        if lo <= n_chars < hi:
            return name
    return "long"


def is_preamble(r: dict) -> bool:
    """The constitution's own preamble: article (or, failing that, header) reads Preamble/Preámbulo,
    and the header, when present, is nothing else — statute preambles inside compilations
    (United Kingdom: "Magna Carta 1297" …), schedules and titled parts are excluded."""
    article, header = (r.get("article") or ""), (r.get("header") or "")
    name_ok = bool(PREAMBLE_ARTICLE.match(article)) or (not article and bool(PREAMBLE_ARTICLE.match(header)))
    header_ok = not header or bool(PREAMBLE_ARTICLE.match(header))
    return name_ok and header_ok


def load_rows(data: Path, langs: tuple[str, ...] = ("en", "es")) -> tuple[list[dict], list[dict]]:
    """Return (kept, excluded) manifest rows across languages; excluded = not a preamble article."""
    kept, excluded = [], []
    for lang in langs:
        p = data / f"snapshot_manifest_preamble_{lang}.json"
        if not p.exists():
            continue
        for r in json.loads(p.read_text(encoding="utf-8"))["sections"]:
            (kept if is_preamble(r) else excluded).append(r)
    return kept, excluded


def stratified_pilot(rows: list[dict], n: int = 100, seed: int = 20260916, min_per_stratum: int = 3) -> list[dict]:
    """Draw n preambles stratified by (lang, length band), proportional with a floor per stratum.

    Deterministic given the seed; ids and hashes only. One record per (constitution, lang):
    a constitution present in both languages may be drawn twice (translation pair).
    """
    rng = random.Random(seed)
    n = min(n, len(rows))
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rows:
        groups[(r["lang"], length_band(r["n_chars"]))].append(r)
    total = len(rows)
    alloc = {k: min(len(v), max(min_per_stratum, round(n * len(v) / total))) for k, v in groups.items()}
    order = sorted(groups, key=lambda k: -len(groups[k]))
    while sum(alloc.values()) > n:
        for k in order:
            if alloc[k] > min_per_stratum and sum(alloc.values()) > n:
                alloc[k] -= 1
    while sum(alloc.values()) < n:
        before = sum(alloc.values())
        for k in order:
            if alloc[k] < len(groups[k]) and sum(alloc.values()) < n:
                alloc[k] += 1
        if sum(alloc.values()) == before:
            break
    out: list[dict] = []
    for k in order:
        pool = sorted(groups[k], key=lambda r: (r["constitution_id"], r["section_id"]))
        for r in rng.sample(pool, alloc[k]):
            out.append({
                "constitution_id": r["constitution_id"], "section_id": r["section_id"], "lang": r["lang"],
                "length_band": k[1], "n_chars": r["n_chars"], "topic_keys": r.get("topic_keys", []),
                "article": r.get("article", ""), "sha256": r["sha256"],
            })
    return out


def main(argv: list[str] | None = None) -> int:
    import argparse
    from collections import Counter

    ap = argparse.ArgumentParser(description="Report the preamble corpus and draw the stratified pilot.")
    ap.add_argument("--data", type=Path, default=Path("data"))
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seed", type=int, default=20260916)
    ap.add_argument("--out", type=Path, default=Path("data/splits/pilot_preamble_100.json"))
    a = ap.parse_args(argv)
    kept, excluded = load_rows(a.data)
    print(f"preamble corpus: {len(kept)} records kept, {len(excluded)} excluded (not a preamble article)")
    for r in excluded:
        print(f"  excluded {r['constitution_id']} §{r['section_id']} {r['lang']} article={r.get('article')!r} header={r.get('header', '')[:50]!r}")
    print("by lang × length band:", dict(Counter((r["lang"], length_band(r["n_chars"])) for r in kept)))
    en = {r["constitution_id"] for r in kept if r["lang"] == "en"}
    es = {r["constitution_id"] for r in kept if r["lang"] == "es"}
    print(f"translation pairs (EN and ES): {len(en & es)}")
    pilot = stratified_pilot(kept, a.n, a.seed)
    dump = next(iter(json.loads((a.data / "snapshot_manifest_preamble_en.json").read_text(encoding="utf-8")).values()))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps({
        "seed": a.seed, "n": len(pilot), "strata": "lang × length band (short < 600 < medium < 2000 < long chars)",
        "filter": "is_preamble: article (or header) is Preamble/Preámbulo and the header is nothing else (statute preambles in compilations excluded)", "snapshot_dump_date": dump,
        "note": "a constitution may appear in both languages (translation pair); the unit is (constitution_id, section_id, lang)",
        "sections": pilot,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("pilot:", dict(Counter((r["lang"], r["length_band"]) for r in pilot)), "→", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

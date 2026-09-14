"""Fetch topic-tagged sections from the Constitute API into a local snapshot + hash-only manifest.

Documented endpoints only (Constitute API doc, linked from
https://www.constituteproject.org/content/data):

    GET {API_BASE}constitutions?lang=<lang>&in_force=true
    GET {API_BASE}sectionstopicsearch?cons_id=<id>&key=<topic>&lang=<lang>

`constopicsearch` and the HTML `/constitutions` pages are disallowed for robots and are not used.
Texts go to --out (git-ignored); only the manifest (ids, metadata, hashes) is committed.

Live shape (checked 2026-09-14): `sectionstopicsearch` returns {cons_id: {num_results, public,
results: [html, ...]}}; each html snippet is parsed by nra.constitute.

Usage:
    python -m nra.fetch --key em --lang en --out data/snapshot --manifest data/snapshot_manifest_en.json
    python -m nra.fetch --verify --manifest data/snapshot_manifest_en.json --out data/snapshot
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path
from urllib import robotparser

import requests

from .constitute import parse_topic_search
from .manifest import API_BASE, SectionRecord, SnapshotManifest, sha256_text

USER_AGENT = "nra-fetch/0.0.1 (+https://github.com/computational-ontology/model)"
PAUSE_S = 1.0  # no rate limit is published; we impose our own


def _robots() -> robotparser.RobotFileParser:
    rp = robotparser.RobotFileParser()
    rp.set_url("https://www.constituteproject.org/robots.txt")
    try:
        rp.read()
    except Exception:
        rp.parse(["User-agent: *", "Disallow: /"])  # unreachable → be conservative
    return rp


def _get(session: requests.Session, rp: robotparser.RobotFileParser, path: str, **params) -> object:
    url = API_BASE + path
    if not rp.can_fetch(USER_AGENT, url):
        raise RuntimeError(f"robots.txt disallows {url}")
    r = session.get(url, params=params, timeout=60, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    time.sleep(PAUSE_S)
    return r.json()


def _fname(cid: str, sid: str, lang: str) -> str:
    return f"{cid}__{sid.replace('/', '_')}__{lang}.txt"


def build(key: str, lang: str, out: Path, manifest_path: Path, limit: int | None = None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    session, rp = requests.Session(), _robots()
    cons = list(_get(session, rp, "constitutions", lang=lang, in_force="true"))
    if limit:
        cons = cons[:limit]
    records: list[SectionRecord] = []
    n_cons_hit = 0
    for i, c in enumerate(cons, 1):
        cid = str(c["id"])
        payload = _get(session, rp, "sectionstopicsearch", cons_id=cid, key=key, lang=lang)
        secs = parse_topic_search(payload, cid)
        if secs:
            n_cons_hit += 1
        for s in secs:
            if not s.text:
                continue
            (out / _fname(cid, s.section_id, lang)).write_text(s.text, encoding="utf-8")
            records.append(
                SectionRecord(
                    constitution_id=cid,
                    section_id=s.section_id,
                    lang=lang,
                    topic_keys=sorted(set([key] + s.topic_hits)),
                    header=s.header,
                    article=s.article,
                    copyright=c.get("copyright"),
                    translator=c.get("translator"),
                    sha256=sha256_text(s.text),
                    n_chars=len(s.text),
                )
            )
        print(f"[{i}/{len(cons)}] {cid}: {len(secs)} sections", file=sys.stderr)
    manifest = SnapshotManifest(
        dump_date=date.today(),
        query={"key": key, "lang": lang, "in_force": "true"},
        sections=records,
    )
    manifest.save(manifest_path)
    print(
        json.dumps(
            {
                "constitutions_queried": len(cons),
                "constitutions_with_hits": n_cons_hit,
                "sections": len(records),
                "manifest": str(manifest_path),
            }
        )
    )


def verify(manifest_path: Path, out: Path) -> int:
    """Re-hash local texts against the manifest. Returns the number of mismatches."""
    m = SnapshotManifest.load(manifest_path)
    bad = 0
    for rec in m.sections:
        p = out / _fname(rec.constitution_id, rec.section_id, rec.lang)
        if not p.exists() or sha256_text(p.read_text(encoding="utf-8")) != rec.sha256:
            bad += 1
            print(f"MISMATCH {p}", file=sys.stderr)
    return bad


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", help="Constitute topic key, e.g. em")
    ap.add_argument("--lang", default="en", choices=["en", "es", "ar"])
    ap.add_argument("--out", type=Path, default=Path("data/snapshot"))
    ap.add_argument("--manifest", type=Path, default=Path("data/snapshot_manifest.json"))
    ap.add_argument("--limit", type=int, default=None, help="only the first N constitutions (probe)")
    ap.add_argument("--verify", action="store_true", help="only re-hash against the manifest")
    a = ap.parse_args(argv)
    if a.verify or not a.key:
        n = verify(a.manifest, a.out)
        print(json.dumps({"mismatches": n}))
        return 1 if n else 0
    build(a.key, a.lang, a.out, a.manifest, a.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Fetch sections from the Constitute API into a local snapshot and write the manifest.

Endpoints used are the documented ones (Constitute API doc, linked from
https://www.constituteproject.org/content/data):

    GET {API_BASE}constitutions?lang=en&in_force=true
    GET {API_BASE}sectionstopicsearch?cons_id=<id>&key=<topic>&lang=<lang>

`constopicsearch` and `/constitutions` (HTML) are disallowed for robots and are not used.
The texts are written to --out (git-ignored); only the manifest is committed.

Usage:
    python -m nra.fetch --key em --lang en --out data/snapshot --manifest data/snapshot_manifest.json
    python -m nra.fetch --manifest data/snapshot_manifest.json --out data/snapshot   # rebuild + verify
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

from .manifest import API_BASE, SectionRecord, SnapshotManifest, sha256_text

USER_AGENT = "nra-fetch/0.0.1 (+https://github.com/computational-ontology/model)"
PAUSE_S = 1.0  # be polite; no rate limit is published, so we impose our own


def _robots_ok(url: str) -> bool:
    rp = robotparser.RobotFileParser()
    rp.set_url("https://www.constituteproject.org/robots.txt")
    try:
        rp.read()
    except Exception:  # robots unreachable → be conservative
        return False
    return rp.can_fetch(USER_AGENT, url)


def _get(session: requests.Session, path: str, **params) -> object:
    url = API_BASE + path
    if not _robots_ok(url):
        raise RuntimeError(f"robots.txt disallows {url}")
    r = session.get(url, params=params, timeout=60, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    time.sleep(PAUSE_S)
    return r.json()


def list_constitutions(session: requests.Session, lang: str, in_force: bool = True) -> list[dict]:
    data = _get(session, "constitutions", lang=lang, in_force=str(in_force).lower())
    return list(data)


def fetch_sections(session: requests.Session, cons_id: str, key: str, lang: str) -> list[dict]:
    data = _get(session, "sectionstopicsearch", cons_id=cons_id, key=key, lang=lang)
    return list(data)


def _section_text(sec: dict) -> str:
    # Field names follow the API doc; adjust here if the JSON shape differs on first real run.
    return str(sec.get("text") or sec.get("content") or "")


def build(key: str, lang: str, out: Path, manifest_path: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    records: list[SectionRecord] = []
    for cons in list_constitutions(session, lang):
        cid = str(cons["id"])
        for sec in fetch_sections(session, cid, key, lang):
            text = _section_text(sec)
            if not text:
                continue
            sid = str(sec.get("id") or sec.get("section_id"))
            (out / f"{cid}__{sid}__{lang}.txt").write_text(text, encoding="utf-8")
            records.append(
                SectionRecord(
                    constitution_id=cid,
                    section_id=sid,
                    lang=lang,
                    topic_keys=[key],
                    copyright=cons.get("copyright"),
                    translator=cons.get("translator"),
                    sha256=sha256_text(text),
                    n_chars=len(text),
                )
            )
    manifest = SnapshotManifest(
        dump_date=date.today(),
        query={"key": key, "lang": lang, "in_force": "true"},
        sections=records,
    )
    manifest.save(manifest_path)
    print(f"{len(records)} sections → {out}; manifest → {manifest_path}", file=sys.stderr)


def verify(manifest_path: Path, out: Path) -> int:
    """Re-hash local texts against the manifest. Returns the number of mismatches."""
    m = SnapshotManifest.load(manifest_path)
    bad = 0
    for rec in m.sections:
        p = out / f"{rec.constitution_id}__{rec.section_id}__{rec.lang}.txt"
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
    ap.add_argument("--verify", action="store_true", help="only re-hash against the manifest")
    a = ap.parse_args(argv)
    if a.verify or not a.key:
        n = verify(a.manifest, a.out)
        print(json.dumps({"mismatches": n}))
        return 1 if n else 0
    build(a.key, a.lang, a.out, a.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

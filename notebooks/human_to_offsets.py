"""Convert an export of the annotation instrument (human, codebook v2.0) into the offsets form used by the
model annotations (`*.offsets.jsonl`, one record per preamble), so that `align_claims.py` and `analyze_02.py`
read human and model records alike. Verifies every span against the frozen snapshot when `--snapshot` is
given: the quoted text must equal the record's text at the offsets and the record's SHA-256 must match.

    python notebooks/human_to_offsets.py calib6_Luis_2026-09-18.json --snapshot data/snapshot_preamble \\
        --out data/annotations/calibration/Luis.offsets.jsonl [--only-complete]

Amendable output (Table 1): the human labels are the project's gold candidates, still amendable until adjudication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

NATURALISING = {"nature", "history", "god", "spirit", "doctrine"}


def rule(ground: str | None) -> str:
    return "naturalised" if ground in NATURALISING else "revealed" if ground == "act" else "other"


def load_text(snapshot: Path, rec: dict) -> str | None:
    p = snapshot / f"{rec['constitution_id']}__{rec['section_id']}__{rec['lang']}.txt"
    if not p.exists():
        return None
    return p.read_bytes().decode("utf-8").replace("\r\n", "\n")  # LF form = the manifest's hash


def convert(export: dict, snapshot: Path | None, only_complete: bool) -> tuple[list[dict], list[str]]:
    out, problems = [], []
    for rec in export["records"]:
        if only_complete and not rec.get("complete"):
            continue
        if not rec["t5"] and not rec["t2"] and not rec.get("complete"):
            continue  # untouched preamble: nothing to release
        text = load_text(snapshot, rec) if snapshot else None
        key = f"{rec['constitution_id']}/{rec['lang']}"
        if text is not None:
            h = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if h != rec["sha256"]:
                problems.append(f"{key}: sha256 mismatch (export {rec['sha256'][:12]}, snapshot {h[:12]})")
            for c in rec["t5"]:
                if text[c["start"]:c["end"]] != c["claim"]:
                    problems.append(f"{key}: claim span [{c['start']},{c['end']}) does not match its text")
                for m, (a, b) in zip(c["markers"], c["marker_offsets"], strict=True):
                    if text[a:b] != m:
                        problems.append(f"{key}: marker span [{a},{b}) does not match its text")
                    if not (c["start"] <= a and b <= c["end"]):
                        problems.append(f"{key}: marker [{a},{b}) outside its claim")
            for m in rec["t2"]:
                if text[m["start"]:m["end"]] != m["mention"]:
                    problems.append(f"{key}: mention span [{m['start']},{m['end']}) does not match its text")
        for c in rec["t5"]:
            if c["ground"] is None or c["frame"] is None:
                problems.append(f"{key}: claim [{c['start']},{c['end']}) has no ground or no frame")
            if c["operator"] != rule(c["ground"]):
                problems.append(f"{key}: operator {c['operator']} != rule({c['ground']})")
        out.append({
            "constitution_id": rec["constitution_id"], "section_id": rec["section_id"], "lang": rec["lang"],
            "sha256": rec["sha256"], "annotator": rec["annotator"], "emitter_kind": "human",
            "emitted_at": rec.get("timestamp") or export["exported_at"], "codebook_version": rec["codebook_version"],
            "instrument": rec.get("instrument"), "prompt_version": None, "decoding": None,
            "output": {
                "t2": [{"mention": [m["start"], m["end"]], "type": m["type"]} for m in rec["t2"]],
                "t5": [{"claim": [c["start"], c["end"]], "operator": rule(c["ground"]), "markers": c["marker_offsets"],
                        "frame": c["frame"], "ground": c["ground"], "secondary": c.get("secondary_operator"),
                        "note": c.get("note") or ""} for c in rec["t5"]],
                "notes": rec.get("notes") or "",
            },
            "parse_ok": True, "verbatim_ok": True, "complete": bool(rec.get("complete")),
            "run": {"length_band": rec.get("length_band"), "presentation_order": export.get("presentation_order"),
                    "order_seed": export.get("order_seed")},
        })
    return out, problems


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("export", nargs="+", help="instrument export(s), JSON")
    ap.add_argument("--snapshot", type=Path, default=None, help="directory with <cid>__<sid>__<lang>.txt (verifies spans)")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only-complete", action="store_true")
    args = ap.parse_args()
    records, problems = [], []
    for f in args.export:
        export = json.loads(Path(f).read_text(encoding="utf-8"))
        r, p = convert(export, args.snapshot, args.only_complete)
        records += r
        problems += p
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="\n") as fo:
        for r in records:
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")
    n_claims = sum(len(r["output"]["t5"]) for r in records)
    n_ment = sum(len(r["output"]["t2"]) for r in records)
    print(f"{len(records)} records, {n_claims} claims, {n_ment} mentions -> {args.out}")
    print("verification:", "OK" if not problems else f"{len(problems)} problem(s)")
    for p in problems:
        print("  -", p)
    if problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

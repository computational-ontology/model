"""Claim-level agreement between emitters, on the releasable offsets form.

Sections are the unit in analyze_02.py; here the unit is the aligned claim: two claims from two emitters
(models, or human annotators converted with human_to_offsets.py; any *.offsets.jsonl in --dir is read)
are aligned when their character spans overlap with IoU >= --iou (default 0.5), greedily by best IoU.
Prints, per model pair: coverage (aligned / claims), Krippendorff nominal alpha on operator, ground and
frame over aligned claims (plus operator_from_ground, and operator alpha per language and per length band),
and per model the share of claims whose operator matches the codebook v2.0 rule operator = rule(ground). Amendable output (Table 1): a measure of solidarity between emitters, not
of objectivity (Manifiesto pp. 97-99); objectivity comes from the human anchoring (D11).
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
from pathlib import Path

import krippendorff
import numpy as np

MODELS = {"gemma": "gemma-4-12B-it", "qwen": "Qwen3.5-9B", "eurollm": "EuroLLM-9B-Instruct-2512"}
NATURALISING = {"nature", "history", "god", "spirit", "doctrine"}


def rule(ground: str) -> str:
    return "naturalised" if ground in NATURALISING else "revealed" if ground == "act" else "other"


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open(encoding="utf-8")]


def iou(a, b) -> float:
    inter = max(0, min(a[1], b[1]) - max(a[0], b[0]))
    union = (a[1] - a[0]) + (b[1] - b[0]) - inter
    return inter / union if union else 0.0


def align(ca: list[dict], cb: list[dict], thr: float) -> list[tuple[dict, dict]]:
    cand = sorted(((iou(x["claim"], y["claim"]), i, j) for i, x in enumerate(ca) for j, y in enumerate(cb)), reverse=True)
    used_a, used_b, out = set(), set(), []
    for s, i, j in cand:
        if s < thr:
            break
        if i in used_a or j in used_b:
            continue
        used_a.add(i)
        used_b.add(j)
        out.append((ca[i], cb[j]))
    return out


def alpha(pairs: list[tuple[str, str]]) -> float | None:
    if len(pairs) < 2:
        return None
    vals = sorted({v for p in pairs for v in p})
    if len(vals) < 2:
        return None
    idx = {v: k for k, v in enumerate(vals)}
    data = np.array([[idx[a] for a, _ in pairs], [idx[b] for _, b in pairs]], dtype=float)
    try:
        return round(float(krippendorff.alpha(reliability_data=data, level_of_measurement="nominal")), 3)
    except ValueError:  # degenerate domain (no pairable values)
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="data/annotations/stage1_preamble")
    ap.add_argument("--iou", type=float, default=0.5)
    args = ap.parse_args()
    d = Path(args.dir)
    files = {m: d / f"{n}.offsets.jsonl" for m, n in MODELS.items() if (d / f"{n}.offsets.jsonl").exists()}
    known = set(files.values())
    for f in sorted(d.glob("*.offsets.jsonl")):  # any other emitter (human annotators, extra models): keyed by file stem
        if f not in known:
            files[f.name.replace(".offsets.jsonl", "")] = f
    R = {m: {(r["constitution_id"], r["section_id"], r["lang"]): r for r in read(f) if r["parse_ok"]} for m, f in files.items()}
    # a claim whose span could not be located in the record (non-verbatim quote) has claim=None: it cannot be aligned
    for m, recs in R.items():
        dropped = 0
        for r in recs.values():
            t5 = r["output"]["t5"]
            kept = [c for c in t5 if c["claim"]]
            dropped += len(t5) - len(kept)
            r["output"]["t5"] = kept
        print(f"{m}: {dropped} claims without a located span dropped from alignment")

    print("operator = rule(ground) consistency per model (codebook v2.0 section 3):")
    for m, recs in R.items():
        cl = [c for r in recs.values() for c in r["output"]["t5"]]
        ok = sum(c["operator"] == rule(c["ground"]) for c in cl)
        off = collections.Counter((c["ground"], c["operator"]) for c in cl if c["operator"] != rule(c["ground"]))
        print(f"  {m:8s} {ok}/{len(cl)} = {ok/len(cl):.2f}; top mismatches (ground, operator): {off.most_common(4)}")

    for a, b in itertools.combinations(R, 2):
        keys = sorted(set(R[a]) & set(R[b]))
        if not keys:
            print(f"\n{a}-{b}: no section annotated by both; skipped")
            continue
        pairs, na, nb = [], 0, 0
        for k in keys:
            ca, cb = R[a][k]["output"]["t5"], R[b][k]["output"]["t5"]
            na += len(ca)
            nb += len(cb)
            pairs += align(ca, cb, args.iou)
        print(f"\n{a}-{b}: {len(keys)} sections valid in both; aligned claims {len(pairs)} "
              f"(coverage {len(pairs)/max(na, 1):.2f} of {a}, {len(pairs)/max(nb, 1):.2f} of {b}; IoU >= {args.iou})")
        for field in ("operator", "ground", "frame"):
            pp = [(x[field], y[field]) for x, y in pairs]
            agree = sum(x == y for x, y in pp) / max(len(pp), 1)
            print(f"  {field:9s} raw agreement {agree:.2f}  alpha {alpha(pp)}")
        pp = [(rule(x["ground"]), rule(y["ground"])) for x, y in pairs]
        print(f"  operator_from_ground raw {sum(x == y for x, y in pp)/max(len(pp), 1):.2f}  alpha {alpha(pp)}")
        for lang in ("en", "es"):
            sub = [(x["operator"], y["operator"]) for k in keys if k[2] == lang
                   for x, y in align(R[a][k]["output"]["t5"], R[b][k]["output"]["t5"], args.iou)]
            print(f"  operator {lang}: n={len(sub)} alpha {alpha(sub)}")
        for band in ("short", "medium", "long"):
            sub = [(x["operator"], y["operator"]) for k in keys if R[a][k]["run"]["length_band"] == band
                   for x, y in align(R[a][k]["output"]["t5"], R[b][k]["output"]["t5"], args.iou)]
            print(f"  operator {band}: n={len(sub)} alpha {alpha(sub)}")
        conf = collections.Counter((x["operator"], y["operator"]) for x, y in pairs)
        print("  operator confusion (a, b):", dict(conf.most_common()))


if __name__ == "__main__":
    main()

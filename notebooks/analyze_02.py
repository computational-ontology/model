"""Bake-off analysis for notebook 02 (Stage 1 silver annotations).

Reads the releasable offsets form in data/annotations/stage1/ and prints: format discipline (§7),
model–model agreement under three units (§8) and the chapter-type table. Run from the repo root:

    python notebooks/analyze_02.py [--private DIR]

--private points at a directory with the span form (kept out of the repository); it adds the checks
that need the strings: prompt-example markers echoed by the model, and T2 types of boundary terms.
Everything printed here is amendable output of the pipeline (Table 1), not a property of the corpus.
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics as st
from pathlib import Path

import krippendorff
import numpy as np
import pandas as pd

MODELS = {"gemma": "gemma-4-12B-it", "qwen": "Qwen3.5-9B", "eurollm": "EuroLLM-9B-Instruct-2512"}
PRIVATE_NAMES = {"gemma": "google__gemma-4-12B-it", "qwen": "Qwen__Qwen3.5-9B", "eurollm": "utter-project__EuroLLM-9B-Instruct-2512"}
# markers quoted as examples in the p1 prompt (notebooks/_shared_cells.py); a model may copy them instead of quoting
EXAMPLE_MARKERS = {"in case of", "when X threatens", "during any period of public emergency", "en caso de",
                   "if the President is satisfied", "may declare", "subject to Article 58", "con acuerdo del Senado"}
LABELS = {"revealed": 0, "naturalised": 1, "other": 2}


def read(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open(encoding="utf-8")]


def key(r: dict) -> tuple:
    return (r["constitution_id"], r["section_id"], r["lang"])


def labels_of(r: dict) -> list[str]:
    return [c["operator"] for c in r["output"]["t5"]] if r["parse_ok"] else []


def dominant(labels: list[str], ties: str = "missing") -> str | None:
    """Section-level dominant T5 label. ties='other' is the rule notebook 02 v1 used; 'missing' is the
    honest one (a 1–1 split carries no dominant label)."""
    if not labels:
        return None
    c = collections.Counter(labels).most_common()
    if len(c) == 1 or c[0][1] > c[1][1]:
        return c[0][0]
    return "other" if ties == "other" else None


def share_naturalised(labels: list[str]) -> float | None:
    return sum(x == "naturalised" for x in labels) / len(labels) if labels else None


def alpha(recs: dict, keys: list, models: list, fn, level: str) -> float:
    rows = []
    for m in models:
        vals = [fn(recs[k].get(m, [])) for k in keys]
        if level == "nominal":
            vals = [LABELS[v] if v in LABELS else np.nan for v in vals]
        else:
            vals = [np.nan if v is None else v for v in vals]
        rows.append(vals)
    return float(krippendorff.alpha(reliability_data=np.array(rows, dtype=float), level_of_measurement=level))


def pairwise(recs: dict, keys: list, models: list, fn) -> dict:
    out = {}
    for i, a in enumerate(models):
        for b in models[i + 1:]:
            n = agree = 0
            for k in keys:
                x, y = fn(recs[k].get(a, [])), fn(recs[k].get(b, []))
                if x is None or y is None:
                    continue
                n += 1
                agree += x == y
            out[f"{a}-{b}"] = (agree, n, round(agree / n, 2) if n else None)
    return out


def discipline(R: dict) -> pd.DataFrame:
    rows = []
    for m, rs in R.items():
        valid = [r for r in rs if r["parse_ok"]]
        t2 = collections.Counter(x["type"] for r in valid for x in r["output"]["t2"])
        claims = [c for r in valid for c in r["output"]["t5"]]
        secondary = collections.Counter((c["secondary"] or "null") for c in claims)
        rows.append(dict(
            model=m, records=len(rs), valid=len(valid), eos=sum(r["run"]["stopped_by_eos"] for r in rs),
            fully_verbatim=sum(bool(r["verbatim_ok"]) for r in rs), duplicates_removed=sum(r["run"]["n_dup_removed"] for r in rs),
            out_tokens_mean=round(st.mean(r["run"]["n_out"] for r in rs)), out_tokens_p90=round(float(np.percentile([r["run"]["n_out"] for r in rs], 90))),
            sec_mean=round(st.mean(r["run"]["sec"] for r in rs)), sec_p90=round(float(np.percentile([r["run"]["sec"] for r in rs], 90))),
            mentions=sum(t2.values()), t2_physical=t2["physical"], t2_ideal=t2["ideal"], t2_social=t2["social"],
            claims=len(claims), claims_per_section=round(len(claims) / max(len(valid), 1), 2),
            markers_empty=sum(not c["markers"] for c in claims),
            secondary=", ".join(f"{k} {v}" for k, v in secondary.most_common()),
        ))
    return pd.DataFrame(rows).set_index("model")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="data/annotations/stage1")
    ap.add_argument("--private", default=None, help="directory with the span-form JSONL (not in the repo)")
    args = ap.parse_args()
    d = Path(args.dir)
    R = {m: read(d / f"{name}.offsets.jsonl") for m, name in MODELS.items()}
    models = list(R)
    pd.set_option("display.width", 220)
    pd.set_option("display.max_columns", 40)

    print("§7 format discipline\n")
    df7 = discipline(R)
    print(df7.drop(columns="secondary").T.to_string(), "\n")
    for m in models:
        print(f"  {m} secondary: {df7.loc[m, 'secondary']}")
    if any(r["parse_ok"] and "ground" in r["output"]["t5"][0] for rs in R.values() for r in rs[:1]):
        print("\nT5 ground / frame shares (v2.0 records):")
        for m, rs in R.items():
            g = collections.Counter(c["ground"] for r in rs if r["parse_ok"] for c in r["output"]["t5"])
            f = collections.Counter(c["frame"] for r in rs if r["parse_ok"] for c in r["output"]["t5"])
            n = sum(g.values()) or 1
            print(f"  {m:8s} ground: " + ", ".join(f"{k} {v/n:.2f}" for k, v in g.most_common()) + " | frame: " + ", ".join(f"{k} {v/n:.2f}" for k, v in f.most_common()))
    print("\nT5 claim-level shares by language (revealed / naturalised / other):")
    for m, rs in R.items():
        for lang in ("en", "es"):
            c = collections.Counter(x for r in rs if r["lang"] == lang for x in labels_of(r))
            n = sum(c.values()) or 1
            print(f"  {m:8s} {lang}: n={sum(c.values()):3d}  {c['revealed']/n:.2f} / {c['naturalised']/n:.2f} / {c['other']/n:.2f}")

    recs: dict = {}
    for m, rs in R.items():
        for r in rs:
            recs.setdefault(key(r), {"chapter_type": r["run"].get("chapter_type") or r["run"].get("length_band"), "lang": r["lang"]})[m] = labels_of(r)
    keys = sorted(recs)
    dom_other = lambda x: dominant(x, "other")  # noqa: E731
    dom_missing = lambda x: dominant(x, "missing")  # noqa: E731

    print("\n§8 agreement between emitters (100 pilot sections)")
    print("  section dominant label, ties → other (notebook v1 rule):", pairwise(recs, keys, models, dom_other),
          "α =", round(alpha(recs, keys, models, dom_other, "nominal"), 3))
    print("  section dominant label, ties → missing:               ", pairwise(recs, keys, models, dom_missing),
          "α =", round(alpha(recs, keys, models, dom_missing, "nominal"), 3))
    print("  share of naturalised claims per section (interval):    α =", round(alpha(recs, keys, models, share_naturalised, "interval"), 3))
    print("  tied sections per model:", {m: sum(dom_other(recs[k].get(m, [])) == "other" and dom_missing(recs[k].get(m, [])) is None for k in keys) for m in models})
    for lang in ("en", "es"):
        sub = [k for k in keys if recs[k]["lang"] == lang]
        print(f"  {lang} ({len(sub)}): ties→missing", pairwise(recs, sub, models, dom_missing),
              "α =", round(alpha(recs, sub, models, dom_missing, "nominal"), 3),
              "| interval α =", round(alpha(recs, sub, models, share_naturalised, "interval"), 3))
    unanimous = collections.Counter()
    for k in keys:
        ds = [dom_missing(recs[k].get(m, [])) for m in models]
        if all(ds) and len(set(ds)) == 1:
            unanimous[ds[0]] += 1
    print("  unanimous sections (all three, ties → missing):", dict(unanimous))

    print("\nmean share of naturalised claims by chapter type (em) or length band (preambles) × model:")
    tab: dict = collections.defaultdict(lambda: collections.defaultdict(list))
    for k in keys:
        for m in models:
            labs = recs[k].get(m, [])
            if labs:
                tab[recs[k]["chapter_type"]][m].append(share_naturalised(labs))
    t8 = pd.DataFrame({ct: {m: round(st.mean(v), 2) for m, v in dd.items()} | {"n": len(dd["gemma"])} for ct, dd in tab.items()}).T
    print(t8.sort_values("n", ascending=False).to_string())

    if args.private:
        p = Path(args.private)
        S = {m: read(p / f"{name}.jsonl") for m, name in PRIVATE_NAMES.items()}
        print("\n[private] prompt-example markers echoed (claims with ≥1 example marker / claims; of those markers, not verbatim):")
        for m, rs in S.items():
            claims = [c for r in rs if r["parse_ok"] for c in r["output"]["t5"]]
            echoed = [(mk, repr(mk) in r["run"]["verdict"]) for r in rs if r["parse_ok"] for c in r["output"]["t5"] for mk in c["markers"] if mk in EXAMPLE_MARKERS]
            print(f"  {m}: {sum(any(mk in EXAMPLE_MARKERS for mk in c['markers']) for c in claims)}/{len(claims)} claims; "
                  f"{len(echoed)} markers, {sum(b for _, b in echoed)} not in the text; "
                  f"{dict(collections.Counter(mk for mk, _ in echoed).most_common(4))}")
        pb = p / "google__gemma-4-12B-it.paraphraseB.jsonl"
        if pb.exists():
            A = {key(r): r for r in S["gemma"]}
            same = n = 0
            sa, sb = [], []
            print("\n[private] §9 paraphrase B (gemma): dominant A → B (ties → missing), share naturalised A → B")
            for b in read(pb):
                a = A[key(b)]
                la, lb = labels_of(a), labels_of(b)
                da, db = dom_missing(la), dom_missing(lb)
                if da and db:
                    n += 1
                    same += da == db
                sa.append(share_naturalised(la))
                sb.append(share_naturalised(lb))
                print(f"  {b['constitution_id']:28s} §{b['section_id']:8s} {str(da):11s} → {str(db):11s}  {share_naturalised(la):.2f} → {share_naturalised(lb):.2f}{'' if da == db else '   changed'}")
            print(f"  unchanged where both defined: {same}/{n}; interval α (A vs B, share naturalised) = "
                  f"{krippendorff.alpha(reliability_data=np.array([sa, sb]), level_of_measurement='interval'):.3f}")


if __name__ == "__main__":
    main()

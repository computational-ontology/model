"""Builds notebooks/01b_preamble_check.ipynb. Run from the repo root: python notebooks/build_01b.py"""

from pathlib import Path

import nbformat as nbf

nb = nbf.v4.new_notebook()
C: list = []
md, code = (lambda s: C.append(nbf.v4.new_markdown_cell(s))), (lambda s: C.append(nbf.v4.new_code_cell(s)))

md("""# 01b · Preamble snapshot check — first read of the campaign-1 corpus (D20)

Campaign 1 of the New-Realism Analyzer (github.com/computational-ontology/model) moves from
emergency provisions to **preambles as the unit** (decision D20). This notebook is the first read
of the frozen snapshot `luisdscientist/nra-snapshot-preamble` (Constitute topic key `preamble`,
in-force constitutions, EN + ES, fetched 2026-09-16): mount path, hash verification of every
record the corpus filter keeps, a length and paragraph profile, the co-occurring topic keys that
Constitute assigns to preambles (`auth`, `motive`, `god`, `prevcond` …), and a look at a few
preambles across the length bands to ground the codebook v2.0 examples (D21).

Nothing here is a result: it establishes that the record is the record (hashes), and describes
the population the pilot was drawn from. Settings: no accelerator needed, Internet **on**
(the manifests and the pilot draw are read from the repository at `main`), dataset
`luisdscientist/nra-snapshot-preamble` attached.""")

md("""## 0 · Mount and repository files""")
code("""import os, json, hashlib, unicodedata, collections, statistics as st
import requests, pandas as pd
MOUNT = "/kaggle/input/datasets/luisdscientist/nra-snapshot-preamble"
RAW = "https://raw.githubusercontent.com/computational-ontology/model/main/"
# the dataset was uploaded as a folder, so the texts sit one level down (…/snapshot_preamble/);
# accept either layout
ROOT = next((os.path.join(d, "") for d, _, f in os.walk(MOUNT) if any(x.endswith(".txt") for x in f)), MOUNT).rstrip("/")
files = sorted(f for f in os.listdir(ROOT) if f.endswith(".txt"))
print(len(files), "files mounted at", ROOT); print(files[:3], "…", files[-2:])
manifests = {lang: requests.get(RAW + f"data/snapshot_manifest_preamble_{lang}.json", timeout=30).json() for lang in ("en", "es")}
pilot_meta = requests.get(RAW + "data/splits/pilot_preamble_100.json", timeout=30).json()
for lang, m in manifests.items():
    print(lang, "manifest:", m["dump_date"], m["query"], len(m["sections"]), "sections")
print("pilot:", pilot_meta["seed"], pilot_meta["n"], "|", pilot_meta["strata"])""")

md("""## 1 · Corpus filter and hash verification

`nra.preamble.is_preamble` keeps the constitution's own preamble and drops statute preambles
inside compilations (United Kingdom), schedules and titled parts. The rule is reproduced inline
so this notebook has no dependency on the package. Every kept record is re-hashed against the
manifest: a mismatch means the mounted snapshot is not the one the manifest describes.""")
code("""import re
PREAMBLE = re.compile(r"^\\s*(preamble|pre[aá]mbulo)\\s*$", re.IGNORECASE)
def is_preamble(r):
    a, h = (r.get("article") or ""), (r.get("header") or "")
    return (bool(PREAMBLE.match(a)) or (not a and bool(PREAMBLE.match(h)))) and (not h or bool(PREAMBLE.match(h)))
def fname(cid, sid, lang):
    return f"{cid}__{sid.replace('/', '_')}__{lang}.txt"
def sha256_text(text):
    return hashlib.sha256(unicodedata.normalize("NFC", text).strip().encode("utf-8")).hexdigest()

rows, excluded, mismatches, missing = [], [], [], []
for lang, m in manifests.items():
    for r in m["sections"]:
        if not is_preamble(r):
            excluded.append(r); continue
        path = f"{ROOT}/{fname(r['constitution_id'], r['section_id'], lang)}"
        if not os.path.exists(path):
            missing.append(path); continue
        text = open(path, encoding="utf-8").read()
        if sha256_text(text) != r["sha256"]:
            mismatches.append(r["constitution_id"])
        rows.append({**r, "text": text, "n_par": sum(1 for line in text.split("\\n") if line.strip()),
                     "n_words": len(text.split())})
print(f"kept {len(rows)} | excluded {len(excluded)} | missing files {len(missing)} | hash mismatches {len(mismatches)}")
assert not missing and not mismatches, "the mounted snapshot does not match the manifests — stop here"
print("excluded:", sorted({(r['constitution_id'], r['lang']) for r in excluded}))""")

md("""## 2 · Length and paragraph profile

Length bands are those of the pilot draw (short < 600 < medium < 2 000 < long characters).
Paragraphs are the `section/N` bodies Constitute returns (one line each in the snapshot) —
the natural candidate unit if the preamble ever needs segmenting (open decision O9).""")
code("""def band(n): return "short" if n < 600 else "medium" if n < 2000 else "long"
df = pd.DataFrame([{k: v for k, v in r.items() if k != "text"} for r in rows])
df["band"] = df["n_chars"].map(band)
print(df.groupby("lang")[["n_chars", "n_words", "n_par"]].describe().round(0).T)
print("\\nrecords by lang × band:"); print(df.pivot_table(index="lang", columns="band", values="constitution_id", aggfunc="count").fillna(0).astype(int))
print("\\nparagraphs per preamble (quantiles):", df["n_par"].quantile([.1, .25, .5, .75, .9, 1]).round(0).to_dict())
print("chars per paragraph (median over preambles):", round((df["n_chars"] / df["n_par"]).median()))
print("\\nlongest:", df.nlargest(5, "n_chars")[["constitution_id", "lang", "n_chars", "n_par"]].to_string(index=False))
print("shortest:", df.nsmallest(5, "n_chars")[["constitution_id", "lang", "n_chars", "n_par"]].to_string(index=False))""")

md("""## 3 · Co-occurring topic keys

Constitute tags the preamble paragraphs with other keys of its taxonomy. Their frequencies are
a free description of the population and a candidate stratifier for later draws — and a
contrast variable for T5: preambles tagged `god` or `prevcond` are where the founding act is
most explicitly grounded in something outside the act itself.""")
code("""keys = collections.Counter(k for r in rows for k in r["topic_keys"] if k != "preamble")
print(pd.Series(keys).sort_values(ascending=False).head(20))
for k in ("auth", "motive", "god", "prevcond", "figures", "region"):
    sub = df[df["topic_keys"].map(lambda ks: k in ks)]
    print(f"{k:9s} {len(sub):3d} records | EN {int((sub.lang=='en').sum())} ES {int((sub.lang=='es').sum())} | median chars {int(sub.n_chars.median())}")
pairs = set(df[df.lang == "en"].constitution_id) & set(df[df.lang == "es"].constitution_id)
print("\\ntranslation pairs:", len(pairs))""")

md("""## 4 · The pilot on the mounted snapshot

Every pilot record must exist and hash-match; the pilot's own strata are recomputed from the
mounted texts as a check on the draw.""")
code("""pilot = pilot_meta["sections"]
have = {(r["constitution_id"], r["section_id"], r["lang"]): r for r in rows}
bad = [p for p in pilot if (p["constitution_id"], p["section_id"], p["lang"]) not in have or have[(p["constitution_id"], p["section_id"], p["lang"])]["sha256"] != p["sha256"]]
print(len(pilot), "pilot records |", len(bad), "not found or hash-mismatched")
assert not bad
pdf = pd.DataFrame(pilot); pdf["band_now"] = pdf["n_chars"].map(band)
print(pdf.pivot_table(index="lang", columns="band_now", values="constitution_id", aggfunc="count").fillna(0).astype(int))
print("pilot translation pairs:", len(set(pdf[pdf.lang=='en'].constitution_id) & set(pdf[pdf.lang=='es'].constitution_id)))""")

md("""## 5 · A first look, one preamble per band and language

Read, do not annotate. The point is to see what a *claim* looks like here — a preamble is a
single founding act unfolded in paragraphs ("We, the people … adopt", "Recognising …",
"Desiring …") with no factual trigger separable from the act. This is the material the T5 test
of codebook v2.0 has to be rewritten for (D21). Printed to this private notebook only; the
texts stay out of the repository.""")
code("""import random
rng = random.Random(20260916)
for lang in ("en", "es"):
    for b in ("short", "medium", "long"):
        pool = [r for r in rows if r["lang"] == lang and band(r["n_chars"]) == b]
        r = rng.choice(pool)
        print("=" * 100); print(f"[{lang} · {b}] {r['constitution_id']} — {r['n_chars']} chars, {r['n_par']} paragraphs, keys {r['topic_keys']}")
        print(r["text"][:1500] + (" …" if len(r["text"]) > 1500 else ""))""")

md("""## 6 · What this notebook establishes

Fill in after the run:

- Mounted files __ ; kept __ (EN __ / ES __); excluded __ (listed); hash mismatches __ (must be 0).
- Length: EN median __ chars / __ paragraphs; ES median __ / __; long tail (> 3 000 chars): __ records.
- Keys: `auth` __, `motive` __, `god` __, `prevcond` __ ; translation pairs __.
- Pilot: 100/100 present and hash-matched; strata as drawn.
- Observations for codebook v2.0 (from §5): __ (how the founding subject is named or erased; recurring performative verbs; where the factual-looking clauses sit — history, God, territory).

Everything above is amendable output (Table 1); the 190 texts are identified by hash and were not modified.""")

nb["cells"] = C
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["language_info"] = {"name": "python"}
out = Path(__file__).with_name("01b_preamble_check.ipynb")
nbf.write(nb, out)
print("wrote", out, len(C), "cells")

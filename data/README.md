# data/

**No constitutional text lives in this directory or in any release** (see `../NOTICE`: Constitute texts are CC BY-NC 3.0 with third-party exceptions).

What is committed:

- `snapshot_manifest.json` — produced by `nra.fetch`: dump date, API base URL, query parameters, and one entry per section with `constitution_id`, `section_id`, `lang`, `topic_keys`, `copyright`, `translator`, `sha256` of the text. This manifest is the **in-emendable record** every experiment reads from.
- `annotations/` — gold and silver labels keyed to `constitution_id + section_id` (never the text).
- `splits/` — frozen train / dev / test section ids, with seed.

What is ignored (`.gitignore`): `snapshot/` (the fetched texts, kept locally and on the private Kaggle Dataset), `raw/`.

To rebuild the snapshot from the manifest:

```
python -m nra.fetch --manifest data/snapshot_manifest.json --out data/snapshot/
```

The fetcher uses only the documented endpoints under `https://www.constituteproject.org/service/` and respects `robots.txt`; it verifies each section's hash against the manifest and aborts on mismatch (the record changed upstream — that is a new inscription, so a new manifest, not a silent update).

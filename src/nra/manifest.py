"""Snapshot manifest — the in-emendable record every experiment reads from.

The manifest holds *no text*: only identifiers, metadata and the SHA-256 of each section's
text as fetched on the dump date. See data/README.md and NOTICE.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field

API_BASE = "https://www.constituteproject.org/service/"


class SectionRecord(BaseModel):
    constitution_id: str
    section_id: str
    lang: str = Field(pattern="^(en|es|ar)$")
    topic_keys: list[str] = Field(default_factory=list)
    header: str = ""  # structural breadcrumb (chapter/article), not the text
    article: str = ""
    copyright: str | None = None
    translator: str | None = None
    sha256: str = Field(min_length=64, max_length=64)
    n_chars: int


class SnapshotManifest(BaseModel):
    dump_date: date
    api_base: str = API_BASE
    query: dict[str, str]  # e.g. {"key": "em", "lang": "en", "in_force": "true"}
    notice: str = (
        "Texts are CC BY-NC 3.0 (Constitute) with third-party exceptions; not redistributed. "
        "Cite Elkins, Ginsburg & Melton, Constitute, constituteproject.org."
    )
    sections: list[SectionRecord]

    def save(self, path: Path) -> None:
        path.write_text(self.model_dump_json(indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> SnapshotManifest:
        return cls.model_validate(json.loads(path.read_text(encoding="utf-8")))


def sha256_text(text: str) -> str:
    """Hash of the normalised text (NFC, stripped). The text itself is never stored here."""
    import unicodedata

    norm = unicodedata.normalize("NFC", text).strip()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()

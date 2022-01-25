from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OkkyPostItem:
    id: int
    title: str
    body: str

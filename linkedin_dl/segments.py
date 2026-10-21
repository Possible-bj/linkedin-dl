"""Parses the HLS segment URLs collected from the browser console.

A LinkedIn segment URL looks like
  .../playlist/vid/v2/<asset>/<rendition>/<key>/<index>/<id>?e=...&t=...
where <rendition> is e.g. "hls-av1-540p-quality-analysis" and <index> the
segment number (1 is the init segment that the others need).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

_PATTERN = re.compile(r"/playlist/vid/v2/[^/]+/(?P<rendition>[^/]+)/[^/]+/(?P<index>\d+)/")
_HEIGHT = re.compile(r"(\d{3,4})p")


@dataclass(frozen=True)
class Segment:
    url: str
    rendition: str
    index: int


@dataclass
class Track:
    rendition: str
    segments: List[Segment]

    @property
    def height(self) -> int:
        match = _HEIGHT.search(self.rendition)
        return int(match.group(1)) if match else 0

    @property
    def is_audio(self) -> bool:
        return "audio" in self.rendition.lower()


class SegmentParser:
    def extract_urls(self, text: str) -> List[str]:
        """Accepts the console's JSON array, one URL per line, or a mix."""
        return re.findall(r"https://dms\.licdn\.com/playlist/vid/[^\"'\s,\]]+", text)

    def parse(self, urls: List[str]) -> List[Track]:
        groups: Dict[str, Dict[int, Segment]] = {}
        for url in urls:
            match = _PATTERN.search(url)
            if match is None:
                continue
            seg = Segment(url, match["rendition"], int(match["index"]))
            groups.setdefault(seg.rendition, {})[seg.index] = seg  # drops duplicates
        return [Track(name, [s[i] for i in sorted(s)]) for name, s in groups.items()]

    def best_video(self, tracks: List[Track]) -> Track:
        videos = [t for t in tracks if not t.is_audio]
        if not videos:
            raise ValueError("No video segment URLs found in the input")
        return max(videos, key=lambda t: (t.height, len(t.segments)))

    def best_audio(self, tracks: List[Track]) -> Optional[Track]:
        audios = [t for t in tracks if t.is_audio]
        return max(audios, key=lambda t: len(t.segments)) if audios else None

    def missing_indexes(self, track: Track) -> List[int]:
        present = {s.index for s in track.segments}
        return [i for i in range(1, max(present) + 1) if i not in present]

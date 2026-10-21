"""Fallback route: download HLS segments and join them into one file per track."""
from __future__ import annotations

import urllib.request
from pathlib import Path

from .segments import Track

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/141.0 Safari/537.36",
    "Referer": "https://www.linkedin.com/",
    "Origin": "https://www.linkedin.com",
}


class SegmentDownloader:
    def __init__(self, timeout: float = 30.0) -> None:
        self._timeout = timeout

    def download(self, track: Track, output: Path) -> Path:
        with output.open("wb") as out:
            for seg in track.segments:
                out.write(self._fetch(seg.url))
                print(f"  {track.rendition}: segment {seg.index}/{track.segments[-1].index}")
        return output

    def _fetch(self, url: str) -> bytes:
        request = urllib.request.Request(url, headers=_HEADERS)
        with urllib.request.urlopen(request, timeout=self._timeout) as response:
            return response.read()

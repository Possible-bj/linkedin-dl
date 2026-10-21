"""Main route: let yt-dlp find and fetch the video from the post link."""
from __future__ import annotations

from pathlib import Path

from .tools import ToolRunner


class PostDownloader:
    def __init__(self, runner: ToolRunner, browser: str = "chrome") -> None:
        self._runner = runner
        self._browser = browser

    def download(self, post_url: str, workdir: Path) -> Path:
        self._runner.run([
            "yt-dlp",
            "--cookies-from-browser", self._browser,
            "--format", "bestvideo*+bestaudio/best",
            "--merge-output-format", "mp4",
            "--output", str(workdir / "%(title).80B.%(ext)s"),
            "--no-playlist",
            post_url,
        ])
        files = sorted(workdir.glob("*.mp4"))
        if not files:
            raise FileNotFoundError("yt-dlp finished but produced no .mp4 file")
        return files[0]

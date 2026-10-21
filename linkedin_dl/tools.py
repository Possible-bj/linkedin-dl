"""Runs the external programs (yt-dlp, ffmpeg, ffprobe) the tool relies on."""
from __future__ import annotations

import shutil
import subprocess
from typing import List


class ToolError(RuntimeError):
    pass


class ToolRunner:
    def require(self, name: str) -> str:
        path = shutil.which(name)
        if path is None:
            raise ToolError(f"'{name}' is not installed. Run: brew install {name}")
        return path

    def run(self, args: List[str]) -> None:
        self.require(args[0])
        result = subprocess.run(args)
        if result.returncode != 0:
            raise ToolError(f"{args[0]} failed (exit code {result.returncode})")

    def output(self, args: List[str]) -> str:
        self.require(args[0])
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            raise ToolError(f"{args[0]} failed: {result.stderr.strip()}")
        return result.stdout

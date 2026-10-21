"""Turns downloaded tracks into one H.264/AAC MP4 that QuickTime and X accept."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from .tools import ToolRunner


class Converter:
    def __init__(self, runner: ToolRunner) -> None:
        self._runner = runner

    def to_h264(self, video: Path, output: Path, audio: Optional[Path] = None) -> Path:
        args = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", str(video)]
        if audio is not None:
            args += ["-i", str(audio), "-map", "0:v:0", "-map", "1:a:0"]
        else:
            args += ["-map", "0:v:0", "-map", "0:a:0?"]
        args += [
            "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart",
            str(output),
        ]
        self._runner.run(args)
        return output

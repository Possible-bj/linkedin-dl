"""Wires the two download routes to the converter and names the final file."""
from __future__ import annotations

import tempfile
from datetime import datetime
from pathlib import Path

from .converter import Converter
from .post_downloader import PostDownloader
from .segment_downloader import SegmentDownloader
from .segments import SegmentParser


class App:
    def __init__(self, post_downloader: PostDownloader, segment_downloader: SegmentDownloader,
                 parser: SegmentParser, converter: Converter, output_dir: Path) -> None:
        self._posts = post_downloader
        self._segments = segment_downloader
        self._parser = parser
        self._converter = converter
        self._output_dir = output_dir

    def from_post(self, post_url: str) -> Path:
        with tempfile.TemporaryDirectory() as tmp:
            original = self._posts.download(post_url, Path(tmp))
            return self._converter.to_h264(original, self._target(original.stem))

    def from_segments(self, text: str) -> Path:
        tracks = self._parser.parse(self._parser.extract_urls(text))
        video = self._parser.best_video(tracks)
        audio = self._parser.best_audio(tracks)
        for track in filter(None, [video, audio]):
            missing = self._parser.missing_indexes(track)
            if missing:
                raise ValueError(f"{track.rendition} is missing segments {missing}; "
                                 "play the video to the end and collect the URLs again")
        if audio is None:
            print("Note: no audio segments in the input, so the video will be silent.")
        with tempfile.TemporaryDirectory() as tmp:
            video_file = self._segments.download(video, Path(tmp) / "video.mp4")
            audio_file = self._segments.download(audio, Path(tmp) / "audio.mp4") if audio else None
            name = f"linkedin-video-{datetime.now():%Y%m%d-%H%M%S}"
            return self._converter.to_h264(video_file, self._target(name), audio_file)

    def _target(self, stem: str) -> Path:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        path = self._output_dir / f"{stem}.mp4"
        n = 2
        while path.exists():
            path = self._output_dir / f"{stem}-{n}.mp4"
            n += 1
        return path

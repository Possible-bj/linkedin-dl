"""Command line: linkedin-dl <post-url> | --segments FILE|- | --print-script."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .app import App
from .converter import Converter
from .post_downloader import PostDownloader
from .segment_downloader import SegmentDownloader
from .segments import SegmentParser
from .tools import ToolError, ToolRunner

_SCRIPT = Path(__file__).with_name("console_script.js")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="linkedin-dl", description="Download a LinkedIn video as H.264 MP4.")
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("post_url", nargs="?", help="link to the LinkedIn post")
    source.add_argument("--segments", metavar="FILE", help="segment URLs from the console script ('-' = stdin)")
    source.add_argument("--print-script", action="store_true", help="print the DevTools console script")
    p.add_argument("-o", "--output-dir", type=Path, default=Path.home() / "Downloads")
    p.add_argument("--browser", default="chrome", help="browser to borrow LinkedIn cookies from")
    return p


def _read(source: str) -> str:
    return sys.stdin.read() if source == "-" else Path(source).read_text()


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.print_script:
        print(_SCRIPT.read_text())
        return 0
    runner = ToolRunner()
    app = App(PostDownloader(runner, args.browser), SegmentDownloader(), SegmentParser(),
              Converter(runner), args.output_dir)
    try:
        result = app.from_segments(_read(args.segments)) if args.segments else app.from_post(args.post_url)
    except (ToolError, ValueError, FileNotFoundError, OSError) as error:
        print(f"linkedin-dl: {error}", file=sys.stderr)
        if args.post_url:
            print("If yt-dlp can't handle this post, use the fallback: linkedin-dl --print-script",
                  file=sys.stderr)
        return 1
    print(f"Saved: {result}")
    return 0

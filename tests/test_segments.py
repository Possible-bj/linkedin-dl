import json
import unittest

from linkedin_dl.segments import SegmentParser

BASE = "https://dms.licdn.com/playlist/vid/v2/ASSET/{r}/KEY/{i}/123?e=1&v=beta&t=tok{i}"


def url(rendition: str, index: int) -> str:
    return BASE.format(r=rendition, i=index)


class SegmentParserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = SegmentParser()

    def test_extracts_urls_from_console_json(self) -> None:
        text = json.dumps([url("hls-av1-540p", 1), url("hls-av1-540p", 2)], indent=4)
        self.assertEqual(self.parser.extract_urls(text), [url("hls-av1-540p", 1), url("hls-av1-540p", 2)])

    def test_orders_segments_numerically_and_drops_duplicates(self) -> None:
        urls = [url("hls-av1-540p", i) for i in (10, 2, 1, 2, 11)]
        track, = self.parser.parse(urls)
        self.assertEqual([s.index for s in track.segments], [1, 2, 10, 11])

    def test_picks_highest_video_and_separates_audio(self) -> None:
        urls = [url("hls-av1-540p", 1), url("hls-av1-720p", 1), url("hls-audio-aac", 1)]
        tracks = self.parser.parse(urls)
        self.assertEqual(self.parser.best_video(tracks).rendition, "hls-av1-720p")
        self.assertEqual(self.parser.best_audio(tracks).rendition, "hls-audio-aac")

    def test_reports_missing_segments(self) -> None:
        track, = self.parser.parse([url("hls-av1-540p", i) for i in (1, 2, 5)])
        self.assertEqual(self.parser.missing_indexes(track), [3, 4])

    def test_rejects_input_without_video(self) -> None:
        with self.assertRaises(ValueError):
            self.parser.best_video(self.parser.parse(["https://example.com/x"]))


if __name__ == "__main__":
    unittest.main()

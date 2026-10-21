# linkedin-dl

Downloads a LinkedIn post's video and saves it as an H.264 MP4 that QuickTime,
iMovie, phones and X accept.

> Only download videos you own or have permission to use, and credit the
> creator when you share them. Respect LinkedIn's terms and copyright law.

## Requirements

- macOS with Python 3.9+ (the system `python3` is fine)
- `brew install ffmpeg yt-dlp`

## Install

```bash
git clone https://github.com/Possible-bj/linkedin-dl.git
cd linkedin-dl
mkdir -p ~/.local/bin
ln -sf "$PWD/bin/linkedin-dl" ~/.local/bin/linkedin-dl
```

`~/.local/bin` must be on your `PATH`. No virtualenv or `pip install` is needed;
the tool uses only the standard library.

## Usage

### 1. From the post link (normal route)

On the post, open the `…` menu, choose **Copy link to post**, then:

```bash
linkedin-dl "https://www.linkedin.com/posts/..."
```

yt-dlp uses your Chrome login to find the best quality and the sound. The first
run shows a macOS Keychain prompt asking to let it read Chrome's cookies; allow it.
Use `--browser safari` (or `firefox`, `brave`, …) if you're logged in elsewhere.

### 2. From the browser (fallback, if route 1 fails)

1. Open the post in Chrome, open DevTools (⌥⌘I) and go to **Console**.
2. **Play the video to the end**, because only the pieces that have loaded get collected.
3. Paste the console script and press Enter. To print it:
   ```bash
   linkedin-dl --print-script
   ```
   It copies the segment URLs to your clipboard.
4. Run:
   ```bash
   pbpaste | linkedin-dl --segments -
   ```
   or save the list to a file and run `linkedin-dl --segments urls.json`.

The URLs are signed and expire after a few days, so run step 4 soon after step 3.

### Options

| Option | Default | Meaning |
|---|---|---|
| `-o`, `--output-dir DIR` | `~/Downloads` | Where the MP4 is saved |
| `--browser NAME` | `chrome` | Browser whose LinkedIn login yt-dlp uses (route 1) |

Existing files are never overwritten; a `-2`, `-3`, … suffix is added instead.

## Troubleshooting

| Message | Fix |
|---|---|
| `'ffmpeg' is not installed` | `brew install ffmpeg yt-dlp` |
| yt-dlp error on a post link | `brew upgrade yt-dlp`, then retry; otherwise use route 2 |
| `… is missing segments [...]` | Play the video to the end, run the console script again |
| `no audio segments … silent` | The post has no sound, or its audio didn't load; play it with sound on and collect again |
| HTTP 403 on segments | The URLs expired; collect them again |

## Tests

```bash
python3 -m unittest discover -s tests -t .
```

## Layout

| File | Responsibility |
|---|---|
| `linkedin_dl/cli.py` | Command-line arguments |
| `linkedin_dl/app.py` | Chooses the route, names the output file |
| `linkedin_dl/post_downloader.py` | Route 1: yt-dlp |
| `linkedin_dl/segments.py` | Parses and orders the console's segment URLs |
| `linkedin_dl/segment_downloader.py` | Route 2: downloads and joins segments |
| `linkedin_dl/converter.py` | ffmpeg conversion to H.264/AAC |
| `linkedin_dl/tools.py` | Runs external programs |
| `linkedin_dl/console_script.js` | DevTools script that collects segment URLs |

## License

MIT, see [LICENSE](LICENSE).

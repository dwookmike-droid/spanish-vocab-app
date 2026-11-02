#!/usr/bin/env python3
"""Voice every line the app needs with Gemini TTS (Castilian Spanish) and save mp3s to webapp/content/audio/.

Run build_data.py first (it writes content/audio_manifest.json), then this, then build_data.py again.
The API key is read from the GEMINI_API_KEY environment variable and is never written to disk.

Usage: GEMINI_API_KEY=... python3 webapp/tools/gen_audio_gemini.py [--limit N] [--workers 4]
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
OUT = APP / "content/audio"
MANIFEST = APP / "content/audio_manifest.json"
MODEL = "gemini-3.8-flash-tts"
STYLE = "Lee en español de España (castellano), con voz natural y clara, a ritmo tranquilo:"


def synth(key, text, voice, dest):
    body = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}},
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
    for attempt in range(5):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=120))
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and attempt < 4:
                time.sleep(5 * 2 ** attempt)
                continue
            raise RuntimeError(f"HTTP {e.code}: {e.read()[:200]!r}") from None
    part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
    data = base64.b64decode(part["data"])
    mime = part.get("mimeType", "")
    src = ["-i", "-"] if "wav" in mime and data[:4] == b"RIFF" else ["-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "-"]
    tmp = dest.with_suffix(".tmp.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src, "-af", "silenceremove=start_periods=1:start_threshold=-50dB",
                    "-ac", "1", "-ar", "24000", "-b:a", "48k", str(tmp)], input=data, check=True)
    tmp.rename(dest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set")
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(n, j) for n, j in json.loads(MANIFEST.read_text(encoding="utf-8")).items() if not (OUT / n).exists()]
    if a.limit:
        jobs = jobs[:a.limit]
    print(f"{len(jobs)} lines to voice")
    done = failed = 0
    with ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(synth, key, j["text"], j["voice"], OUT / n): n for n, j in jobs}
        for f in as_completed(futs):
            try:
                f.result(); done += 1
            except Exception as e:  # keep going; rerun picks up what is missing
                failed += 1
                print("FAIL", futs[f], e, file=sys.stderr)
            if (done + failed) % 25 == 0:
                print(f"  {done + failed}/{len(jobs)} (failed {failed})", flush=True)
    print(f"done {done}, failed {failed}")


if __name__ == "__main__":
    main()

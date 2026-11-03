#!/usr/bin/env python3
"""Voice every line in content/audio_manifest.json with Kokoro (open model, runs locally, free) and save mp3s to
content/audio/. Three Spanish voices are mixed (ef_dora, em_alex, em_santa); build_data.py decides who says what.

  pip install kokoro-onnx soundfile        # once
  python3 webapp/tools/build_data.py       # writes the manifest
  python3 webapp/tools/gen_audio_kokoro.py # makes the missing mp3s (model files download on first run, ~350 MB)
  python3 webapp/tools/build_data.py       # picks them up
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
OUT = APP / "content/audio"
MANIFEST = APP / "content/audio_manifest.json"
CACHE = APP / ".cache/kokoro"
FILES = {
    "kokoro-v1.0.onnx": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx",
    "voices-v1.0.bin": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin",
}
SPEED = 0.92  # a touch slower than conversational, for learners


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, url in FILES.items():
        if not (CACHE / name).exists():
            print("downloading", name)
            urllib.request.urlretrieve(url, CACHE / name)
    from kokoro_onnx import Kokoro
    import soundfile as sf

    k = Kokoro(str(CACHE / "kokoro-v1.0.onnx"), str(CACHE / "voices-v1.0.bin"))
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [(n, j) for n, j in json.loads(MANIFEST.read_text(encoding="utf-8")).items() if not (OUT / n).exists()]
    print(f"{len(jobs)} lines to voice")
    for i, (name, job) in enumerate(jobs, 1):
        audio, sr = k.create(job["text"], voice=job["voice"], speed=SPEED, lang="es")
        wav = OUT / (name + ".wav")
        sf.write(wav, audio, sr)
        # trim leading/trailing silence, mono 24 kHz MP3 48 kbps (same weight as the v6 files)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.15",
                        "-ac", "1", "-ar", "24000", "-b:a", "48k", str(OUT / name)], check=True)
        wav.unlink()
        if i % 25 == 0 or i == len(jobs):
            print(f"  {i}/{len(jobs)}", flush=True)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build the web app's data and media from the project's text YAML and v6 web exports.

Reads (never modifies):
  es/chNN/text/chNN_text.yaml           printed-book text (words, word order, practice, scenes)
  webapp/content/chNN_extra.yaml        web-only dialogues, readings, glossary
  design/deliverables/v6/web/           v6 web export (ch01, ch02, ch11 images + audio)
  es/chNN/design/web_chNN.zip           per-chapter web exports (ch02~ch07)
  design/docs/CREDITS_v6.md, es/chNN/design/CREDITS_chNN_v6.md   photo credits

Writes:
  webapp/data/chapters.json, webapp/data/chNN.json
  webapp/media/img/*.webp, webapp/media/audio/*.mp3, webapp/media/credits/*.md

Audio files are named es_<md5("es"+text)[:10]>.mp3 (same rule as design/build/v6/web_v6.py),
so any sentence that was voiced in v6 gets its mp3; the rest fall back to browser TTS.

Usage: python3 webapp/tools/build_data.py
"""
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "webapp"
CHAPTERS = [1, 2, 3, 4, 5, 6, 7, 8, 11]
V6_WEB = ROOT / "design/deliverables/v6/web"

IMG_OUT = APP / "media/img"
AUDIO_OUT = APP / "media/audio"
CREDITS_OUT = APP / "media/credits"
DATA_OUT = APP / "data"


ARTICLES = {
    "el": {"lemma": "el", "ko": "그 (남성 단수 정관사)", "en": "the", "pron": "엘"},
    "la": {"lemma": "el", "ko": "그 (여성 단수 정관사)", "en": "the", "pron": "라"},
    "los": {"lemma": "el", "ko": "그 (남성 복수 정관사)", "en": "the", "pron": "로스"},
    "las": {"lemma": "el", "ko": "그 (여성 복수 정관사)", "en": "the", "pron": "라스"},
    "un": {"lemma": "uno", "ko": "하나의 (남성 부정관사)", "en": "a, an", "pron": "**운**"},
    "una": {"lemma": "uno", "ko": "하나의 (여성 부정관사)", "en": "a, an", "pron": "**우**나"},
    "unos": {"lemma": "uno", "ko": "몇몇의 (남성 복수)", "en": "some", "pron": "**우**노스"},
    "unas": {"lemma": "uno", "ko": "몇몇의 (여성 복수)", "en": "some", "pron": "**우**나스"},
}


def audio_name(text):
    return "es_" + hashlib.md5(("es" + text).encode()).hexdigest()[:10] + ".mp3"


def collect_media():
    """Copy every image/audio file from the v6 export and chapter zips. Returns (imgs, audios)."""
    for d in (IMG_OUT, AUDIO_OUT, CREDITS_OUT, DATA_OUT):
        if d.exists() and d != DATA_OUT:
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

    def take(name, data):
        if name.endswith(".webp"):
            (IMG_OUT / name).write_bytes(data)
        elif name.endswith(".mp3"):
            (AUDIO_OUT / name).write_bytes(data)

    for sub in ("img", "audio"):
        for f in (V6_WEB / sub).glob("*"):
            take(f.name, f.read_bytes())
    # chapter zips are newer than the combined v6 export, so they overwrite it
    for z in sorted(ROOT.glob("es/ch*/design/web_ch*.zip")):
        with zipfile.ZipFile(z) as zf:
            for info in zf.infolist():
                name = info.filename.rsplit("/", 1)[-1]
                if "/img/" in "/" + info.filename or "/audio/" in "/" + info.filename:
                    take(name, zf.read(info))

    credits = [ROOT / "design/docs/CREDITS_v6.md"] + sorted(ROOT.glob("es/ch*/design/CREDITS_ch*_v6.md"))
    for c in credits:
        shutil.copy(c, CREDITS_OUT / c.name)

    imgs = {f.name for f in IMG_OUT.iterdir()}
    audios = {f.name for f in AUDIO_OUT.iterdir()}
    return imgs, audios, [c.name for c in credits]


def build_chapter(num, imgs, audios):
    nn = f"{num:02d}"
    text = yaml.safe_load((ROOT / f"es/ch{nn}/text/ch{nn}_text.yaml").read_text(encoding="utf-8"))
    extra_p = APP / f"content/ch{nn}_extra.yaml"
    extra = yaml.safe_load(extra_p.read_text(encoding="utf-8")) if extra_p.exists() else {}

    stats = {"audio_hit": 0, "audio_miss": 0}

    def au(s):
        """Attach an mp3 name when one exists for this Spanish text."""
        if not s:
            return None
        n = audio_name(s)
        if n in audios:
            stats["audio_hit"] += 1
            return n
        stats["audio_miss"] += 1
        return None

    def sent(d, *keep):
        out = {k: d.get(k) for k in keep if d.get(k) not in (None, "", [])}
        out["audio"] = au(d.get("es"))
        return out

    words = []
    for w in text["words"]:
        img = None
        for cand in (f"ch{nn}_{w['key']}", f"ch{nn}_c_{w['key']}"):
            if f"{cand}_1x.webp" in imgs:
                img = cand
                break
        ex = w.get("example")
        words.append({
            "key": w["key"], "es": w["es"], "base": w.get("base"), "gender": w.get("gender"),
            "pron": w.get("pron"), "en": w.get("en"), "ko": w.get("ko"), "core": bool(w.get("core")),
            "note": w.get("note") or None, "img": img, "audio": au(w["es"]),
            "example": sent(ex, "es", "en", "ko") if ex else None,
        })

    wo = text.get("word_order") or {}
    word_order = {
        "tema": wo.get("tema"), "tema_sub_ko": wo.get("tema_sub_ko"), "point_ko": wo.get("point_ko"),
        "lead_ko": wo.get("lead_ko"),
        "sentences": [dict(sent(s, "es", "en", "ko", "note_ko"), tokens=s.get("tokens"), highlight=s.get("highlight", []))
                      for s in wo.get("sentences", [])],
        "patterns": wo.get("patterns") or [],
        "contrast": wo.get("contrast"),
        "subject": wo.get("subject"),
        "extra_notes_ko": wo.get("extra_notes_ko") or [],
    }

    dialogues = []
    for d in extra.get("dialogues", []):
        lines = []
        for ln in d.get("lines", []):
            lines.append({"who": ln["who"],
                          "textbook": sent(ln["textbook"], "es", "ko"),
                          "native": sent(ln["native"], "es", "ko", "note_ko")})
        dialogues.append({k: d.get(k) for k in ("id", "title_es", "title_ko", "setting_ko", "roles")} | {"lines": lines})

    readings = []
    for r in extra.get("readings", []):
        readings.append({k: r.get(k) for k in ("id", "title_es", "title_ko", "level", "questions")}
                        | {"paragraphs": [sent(p, "es", "ko") for p in r.get("paragraphs", [])]})

    # glossary: chapter words (by every token of es/base) + extra glossary
    glossary = {}
    for w in text["words"]:
        entry = {"lemma": w.get("base") or w["es"], "ko": w.get("ko"), "en": w.get("en"), "pron": w.get("pron"),
                 "es": w["es"], "key": w["key"]}
        glossary[w["es"].lower()] = entry
        glossary.setdefault((w.get("base") or "").lower(), entry)
    for k, v in (extra.get("glossary") or {}).items():
        glossary[str(k).lower()] = v
    # articles are part of the chapter words ("la toalla"), so the content checker never asks for them
    for k, v in ARTICLES.items():
        glossary.setdefault(k, v)

    ch = text["chapter"]
    data = {
        "num": num, "es": ch["es"], "en": ch["en"], "ko": ch["ko"], "city": ch["city"], "date": ch["date"],
        "opener": text.get("opener"),
        "words": words,
        "word_order": word_order,
        "practice": [sent({"es": p["answer"], **p}, "tiles", "answer", "ko") for p in text.get("practice", [])],
        "variants": text.get("variants") or [],
        "scenes": [sent(s, "es", "en", "ko") for s in text.get("scenes", [])],
        "extras": text.get("extras") or {},
        "dialogues": dialogues,
        "readings": readings,
        "glossary": {k: v for k, v in glossary.items() if k},
    }
    (DATA_OUT / f"ch{nn}.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    summary = {"num": num, "es": ch["es"], "en": ch["en"], "ko": ch["ko"], "city": ch["city"], "date": ch["date"],
               "cover": next((w["img"] for w in words if w["img"]), None),
               "has_media": any(w["img"] for w in words),
               "n_dialogues": len(dialogues), "n_readings": len(readings)}
    return summary, stats


def main():
    imgs, audios, credits = collect_media()
    chapters = []
    for n in CHAPTERS:
        summary, st = build_chapter(n, imgs, audios)
        chapters.append(summary)
        print(f"ch{n:02d} {summary['es']:<22} img={'y' if summary['has_media'] else 'n'} "
              f"dlg={summary['n_dialogues']} rd={summary['n_readings']} audio {st['audio_hit']} mp3 / {st['audio_miss']} TTS")
    (DATA_OUT / "chapters.json").write_text(
        json.dumps({"chapters": chapters, "credits": credits}, ensure_ascii=False, indent=1), encoding="utf-8")
    size = sum(f.stat().st_size for f in (APP / "media").rglob("*") if f.is_file())
    print(f"media: {len(imgs)} images, {len(audios)} audio, {size/1e6:.1f} MB")


if __name__ == "__main__":
    main()

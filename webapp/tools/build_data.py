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
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "webapp"
CHAPTERS = list(range(1, 25))   # every chapter that has es/chNN/text/chNN_text.yaml
V6_WEB = ROOT / "design/deliverables/v6/web"
VOICE_DIR = APP / "content/audio"         # mp3s made by gen_audio_kokoro.py (source, kept in git)
MANIFEST = APP / "content/audio_manifest.json"   # every line that still needs a voice: name -> text, voice
# Kokoro voices, mixed: one female, two male. Lines are spread across them so the app does not sound like one reader.
KOKORO_VOICES = ["ef_dora", "em_alex", "em_santa"]
NARRATOR = None   # None = pick a voice from the text (stable), so single lines rotate between the three

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


def voice_name(text, voice):
    return "kk_" + hashlib.md5(f"{voice}|{text}".encode()).hexdigest()[:10] + ".mp3"


def pick_voice(seed):
    return KOKORO_VOICES[int(hashlib.md5(seed.encode()).hexdigest(), 16) % len(KOKORO_VOICES)]


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
    credits += design_photos()

    imgs = {f.name for f in IMG_OUT.iterdir()}
    audios = {f.name for f in AUDIO_OUT.iterdir()}
    return imgs, audios, [c.name for c in credits]


WANTED = {}


def design_photos():
    """Word photos from Claude Code's print-design folders (claude_design/chNN/img/<word key>.jpg + credits.json),
    for chapters that have no v6 web export. Writes chNN_<key>_2x.webp and a credits page; returns its path."""
    out = []
    for cdir in sorted(ROOT.glob("claude_design/ch[0-9][0-9]")):
        nn = cdir.name[2:]
        text_p = ROOT / f"es/ch{nn}/text/ch{nn}_text.yaml"
        cred_p = cdir / "credits.json"
        if not text_p.exists() or not cred_p.exists():
            continue
        keys = [w["key"] for w in yaml.safe_load(text_p.read_text(encoding="utf-8"))["words"]]
        cred = json.loads(cred_p.read_text(encoding="utf-8"))
        rows = []
        for k in keys:
            src = cdir / "img" / f"{k}.jpg"
            dst = IMG_OUT / f"ch{nn}_{k}_2x.webp"
            if not src.exists() or (dst.exists()):
                continue
            # 240 px tall: sharp at the app's 120 px on 2x screens
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", "scale=-2:240",
                            "-c:v", "libwebp", "-quality", "80", str(dst)], check=True)
            c = cred.get(k) or {}
            rows.append(f"| {k} | {c.get('title', '').removeprefix('File:')} | {c.get('artist', '')} | {c.get('lic', '')} | {c.get('page', '')} |")
        if rows:
            md = CREDITS_OUT / f"CREDITS_ch{nn}_web.md"
            md.write_text(f"# ch{nn} 단어 사진 (웹앱)\n\nWikimedia Commons 또는 Openverse(Flickr 등)에서 받은 CC·퍼블릭 도메인 사진이에요. 웹용으로 줄이고 잘랐어요.\n\n"
                          "| 단어 | 파일 | 저자 | 라이선스 | 링크 |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")
            out.append(md)
    return out


def build_chapter(num, imgs, audios):
    nn = f"{num:02d}"
    text = yaml.safe_load((ROOT / f"es/ch{nn}/text/ch{nn}_text.yaml").read_text(encoding="utf-8"))
    extra_p = APP / f"content/ch{nn}_extra.yaml"
    extra = yaml.safe_load(extra_p.read_text(encoding="utf-8")) if extra_p.exists() else {}

    stats = {"audio_hit": 0, "audio_miss": 0}

    def au(s, voice=NARRATOR, prefer_v6=True):
        """Attach an mp3 for this Spanish text: the v6 recording when it exists (narrated lines only),
        otherwise a Kokoro voice; with neither, the app falls back to the device's TTS."""
        if not s:
            return None
        n = audio_name(s)
        if prefer_v6 and n in audios:
            stats["audio_hit"] += 1
            return n
        v = voice or pick_voice(s)
        g = voice_name(s, v)
        if (VOICE_DIR / g).exists():
            shutil.copy(VOICE_DIR / g, AUDIO_OUT / g)
            audios.add(g)
            stats["audio_hit"] += 1
            return g
        WANTED[g] = {"text": s, "voice": v}
        stats["audio_miss"] += 1
        return None

    def sent(d, *keep, voice=NARRATOR, prefer_v6=True):
        out = {k: d.get(k) for k in keep if d.get(k) not in (None, "", [])}
        out["audio"] = au(d.get("es"), voice, prefer_v6)
        return out

    words = []
    for w in text["words"]:
        img = None
        for cand in (f"ch{nn}_{w['key']}", f"ch{nn}_c_{w['key']}"):
            if f"{cand}_2x.webp" in imgs:
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
    for di, d in enumerate(extra.get("dialogues", [])):
        # two different voices per dialogue: the female voice and one of the male voices, swapping sides by dialogue
        male = KOKORO_VOICES[1 + (num + di) % 2]
        roles = {"A": male, "B": "ef_dora"} if (num + di) % 2 == 0 else {"A": "ef_dora", "B": male}
        lines = []
        for ln in d.get("lines", []):
            v = roles.get(ln["who"], "ef_dora")
            lines.append({"who": ln["who"],
                          "textbook": sent(ln["textbook"], "es", "ko", voice=v, prefer_v6=False),
                          "native": sent(ln["native"], "es", "ko", "note_ko", voice=v, prefer_v6=False)})
        dialogues.append({k: d.get(k) for k in ("id", "title_es", "title_ko", "setting_ko", "roles")} | {"lines": lines})

    readings = []
    for ri, r in enumerate(extra.get("readings", [])):
        rv = KOKORO_VOICES[(num + ri) % len(KOKORO_VOICES)]   # one reader per text
        readings.append({k: r.get(k) for k in ("id", "title_es", "title_ko", "level", "questions")}
                        | {"paragraphs": [sent(p, "es", "ko", voice=rv, prefer_v6=False) for p in r.get("paragraphs", [])]})

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
    # a voice for every tappable word form (chapter words already carry their own audio)
    for k, v in glossary.items():
        if k and not v.get("key"):
            glossary[k] = {**v, "audio": au(k)}

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
    MANIFEST.write_text(json.dumps(WANTED, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")
    print(f"lines without a voice yet: {len(WANTED)} (run gen_audio_kokoro.py, then build again)")

    # keep only the media the app references: one image per word (the 2x file, shown scaled down,
    # stays sharp on phones) and the mp3s that match a sentence
    used = "".join(f.read_text(encoding="utf-8") for f in DATA_OUT.glob("ch*.json"))
    used_img = set(re.findall(r'"img":"([^"]+)"', used))
    used_audio = set(re.findall(r"(?:es|kk)_[0-9a-f]{10}\.mp3", used))
    for f in list(IMG_OUT.iterdir()):
        stem = f.name.removesuffix("_2x.webp")
        if f.name.endswith("_2x.webp") and stem in used_img:
            f.rename(IMG_OUT / f"{stem}.webp")
        else:
            f.unlink()
    for f in list(AUDIO_OUT.iterdir()):
        if f.name not in used_audio:
            f.unlink()
    imgs = {f.name for f in IMG_OUT.iterdir()}
    audios = {f.name for f in AUDIO_OUT.iterdir()}

    # one script with every JSON + credits text, so index.html also works when opened as a file (file://),
    # where browsers block fetch()
    bundle = {f.name: json.loads(f.read_text(encoding="utf-8")) for f in sorted(DATA_OUT.glob("*.json"))}
    bundle["credits"] = {c: (CREDITS_OUT / c).read_text(encoding="utf-8") for c in credits}
    (DATA_OUT / "bundle.js").write_text(
        "window.VV_DATA=" + json.dumps(bundle, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    size = sum(f.stat().st_size for f in (APP / "media").rglob("*") if f.is_file())
    print(f"media: {len(imgs)} images, {len(audios)} audio, {size/1e6:.1f} MB")
    if "--preview" in sys.argv:
        build_preview(Path(sys.argv[sys.argv.index("--preview") + 1]), bundle)


def build_preview(out, bundle):
    """A copy of the site for hosts that cap the file count (claude.ai artifacts): audio is packed into one
    base64 script per chapter (data/audiopack_NN.js) instead of ~1,400 mp3 files."""
    if out.exists():
        shutil.rmtree(out)
    (out / "data").mkdir(parents=True)
    for f in ("index.html", "app.js", "app.css", "manifest.webmanifest"):
        shutil.copy(APP / f, out / f)
    shutil.copytree(APP / "icons", out / "icons")
    shutil.copytree(IMG_OUT, out / "media/img")
    index = {}
    for f in sorted(DATA_OUT.glob("ch[0-9][0-9].json")):
        k = f.stem[2:]
        names = sorted(set(re.findall(r"(?:es|kk)_[0-9a-f]{10}\.mp3", f.read_text(encoding="utf-8"))))
        pack = {n: base64.b64encode((AUDIO_OUT / n).read_bytes()).decode() for n in names}
        for n in names:
            index.setdefault(n, int(k))
        (out / f"data/audiopack_{k}.js").write_text(
            "window.VV_AUDIO=Object.assign(window.VV_AUDIO||{}," + json.dumps(pack, separators=(",", ":")) + ");\n")
    (out / "data/bundle.js").write_text(
        "window.VV_PACKED=true;window.VV_PACK_INDEX=" + json.dumps(index, separators=(",", ":")) + ";\n"
        + "window.VV_DATA=" + json.dumps(bundle, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    n = sum(1 for f in out.rglob("*") if f.is_file())
    print(f"preview: {out} ({n} files)")


if __name__ == "__main__":
    main()

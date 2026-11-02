#!/usr/bin/env python3
"""Validate webapp/content/chNN_extra.yaml (dialogues, readings, glossary coverage).

Usage: python3 webapp/tools/check_extra.py webapp/content/ch01_extra.yaml [...]
Exit code 1 when any error is found.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SPLIT = re.compile(r"[\s.,;:!?¡¿«»\"“”()\[\]—–…/]+")


def tokens(text):
    for t in SPLIT.split(text or ""):
        t = t.strip("'’-").lower()
        if t and not re.fullmatch(r"[\d:.,h%€]+", t):
            yield t


def chapter_words(num):
    p = ROOT / f"es/ch{num:02d}/text/ch{num:02d}_text.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    known = set()
    for w in d["words"]:
        for field in ("es", "base"):
            known.update(tokens(w.get(field, "")))
    return known


def check(path):
    errs, warns = [], []
    d = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    num = d.get("chapter")
    if not isinstance(num, int):
        return [f"chapter must be int, got {num!r}"], warns
    m = re.search(r"ch(\d\d)_extra", str(path))
    if m and int(m.group(1)) != num:
        errs.append(f"chapter {num} does not match file name")
    gl = d.get("glossary") or {}
    for k, v in gl.items():
        if k != k.lower():
            errs.append(f"glossary key not lowercase: {k}")
        for f in ("lemma", "ko", "en", "pron"):
            if not (v or {}).get(f):
                errs.append(f"glossary[{k}] missing {f}")
        if "<" in str((v or {}).get("pron", "")):
            errs.append(f"glossary[{k}] pron has HTML")
    known = chapter_words(num) | set(gl)
    used = {}

    def use(text, where):
        for t in tokens(text):
            used.setdefault(t, where)

    dias = d.get("dialogues") or []
    if len(dias) < 2:
        errs.append(f"need 2 dialogues, got {len(dias)}")
    for di in dias:
        did = di.get("id", "?")
        for f in ("id", "title_es", "title_ko", "setting_ko", "roles", "lines"):
            if not di.get(f):
                errs.append(f"dialogue {did}: missing {f}")
        if len(di.get("setting_ko", "")) > 60:
            warns.append(f"dialogue {did}: setting_ko > 60 chars")
        roles = di.get("roles") or {}
        lines = di.get("lines") or []
        if not 6 <= len(lines) <= 10:
            errs.append(f"dialogue {did}: lines must be 6~10, got {len(lines)}")
        for i, ln in enumerate(lines):
            if ln.get("who") not in roles:
                errs.append(f"dialogue {did} line {i}: who={ln.get('who')} not in roles")
            for ver in ("textbook", "native"):
                v = ln.get(ver) or {}
                if not v.get("es") or not v.get("ko"):
                    errs.append(f"dialogue {did} line {i}: {ver} needs es and ko")
                use(v.get("es", ""), f"{did}#{i}.{ver}")
            note = (ln.get("native") or {}).get("note_ko", "")
            if len(note) > 70:
                warns.append(f"dialogue {did} line {i}: note_ko > 70 chars")

    reads = d.get("readings") or []
    if len(reads) < 2:
        errs.append(f"need 2 readings, got {len(reads)}")
    for r in reads:
        rid = r.get("id", "?")
        for f in ("id", "title_es", "title_ko", "level", "paragraphs"):
            if not r.get(f):
                errs.append(f"reading {rid}: missing {f}")
        if r.get("level") not in ("A1", "A2"):
            errs.append(f"reading {rid}: level must be A1 or A2")
        n = 0
        for i, p in enumerate(r.get("paragraphs") or []):
            if not p.get("es") or not p.get("ko"):
                errs.append(f"reading {rid} para {i}: needs es and ko")
            n += len(list(tokens(p.get("es", ""))))
            use(p.get("es", ""), f"{rid}¶{i}")
        if not 60 <= n <= 140:
            warns.append(f"reading {rid}: {n} words (target 60~120)")
        for j, q in enumerate(r.get("questions") or []):
            ch = q.get("choices_ko") or []
            if not q.get("q_ko") or len(ch) < 2 or not isinstance(q.get("answer"), int) or not 0 <= q["answer"] < len(ch):
                errs.append(f"reading {rid} question {j}: bad q_ko/choices_ko/answer")

    missing = sorted(t for t in used if t not in known)
    for t in missing:
        errs.append(f"glossary missing word: {t!r} (first in {used[t]})")
    unused = sorted(k for k in gl if k not in used)
    if unused:
        warns.append(f"glossary keys never used: {', '.join(unused[:20])}")
    return errs, warns


def main():
    bad = 0
    for p in sys.argv[1:]:
        errs, warns = check(p)
        print(f"== {p}: {len(errs)} errors, {len(warns)} warnings")
        for e in errs:
            print("  ERROR", e)
        for w in warns:
            print("  warn ", w)
        bad += len(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

"""Grok Bot 빌드용 — Claude Code가 쓴 es/chNN/text/chNN_text.yaml을 v6 빌드 데이터 구조로 바꿔요.

  from text_import import load_chapter
  ch = load_chapter(ROOT, 3)
  ch['items']      -> v6 V3 형식 목록 (k, img, es, b, g, p(<b>강세</b>), en, ko, star, v, ex[es,en,ko])
  ch['order']      -> v6 data.json['order'] 형식 (adj/agree/de 대신 patterns 그대로 + sent/clitic/subj/practice/variants)
  ch['notes']      -> {key: note} (카드 메모, v6 NOTE1/NOTE02/NOTE11 형식)
  ch['opener'], ch['props'], ch['scenes'], ch['extras'], ch['chapter']

빌드 전에 tools/validate_text.py로 검증된 파일만 받아요(오류가 있으면 ValueError).
"""
import os, re, subprocess, sys, yaml

def md2b(s): return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s or "")

def load_chapter(root, num, lang="es", validate=True):
    path = os.path.join(root, lang, f"ch{num:02d}", "text", f"ch{num:02d}_text.yaml")
    if validate:
        p = subprocess.run([sys.executable, os.path.join(root, "tools/validate_text.py"), path], capture_output=True, text=True)
        if p.returncode: raise ValueError(f"검증 실패: {path}\n{p.stdout}")
    y = yaml.safe_load(open(path, encoding="utf-8"))
    items, notes = [], {}
    for w in y["words"]:
        it = dict(k=w["key"], img=f"{w['key']}.png", es=w["es"], b=w["base"], g=w["gender"], p=md2b(w["pron"]),
                  en=w["en"], ko=w["ko"], star=bool(w["core"]), v="")
        if w.get("example"): it["ex"] = [w["example"]["es"], w["example"]["en"], w["example"]["ko"]]
        if w.get("note"): notes[w["key"]] = w["note"]
        items.append(it)
    wo = y["word_order"]
    order = dict(
        sent=[dict(id=f"o{i+1}", b=[[t["es"], t["gloss_ko"]] for t in s["tokens"]], hi=s.get("highlight", []),
                   es=s["es"], en=s["en"], ko=s["ko"], note=s["note_ko"]) for i, s in enumerate(wo["sentences"])],
        patterns=wo.get("patterns", []),
        clitic=[[c["es"], c.get("label_ko", ""), c["ko"]] for c in (wo.get("contrast") or {}).get("items", [])],
        subj=[[c["es"], c["ko"]] for c in (wo.get("subject") or {}).get("items", [])],
        practice=[[p["tiles"], p["answer"], p["ko"]] for p in y["practice"]],
        variants=[[v["es"], v["alt"]] for v in y["variants"]])
    return dict(chapter=y["chapter"], opener=y["opener"], items=items, notes=notes, order=order,
                word_order=dict(tema=wo["tema"], sub=wo["tema_sub_ko"], point=wo["point_ko"], lead=wo["lead_ko"],
                                extra=wo.get("extra_notes_ko", [])),
                scenes=[[s["es"], s["en"], s["ko"]] for s in y["scenes"]], extras=y["extras"], props=y["props"])

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    ch = load_chapter(root, n)
    print(f"ch{n:02d}: 단어 {len(ch['items'])} · 핵심 {sum(i['star'] for i in ch['items'])} · 블록예문 {len(ch['order']['sent'])} · 연습 {len(ch['order']['practice'])} · 소품 {len(ch['props'])}")

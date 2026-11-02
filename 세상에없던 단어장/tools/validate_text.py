#!/usr/bin/env python3
"""세상에없던 단어장 — 텍스트 YAML 검증기.

사용법 (폴더 루트에서):
  python3 tools/validate_text.py es/ch03/text/ch03_text.yaml
  python3 tools/validate_text.py --all            # es/ch*/text/ch*_text.yaml 전부 + 장 사이 일관성
  python3 tools/validate_text.py FILE --humanizer # humanizer-kr 감사 스크립트까지 실행
  python3 tools/validate_text.py FILE --strict    # 경고도 실패로 처리

종료 코드: 0 = 통과, 1 = 오류 있음(또는 --strict에서 경고 있음).
필요: python3, PyYAML (pip3 install pyyaml).
"""
from __future__ import annotations
import argparse, glob, os, re, subprocess, sys, unicodedata
try:
    import yaml
except ImportError:
    sys.exit("PyYAML이 필요해요: pip3 install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIM = yaml.safe_load(open(os.path.join(ROOT, "schema/limits.yaml"), encoding="utf-8"))
PLAN = {c["num"]: c for c in yaml.safe_load(open(os.path.join(ROOT, "schema/plan_es.yaml"), encoding="utf-8"))["chapters"]}
HUMANIZER = os.path.join(ROOT, ".claude/skills/humanizer-kr/scripts/audit_korean_text.py")

CHO = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
JUNG = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
GLIDE = set("ㅑㅒㅕㅖㅛㅠ")
FUNC = {"el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "a", "al", "y", "e", "o", "u", "en", "con", "por", "para", "sin", "lo"}
FEM_EL = {"agua", "águila", "hacha", "aula", "arma", "alma", "hambre", "ave", "área"}
BRANDS = ["coca-cola", "pepsi", "zara", "mango", "mercadona", "el corte inglés", "carrefour", "starbucks", "mcdonald", "burger king", "telepizza",
          "nescafé", "nespresso", "cola cao", "colacao", "chupa chups", "mahou", "estrella damm", "cruzcampo", "san miguel", "tío pepe", "iberia",
          "vueling", "ryanair", "renfe", "alsa", "movistar", "vodafone", "ikea", "iphone", "samsung", "nike", "adidas", "decathlon",
          "uber", "cabify", "airbnb", "booking", "google", "nutella", "kleenex", "danone", "loewe", "desigual", "camper", "lacoste"]
LATAM = ["carro", "boleto", "celular", "computadora", "jugo", "manejar", "departamento", "lentes", "papas fritas", "frijol", "durazno", "elevador",
         "recámara", "regadera", "camión", "alberca", "chamarra", "cuadra", "ustedes vosotros"]
HANGUL = re.compile(r"[가-힣]")

def strip_md(s: str) -> str:
    return re.sub(r"\*\*", "", s or "")

def jamo(s: str):
    out = []
    for ch in s:
        o = ord(ch) - 0xAC00
        if 0 <= o < 11172:
            out.append((CHO[o // 588], JUNG[(o % 588) // 28], o % 28))
    return out

class Report:
    def __init__(self, name):
        self.name, self.err, self.warn = name, [], []
    def e(self, where, msg): self.err.append(f"[오류] {where}: {msg}")
    def w(self, where, msg): self.warn.append(f"[경고] {where}: {msg}")

def need(r, obj, key, where, typ=str):
    if not isinstance(obj, dict) or key not in obj:
        r.e(where, f"'{key}' 필드가 없어요"); return None
    v = obj[key]
    if typ is str and not isinstance(v, str):
        r.e(f"{where}.{key}", "문자열이어야 해요"); return None
    if typ is list and not isinstance(v, list):
        r.e(f"{where}.{key}", "목록이어야 해요"); return None
    if typ is dict and not isinstance(v, dict):
        r.e(f"{where}.{key}", "항목 묶음(dict)이어야 해요"); return None
    if typ is str and not v.strip() and key not in ("note",):
        r.e(f"{where}.{key}", "비어 있어요")
    return v

def length(r, val, limit, where):
    if isinstance(val, str) and len(strip_md(val)) > limit:
        r.e(where, f"{len(strip_md(val))}자 > 최대 {limit}자: «{strip_md(val)}»")

def spanish_checks(r, s, where, main=True):
    if not isinstance(s, str): return
    if s.count("¿") != s.count("?"): r.e(where, f"¿ … ? 짝이 안 맞아요: «{s}»")
    if s.count("¡") != s.count("!"): r.e(where, f"¡ … ! 짝이 안 맞아요: «{s}»")
    if "  " in s or s != s.strip(): r.w(where, "공백이 두 칸이거나 앞뒤 공백이 있어요")
    if re.search(r"['\"]", s): r.w(where, "곧은 따옴표 대신 « » 또는 ‘ ’를 써요")
    low = s.lower()
    if main:
        for t in LATAM:
            if re.search(rf"\b{re.escape(t)}\b", low): r.w(where, f"중남미 어휘로 보여요('{t}'). 본문은 스페인(카스티야) 표준으로 쓰고, 지역 변이는 variants/note에만 넣어요")

def sentence_checks(r, s, where):
    spanish_checks(r, s, where)
    if isinstance(s, str) and s and s[-1] not in ".?!…»":
        r.e(where, f"문장은 . ? ! 로 끝나야 해요: «{s}»")

def korean_checks(r, s, where, sentence=False):
    if not isinstance(s, str) or not s: return
    if re.search(r"(니다|십시오|하였다|했다|이다|한다)[.!?]?$", s.strip()): r.w(where, f"해요체가 아니에요(책 전체 해요체): «{s}»")
    for bad in ("박았", "발사", "쏩니다", "투입", "전개", "런칭"):
        if bad in s: r.e(where, f"금지 어휘 '{bad}'")
    if re.search(r"[\U0001F300-\U0001FAFF]", s): r.e(where, "이모지는 쓰지 않아요")
    if sentence and s[-1] not in ".?!…)": r.w(where, f"한국어 문장 끝 문장부호가 없어요: «{s}»")

def brand_check(r, text, where):
    low = text.lower()
    for b in BRANDS:
        if re.search(rf"(?<![a-záéíóúñ]){re.escape(b)}(?![a-záéíóúñ])", low):
            r.e(where, f"상표·브랜드명 '{b}'는 쓰지 않아요")

def pron_check(r, es, pron, where):
    if not isinstance(pron, str): return
    if re.search(r"[^가-힣\s\*]", pron): r.e(where, f"발음에는 한글·공백·** 만 써요: «{pron}»")
    if pron.count("**") % 2: r.e(where, f"** 짝이 안 맞아요: «{pron}»"); return
    et, pt = es.split(), pron.split()
    if len(et) != len(pt):
        r.e(where, f"단어 수가 달라요: 스페인어 {len(et)}개({es}) / 발음 {len(pt)}개({pron})"); return
    for w, p in zip(et, pt):
        n = len(re.findall(r"\*\*[^*]+\*\*", p))
        wl = w.lower().strip("¿?¡!.,")
        if wl in FUNC and n: r.e(where, f"기능어 '{w}'에는 강세 표시를 하지 않아요")
        if wl not in FUNC and n != 1: r.e(where, f"'{w}'에 강세 표시 **…**가 정확히 1개 있어야 해요(지금 {n}개)")
    J = jamo(strip_md(pron)); cho = [a for a, b, c in J]; w = es.lower()
    if "ㅋ" in cho or "ㅌ" in cho: r.e(where, f"ㅋ·ㅌ 금지 — c(k)/qu/k는 ㄲ, t는 ㄸ: «{pron}»")
    if "ㅍ" in cho and "f" not in w: r.e(where, f"ㅍ은 f에만 써요(p는 ㅃ): «{pron}»")
    if "f" in w and "ㅍ" not in cho: r.e(where, f"f는 ㅍ으로 적어요: «{pron}»")
    if "p" in w and "ㅃ" not in cho: r.e(where, f"p는 ㅃ으로 적어요: «{pron}»")
    if "t" in w and "ㄸ" not in cho: r.e(where, f"t는 ㄸ으로 적어요: «{pron}»")
    if re.search(r"(qu|k|c(?![eiéíh]))", w) and "ㄲ" not in cho and not re.search(r"c(?=[ct])|x", w):
        r.e(where, f"c(a·o·u)/qu/k는 ㄲ으로 적어요: «{pron}»")
    if re.search(r"z|c[eiéí]", w) and not ({"ㅅ", "ㅆ"} & set(cho)): r.e(where, f"z·c(e·i)는 ㅅ으로 적어요: «{pron}»")
    if re.search(r"ll|y[aeiouáéíóú]", w) and not any(a == "ㅇ" and (b in GLIDE or b == "ㅣ") for a, b, c in J):
        r.e(where, f"ll·y는 야·예·요·유(이 소리)로 적어요: «{pron}»")
    if re.search(r"j|g[eiéí]", w) and "ㅎ" not in cho: r.e(where, f"j·g(e·i)는 ㅎ으로 적어요: «{pron}»")
    if "ch" in w and "ㅊ" not in cho: r.e(where, f"ch는 ㅊ으로 적어요: «{pron}»")
    if "ñ" in w and not any(a == "ㄴ" and b in GLIDE for a, b, c in J): r.e(where, f"ñ는 냐·녜·뇨·뉴로 적어요: «{pron}»")
    if re.search(r"\bh", w) and "ㅎ" in cho and not re.search(r"j|g[eiéí]", w): r.w(where, f"h는 소리 나지 않아요(ㅎ으로 적지 않아요): «{pron}»")

def check_file(path: str) -> tuple[Report, dict]:
    r = Report(os.path.relpath(path, ROOT))
    try:
        y = yaml.safe_load(open(path, encoding="utf-8"))
    except Exception as ex:
        r.e("YAML", f"읽기 실패: {ex}"); return r, {}
    if not isinstance(y, dict): r.e("YAML", "최상위가 dict가 아니에요"); return r, {}
    if y.get("schema_version") != 1: r.e("schema_version", "1이어야 해요")
    allkeys = ["schema_version", "chapter", "opener", "words", "word_order", "practice", "variants", "scenes", "extras", "props"]
    for k in y:
        if k not in allkeys: r.e(k, "스키마에 없는 최상위 키예요")
    ch = need(r, y, "chapter", "root", dict) or {}
    num = ch.get("num")
    plan = PLAN.get(num)
    if not plan: r.e("chapter.num", f"계획에 없는 장 번호: {num}"); plan = {}
    m = re.search(r"ch(\d\d)_text\.yaml$", path)
    if m and num is not None and int(m.group(1)) != num: r.e("chapter.num", "파일 이름의 장 번호와 달라요")
    for k in ("es", "en", "ko", "city", "skin", "date"):
        v = need(r, ch, k, "chapter")
        if v and k in LIM["chapter"]: length(r, v, LIM["chapter"][k], f"chapter.{k}")
        if v and plan and k in plan and k != "en" and v != plan[k]: r.e(f"chapter.{k}", f"계획값과 달라요: «{v}» ≠ «{plan[k]}»")
    date = plan.get("date", ch.get("date", ""))
    # opener
    op = need(r, y, "opener", "root", dict) or {}
    for k in ("parada", "place", "hand"):
        v = need(r, op, k, "opener")
        if v: length(r, v, LIM["opener"][k], f"opener.{k}"); spanish_checks(r, v, f"opener.{k}")
    if op.get("parada") and num and plan and op["parada"] != f"Parada {num:02d} · {plan['city']}":
        r.e("opener.parada", f"형식은 'Parada {num:02d} · {plan.get('city')}'이에요")
    if op.get("photo_note_ko"): length(r, op["photo_note_ko"], LIM["opener"]["photo_note_ko"], "opener.photo_note_ko")
    # words
    words = need(r, y, "words", "root", list) or []
    L = LIM["word"]
    if len(words) != LIM["counts"]["words"]: r.e("words", f"단어는 {LIM['counts']['words']}개여야 해요(지금 {len(words)}개)")
    cores = [w for w in words if isinstance(w, dict) and w.get("core") is True]
    if len(cores) != LIM["counts"]["core"]: r.e("words", f"core: true는 {LIM['counts']['core']}개여야 해요(지금 {len(cores)}개)")
    if words and any(w.get("core") for w in words[8:] if isinstance(w, dict)): r.e("words", "핵심(core) 8개를 목록 맨 앞에 둬요")
    seen_k, seen_es = set(), set()
    for i, w in enumerate(words):
        wh = f"words[{i}]"
        if not isinstance(w, dict): r.e(wh, "dict여야 해요"); continue
        for k in ("key", "es", "base", "gender", "pron", "en", "ko"): need(r, w, k, wh)
        if "core" not in w or not isinstance(w.get("core"), bool): r.e(wh, "core: true/false 가 필요해요")
        es = w.get("es", ""); wh = f"words[{i}] {es}"
        if w.get("key") in seen_k: r.e(wh, "key 중복")
        if es in seen_es: r.e(wh, "단어 중복")
        seen_k.add(w.get("key")); seen_es.add(es)
        if w.get("key") and not re.fullmatch(r"[a-z0-9_]+", w["key"]): r.e(wh, "key는 영문 소문자·숫자·_ 만 써요(사진 파일 이름에 쓰여요)")
        for k in ("es", "base", "pron", "en", "ko", "note"):
            if isinstance(w.get(k), str): length(r, w[k], L[k], f"{wh}.{k}")
        spanish_checks(r, es, f"{wh}.es"); spanish_checks(r, w.get("note", ""), f"{wh}.note", main=False)
        art = es.split()[0].lower() if es else ""
        g = w.get("gender")
        exp = {"el": "m", "la": "f", "los": "mpl", "las": "fpl"}.get(art, "-")
        if art == "el" and len(es.split()) > 1 and es.split()[1].lower() in FEM_EL: exp = "f"
        if g not in ("m", "f", "mpl", "fpl", "-"): r.e(f"{wh}.gender", "m / f / mpl / fpl / - 중 하나")
        elif g != exp: r.e(f"{wh}.gender", f"관사와 성이 안 맞아요(기대값 {exp}). el agua처럼 여성 명사 앞 el이면 f예요")
        if es and art in ("el", "la", "los", "las") and w.get("base") and es.split(" ", 1)[1] != w["base"]: r.e(f"{wh}.base", "관사를 뺀 형태와 같아야 해요")
        pron_check(r, es, w.get("pron"), f"{wh}.pron")
        if isinstance(w.get("ko"), str) and not HANGUL.search(w["ko"]): r.e(f"{wh}.ko", "한국어 뜻이 없어요")
        ex = w.get("example")
        if w.get("core") and not ex: r.e(wh, "핵심 단어는 example(es/en/ko)이 필요해요")
        if ex:
            for k in ("es", "en", "ko"):
                v = need(r, ex, k, f"{wh}.example")
                if v: length(r, v, L[f"example_{k}"], f"{wh}.example.{k}")
            sentence_checks(r, ex.get("es"), f"{wh}.example.es"); korean_checks(r, ex.get("ko"), f"{wh}.example.ko", True)
            b = (w.get("base") or "").split()[0].lower()[:4]
            if b and b not in (ex.get("es") or "").lower(): r.w(f"{wh}.example.es", "예문에 표제어가 안 보여요")
    if plan.get("words"):
        got = [w.get("es") for w in words if isinstance(w, dict)]
        changes = {c.get("from"): c.get("to") for c in (ch.get("word_changes") or []) if isinstance(c, dict)}
        for c in (ch.get("word_changes") or []):
            if not (isinstance(c, dict) and c.get("from") and c.get("to") and c.get("reason")): r.e("chapter.word_changes", "from / to / reason 세 가지를 모두 적어요")
        want = [changes.get(x, x) for x in plan["words"]]
        if set(got) != set(want):
            miss = [x for x in want if x not in got]; extra = [x for x in got if x not in want]
            r.e("words", f"계획 단어 목록과 달라요. 빠짐: {miss} / 추가: {extra}. 바꾸려면 chapter.word_changes에 이유를 적어요")
    # word order
    wo = need(r, y, "word_order", "root", dict) or {}
    W = LIM["word_order"]
    for k in ("tema", "tema_sub_ko", "point_ko", "lead_ko"):
        v = need(r, wo, k, "word_order")
        if v: length(r, v, W[k], f"word_order.{k}")
    korean_checks(r, wo.get("lead_ko"), "word_order.lead_ko", True)
    sents = need(r, wo, "sentences", "word_order", list) or []
    lo, hi = LIM["counts"]["sentences"]
    if not lo <= len(sents) <= hi: r.e("word_order.sentences", f"{lo}~{hi}개여야 해요(지금 {len(sents)}개)")
    for i, s in enumerate(sents):
        wh = f"word_order.sentences[{i}]"
        for k in ("es", "en", "ko", "note_ko"):
            v = need(r, s, k, wh)
            if v: length(r, v, W[{"es": "sentence_es", "en": "sentence_en", "ko": "sentence_ko", "note_ko": "sentence_note_ko"}[k]], f"{wh}.{k}")
        sentence_checks(r, s.get("es"), f"{wh}.es"); korean_checks(r, s.get("ko"), f"{wh}.ko", True)
        toks = need(r, s, "tokens", wh, list) or []
        tl, th = LIM["counts"]["tokens"]
        if not tl <= len(toks) <= th: r.e(f"{wh}.tokens", f"블록은 {tl}~{th}개")
        for j, t in enumerate(toks):
            if not isinstance(t, dict) or not t.get("es") or not t.get("gloss_ko"): r.e(f"{wh}.tokens[{j}]", "es / gloss_ko 둘 다 필요해요"); continue
            length(r, t["es"], W["token_es"], f"{wh}.tokens[{j}].es"); length(r, t["gloss_ko"], W["token_gloss_ko"], f"{wh}.tokens[{j}].gloss_ko")
            if not HANGUL.search(t["gloss_ko"]): r.e(f"{wh}.tokens[{j}].gloss_ko", "한국어 직역이 없어요")
        if toks and s.get("es"):
            joined = " ".join(t.get("es", "") for t in toks if isinstance(t, dict))
            if joined.rstrip(".!?…") != s["es"].rstrip(".!?…"): r.e(f"{wh}.tokens", f"블록을 이으면 문장과 같아야 해요: «{joined}» ≠ «{s['es']}»")
        hl = s.get("highlight", [])
        if not isinstance(hl, list) or any((not isinstance(x, int)) or x >= len(toks) or x < 0 for x in hl): r.e(f"{wh}.highlight", "블록 번호(0부터) 목록이어야 해요")
    for gi, grp in enumerate(wo.get("patterns", []) or []):
        wh = f"word_order.patterns[{gi}]"
        length(r, grp.get("title_ko", ""), W["pattern_title_ko"], f"{wh}.title_ko")
        for j, it in enumerate(grp.get("items", []) or []):
            for k in ("es", "ko", "en", "lit"):
                if it.get(k): length(r, it[k], W[f"pattern_{k}"], f"{wh}.items[{j}].{k}")
            spanish_checks(r, it.get("es", ""), f"{wh}.items[{j}].es")
    for sec in ("contrast", "subject"):
        grp = wo.get(sec)
        if grp:
            for j, it in enumerate(grp.get("items", []) or []):
                length(r, it.get("es", ""), W["contrast_es"], f"word_order.{sec}.items[{j}].es")
                length(r, it.get("ko", ""), W["contrast_ko"], f"word_order.{sec}.items[{j}].ko")
                if it.get("label_ko"): length(r, it["label_ko"], W["contrast_label_ko"], f"word_order.{sec}.items[{j}].label_ko")
                sentence_checks(r, it.get("es", ""), f"word_order.{sec}.items[{j}].es")
    for j, n_ in enumerate(wo.get("extra_notes_ko", []) or []):
        length(r, n_, W["extra_note_ko"], f"word_order.extra_notes_ko[{j}]"); korean_checks(r, n_, f"word_order.extra_notes_ko[{j}]")
    # practice
    pr = need(r, y, "practice", "root", list) or []
    if len(pr) != LIM["counts"]["practice"]: r.e("practice", f"{LIM['counts']['practice']}문제여야 해요(지금 {len(pr)})")
    for i, p in enumerate(pr):
        wh = f"practice[{i}]"
        tiles, ans = p.get("tiles"), p.get("answer", "")
        if not isinstance(tiles, list) or not ans: r.e(wh, "tiles(목록) / answer / ko 필요"); continue
        length(r, ans, LIM["practice"]["answer"], f"{wh}.answer"); length(r, p.get("ko", ""), LIM["practice"]["ko"], f"{wh}.ko")
        words_ = ans.rstrip(".!?…").replace("¿", "").replace("¡", "").split()
        tl = [t.replace("¿", "").replace("¡", "").rstrip("?!") for t in tiles]
        if sorted(tl) != sorted(words_): r.e(f"{wh}.tiles", f"정답 단어를 섞은 것이어야 해요: {tiles} ↔ «{ans}»")
        elif tl == words_: r.e(f"{wh}.tiles", "정답 순서 그대로예요. 섞어 주세요")
        spanish_checks(r, ans, f"{wh}.answer")
    # variants / scenes
    va = need(r, y, "variants", "root", list) or []
    lo, hi = LIM["counts"]["variants"]
    if not lo <= len(va) <= hi: r.e("variants", f"{lo}~{hi}개")
    for i, v in enumerate(va):
        length(r, v.get("es", ""), LIM["variant"]["es"], f"variants[{i}].es"); length(r, v.get("alt", ""), LIM["variant"]["alt"], f"variants[{i}].alt")
        if v.get("es") and v["es"] not in seen_es: r.w(f"variants[{i}]", f"«{v['es']}»가 이 장 단어 목록에 없어요")
    sc = need(r, y, "scenes", "root", list) or []
    lo, hi = LIM["counts"]["scenes"]
    if not lo <= len(sc) <= hi: r.e("scenes", f"{lo}~{hi}개")
    for i, s in enumerate(sc):
        for k in ("es", "en", "ko"):
            v = need(r, s, k, f"scenes[{i}]")
            if v: length(r, v, LIM["scene"][k], f"scenes[{i}].{k}")
        sentence_checks(r, s.get("es"), f"scenes[{i}].es"); korean_checks(r, s.get("ko"), f"scenes[{i}].ko", True)
    # extras
    ex = need(r, y, "extras", "root", dict) or {}
    g = ex.get("grammar_ko") or []
    lo, hi = LIM["counts"]["grammar_ko"]
    if not lo <= len(g) <= hi: r.e("extras.grammar_ko", f"{lo}~{hi}개")
    for i, s in enumerate(g): length(r, s, LIM["extras"]["grammar_ko"], f"extras.grammar_ko[{i}]"); korean_checks(r, s, f"extras.grammar_ko[{i}]", True)
    for i, c in enumerate(ex.get("cognates") or []): length(r, c.get("note_ko", ""), LIM["extras"]["cognate_note_ko"], f"extras.cognates[{i}].note_ko")
    ff = ex.get("false_friend")
    if ff: length(r, ff.get("note_ko", ""), LIM["extras"]["false_friend_note_ko"], "extras.false_friend.note_ko")
    if ex.get("fun_fact_ko"): length(r, ex["fun_fact_ko"], LIM["extras"]["fun_fact_ko"], "extras.fun_fact_ko")
    # props
    props = need(r, y, "props", "root", list) or []
    lo, hi = LIM["counts"]["props"]
    if not lo <= len(props) <= hi: r.e("props", f"소품 문구는 {lo}~{hi}개")
    for i, p in enumerate(props):
        kind = p.get("kind"); lines = p.get("lines") or []
        if kind not in LIM["props"]: r.e(f"props[{i}].kind", f"종류는 {list(LIM['props'])} 중 하나"); continue
        mx, ml = LIM["props"][kind]
        if len(lines) > ml: r.e(f"props[{i}]", f"{kind}는 최대 {ml}줄")
        for j, ln in enumerate(lines):
            length(r, ln, mx, f"props[{i}].lines[{j}]")
            for dm in re.finditer(r"\b(\d{1,2}) (MAY|JUN|ABR|APR)\b", ln):
                d2 = f"{dm.group(1)} {dm.group(2)}"
                if d2 != date and kind != "ticket": r.e(f"props[{i}]", f"날짜 «{d2}»가 여행일정({date})과 달라요")
                if kind == "ticket" and int(dm.group(1)) < int(date.split()[0]): r.e(f"props[{i}]", f"표 날짜 «{d2}»가 방문일({date})보다 앞서요")
            if re.search(r"\b(lunes|martes|miércoles|jueves|viernes|sábado|domingo|MON|TUE|WED|THU|FRI|SAT|SUN|LUN|MAR|MIÉ|JUE|VIE|SÁB|DOM)\b", ln):
                r.e(f"props[{i}]", "요일은 쓰지 않아요(연도 미정)")
            if re.search(r"\b20\d\d\b", ln): r.e(f"props[{i}]", "연도는 쓰지 않아요")
    # whole-file brand scan
    brand_check(r, yaml.safe_dump(y, allow_unicode=True), "전체")
    return r, y

def korean_prose(y: dict) -> str:
    out = []
    def add(s):
        if isinstance(s, str) and HANGUL.search(s): out.append(strip_md(s))
    wo = y.get("word_order", {}) or {}
    add(wo.get("lead_ko"))
    for s in wo.get("sentences", []) or []: add(s.get("ko")); add(s.get("note_ko"))
    for n in wo.get("extra_notes_ko", []) or []: add(n)
    for w in y.get("words", []) or []:
        if w.get("example"): add(w["example"].get("ko"))
    for s in y.get("scenes", []) or []: add(s.get("ko"))
    ex = y.get("extras", {}) or {}
    for g in ex.get("grammar_ko", []) or []: add(g)
    for c in ex.get("cognates", []) or []: add(c.get("note_ko"))
    if ex.get("false_friend"): add(ex["false_friend"].get("note_ko"))
    add(ex.get("fun_fact_ko"))
    return "\n".join(out) + "\n"

def run_humanizer(path, y, r):
    prose = korean_prose(y)
    outp = re.sub(r"_text\.yaml$", "_ko_prose.md", path)
    open(outp, "w", encoding="utf-8").write(prose)
    if not os.path.exists(HUMANIZER):
        r.w("humanizer", f"감사 스크립트가 없어요: {HUMANIZER}"); return
    p = subprocess.run([sys.executable, HUMANIZER, "--quality", "--genre", "docs", outp], capture_output=True, text=True)
    txt = (p.stdout + p.stderr).strip()
    print(f"--- humanizer-kr 감사 ({os.path.relpath(outp, ROOT)}) ---\n{txt or '(지적 없음)'}")
    if re.search(r"\b(finding|Finding|발견|\[)", txt) and "No findings" not in txt and "0 findings" not in txt:
        r.w("humanizer", "humanizer-kr 감사에서 지적이 나왔어요. 위 목록을 보고 고칠지 판단해요(스크립트는 참고용)")

def cross_check(ys):
    r = Report("장 사이 일관성"); seen = {}
    for path, y in ys:
        for w in y.get("words", []) or []:
            k = w.get("es")
            if not k: continue
            if k in seen:
                p0, w0 = seen[k]
                for f in ("pron", "ko", "gender"):
                    if w0.get(f) != w.get(f): r.w(k, f"{f}가 장마다 달라요: {os.path.basename(p0)} «{w0.get(f)}» / {os.path.basename(path)} «{w.get(f)}»")
            else: seen[k] = (path, w)
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--humanizer", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    files = a.files or []
    if a.all: files += sorted(glob.glob(os.path.join(ROOT, "es/ch*/text/ch*_text.yaml")))
    if not files: ap.print_help(); return 2
    bad = 0; ys = []
    for f in files:
        f = os.path.abspath(f)
        r, y = check_file(f); ys.append((f, y))
        if a.humanizer and y: run_humanizer(f, y, r)
        print(f"\n== {r.name}: 오류 {len(r.err)} · 경고 {len(r.warn)}")
        for m in r.err + r.warn: print("  " + m)
        bad += len(r.err) + (len(r.warn) if a.strict else 0)
    if len(ys) > 1:
        r = cross_check(ys); print(f"\n== {r.name}: 경고 {len(r.warn)}")
        for m in r.warn: print("  " + m)
        bad += len(r.warn) if a.strict else 0
    print("\n결과:", "통과" if not bad else "실패")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())

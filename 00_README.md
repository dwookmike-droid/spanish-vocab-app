# 세상에없던 단어장 — 작업 폴더

사진으로 배우는 여행 단어장 『Vocabulario visual』의 작업 폴더예요. 스페인어 편(es)을 먼저 만들고, 프랑스어 편(fr)은 자리만 만들어 뒀어요.

## 역할 분담
| 누가 | 맡는 일 | 쓰는 곳 |
|---|---|---|
| Claude Code | 텍스트 전부: 단어 뜻·발음, 예문, 어순 설명, 연습문제, 장면 문장, 소품 문구 | `es/chNN/text/` |
| Grok Bot | 사진, 디자인, 레이아웃, PDF·웹 빌드, 용량 최적화 | `design/`, `es/chNN/design/` |
| Mike | 방향 결정, 최종 검수 | — |

## 작업 흐름
1. **텍스트** — Claude Code가 장별 작업지시서대로 `chNN_text.yaml`을 쓰고, humanizer-kr로 한국어를 다듬고, 검증기를 통과시켜요.
2. **디자인·빌드** — Grok Bot이 YAML을 읽어 지면에 앉히고 인쇄용·화면용 PDF와 웹판을 만들어요. 넘치는 문구는 필드를 짚어 되돌려요.
3. **검수** — Mike가 PDF로 확인하고, 고칠 점을 텍스트/디자인 중 맞는 쪽에 넘겨요.

## 폴더 구조
```
세상에없던 단어장/
├─ 00_README.md            이 문서
├─ CLAUDE.md               Claude Code가 자동으로 읽는 규칙(텍스트만, design 수정 금지, humanizer-kr 필수)
├─ 작업지시서_텍스트.md     텍스트 총괄 작업지시서
├─ .claude/skills/         프로젝트 스킬: humanizer-kr(사본), vocab-text-writer, spanish-pronunciation-ko
├─ schema/                 SCHEMA.md(필드 설명) · limits.yaml(글자 수) · plan_es.yaml(24장 계획·여행일정)
├─ tools/validate_text.py  텍스트 검증기
├─ es/
│  ├─ _book/               TOC_v6.md(총 목차) · 여행일정.md
│  └─ ch01 … ch24/
│     ├─ 작업지시서_chNN.md
│     ├─ text/             Claude Code 결과물 (ch01은 골드 샘플, ch02·ch11은 v6 seed 포함)
│     └─ design/           Grok Bot 자리
├─ fr/                     프랑스어 편 자리(ch01 … ch24, 비어 있음)
└─ design/                 Grok Bot: 결과물(v6 PDF·웹), 문서, 빌드 스크립트, 사진·폰트, 미리보기
```

## 시작하기 (Claude Code)
```bash
cd ~/"Library/Mobile Documents/com~apple~CloudDocs/2025년/2025 과외/세상에없던 단어장"
claude
```
그다음: `작업지시서_텍스트.md 따라 ch03 써줘`

검증만 따로: `python3 tools/validate_text.py es/ch03/text/ch03_text.yaml --humanizer`

## 현재 상태 (2026-11-02 KST)
- v6 결과물: 목차 + ch01 · ch02 · ch11 + 출처 페이지 (`design/deliverables/v6/`)
- 텍스트: ch01 완료(골드 샘플), ch02 · ch11 단어 카드만 있음, 나머지 21장 신규

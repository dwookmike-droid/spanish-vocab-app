---
name: vocab-text-writer
description: 『Vocabulario visual』(세상에없던 단어장) 한 장의 텍스트를 chNN_text.yaml 스키마대로 쓰는 절차. "chNN 써줘", "단어장 텍스트", "작업지시서대로 써줘", 장별 예문·어순·연습문제·소품 문구 작성 요청에 사용. 발음은 spanish-pronunciation-ko, 한국어 다듬기는 humanizer-kr과 함께 써요.
---

# vocab-text-writer — 장 하나 쓰기

텍스트만 써요. `design/`과 `chNN/design/`은 읽지도 고치지도 않아요(사진·레이아웃은 Grok Bot 담당).

## 0. 읽을 것 (순서대로)
1. `작업지시서_텍스트.md` — 총괄 규칙
2. `es/chNN/작업지시서_chNN.md` — 이 장의 도시·날짜·어순 포인트·단어 20·주의 단어·소품
3. `es/ch01/text/ch01_text.yaml` — 골드 샘플. 구조·말투·길이의 기준
4. `schema/SCHEMA.md`, `schema/limits.yaml` — 필드와 글자 수
5. seed가 있으면(`chNN_seed_v6.yaml`) 그 내용을 출발점으로 써요

## 1. 쓰는 순서
1. **chapter / opener**: 계획값을 그대로 옮겨요. `place`는 실제 장소명(스페인어), `hand`는 여행자가 손으로 적은 듯한 짧은 스페인어 한 줄이에요.
2. **words 20**: 핵심 8개를 앞에. 단어마다
   - `es` 관사 포함, `base` 관사 뺀 형태, `gender` 관사 기준(el agua류는 f)
   - `pron` → spanish-pronunciation-ko 스킬로 작성(강세 `**…**`)
   - `en` 짧게(≤16), `ko` 가장 흔한 한국어 명사(≤8)
   - `note` 필요할 때만(≤24): `Latam: …`, `= …`(동의어), `también: …`, `¡siempre plural!`
   - 핵심 8개는 `example` 필수: 그 장소에서 실제로 할 법한 말, 스페인어 ≤40, 한국어 ≤22
3. **word_order**: 대표 예문을 첫 문장으로. 블록(tokens)마다 한국어 직역(`gloss_ko` ≤9). 블록을 이으면 원문과 같아야 해요. `highlight`로 포인트 블록 지정. 필요하면 patterns / contrast / subject 묶음 추가.
4. **practice 5**: 정답 문장을 단어 단위로 섞은 `tiles`. 정답 순서 그대로면 안 돼요. 3문제 이상은 이 장의 어순 포인트.
5. **variants 3~8**: 중남미 등 지역 변이. 확실한 것만.
6. **scenes 4~6**: 그 장소에서 바로 쓰는 문장.
7. **extras**: 문법 상자 3~4(각 ≤96), cognates, false friend, fun fact — 출처가 확실한 것만. 모르면 비워요(선택 필드).
8. **props 3~7**: 스킨에 맞는 종류. 날짜는 여행일정 값, 연도·요일·브랜드 금지. 표 번호는 가짜.

## 2. 한국어 다듬기 (humanizer-kr)
- 한국어 문장 필드를 모아 humanizer-kr 스킬의 Core Workflow대로 다듬어요. 장르: 학습서 설명문 / 독자: 처음 배우는 성인 / 말투: 해요체.
- 의미·사실·스페인어 인용은 그대로 두고 말만 고쳐요. 글자 수 제한 안에서 고쳐요.
- 검증기 `--humanizer`가 만든 `chNN_ko_prose.md`(한국어 문장 모음)와 감사 결과를 보고 다시 읽어요. 지적이 없어도 소리 내어 읽는 느낌으로 한 번 더 확인해요.
- 직역 괄호·인용 표기·성별 표시에 붙는 `punctuation-clutter` 지적은 단어장 표기 규칙이라 그대로 둬요. 번역투·명사화·어색한 연결은 고쳐요. 표현 점검은 `references/humanize-korean-quick-rules.md`도 함께 봐요.
- 더 정밀한 점검이 필요하면 `references/humanize-korean-quick-rules.md`(humanize-korean 스킬의 빠른 규칙표)도 참고해요.

## 3. 검증
```bash
python3 tools/validate_text.py es/chNN/text/chNN_text.yaml --humanizer
python3 tools/validate_text.py --all     # 장 2개 이상일 때 장 사이 일관성
```
오류 0이 될 때까지 고쳐요. 경고는 하나씩 읽고 고칠지 판단해요.

## 4. 보고 (짧게)
- 파일 경로, 검증 결과(오류·경고 수)
- 계획과 달라진 점(word_changes, 핵심 단어 변경)
- 확인하지 못한 발음·사실 목록

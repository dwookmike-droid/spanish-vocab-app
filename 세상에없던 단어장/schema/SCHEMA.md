# chNN_text.yaml 스키마 (schema_version: 1)

골드 샘플: `es/ch01/text/ch01_text.yaml`. 글자 수: `limits.yaml`. 계획값(단어·도시·날짜): `plan_es.yaml`.
검증: `python3 tools/validate_text.py <파일>`

```yaml
schema_version: 1
chapter:
  num: 3                      # 정수, 파일 이름 ch03과 같아야 함
  es: El salón                # 계획값 그대로
  en: The living room
  ko: 거실
  city: Sevilla               # 계획값 그대로
  skin: Azulejo · patio       # 계획값 그대로
  date: 23 MAY                # 계획값 그대로 (여행일정)
  word_changes: []            # 계획 단어를 바꿀 때만: [{from: el mando, to: el mando a distancia, reason: "..."}]
opener:
  parada: Parada 03 · Sevilla # 형식 고정
  place: Casa de Pilatos, el patio   # 사진 장소 (스페인어, ≤46)
  hand: ...                   # 손글씨 한 줄 (스페인어, ≤50)
  photo_note_ko: ...          # 사진 설명 한 줄 (한국어, ≤40, 선택)
words:                        # 20개, 핵심(core: true) 8개를 맨 앞에
  - key: sofa                 # 영문 소문자 id (사진 파일 이름과 연결)
    es: el sofá               # 관사 포함
    base: sofá                # 관사 뺀 형태
    gender: m                 # m | f | mpl | fpl | -(관사 없는 표현)
    pron: 엘 소**파**         # 한글 발음, 강세 **…**
    en: sofa                  # 영어 뜻 (≤16)
    ko: 소파                  # 한국어 뜻 (≤8)
    core: true
    note: ''                  # 카드 메모 (≤24, 스페인어/짧은 표기: "Latam: …", "= …", "también: …")
    example:                  # 핵심 8개는 필수, 보조는 선택
      es: ...
      en: ...
      ko: ...
word_order:
  tema: ...                   # 문법 쪽 큰 제목 (스페인어)
  tema_sub_ko: ...            # 한국어 부제
  point_ko: ...               # 어순 포인트 한 줄 (계획 문구 기반)
  lead_ko: ...                # 도입 설명 (≤72)
  sentences:                  # 3~5개 — 블록 예문
    - es: El sofá está al lado de la ventana.
      en: ...
      ko: 소파는 창문 옆에 있어요.
      note_ko: ...            # 어순 설명 한 줄 (≤36)
      tokens:                 # 2~6블록, 이으면 es와 같아야 함
        - {es: El sofá, gloss_ko: 그 소파}
        - {es: está, gloss_ko: 있다}
        - {es: al lado de, gloss_ko: ~의 옆에}
        - {es: la ventana, gloss_ko: 그 창문}
      highlight: [2]          # 강조할 블록 번호(0부터)
  patterns:                   # 선택, 묶음 0~3개 (ch01 참고)
    - title_ko: ...
      items: [{es: ..., ko: ..., en: ..., lit: ..., tag: ...}]   # en/lit/tag 선택
  contrast:                   # 선택 — 같은 뜻 다른 어순 비교
    title_ko: ...
    items: [{es: ..., label_ko: ..., ko: ...}]
  subject:                    # 선택 — 주어 생략 등
    title_ko: ...
    items: [{es: ..., ko: ...}]
  extra_notes_ko: [...]       # 보충 설명 0~2개 (≤150)
practice:                     # 5문제
  - tiles: [ventana, al, El, sofá, lado, está, de, la]   # 정답 단어를 섞은 것
    answer: El sofá está al lado de la ventana.
    ko: 소파는 창문 옆에 있어요.
variants: [{es: el mando, alt: "el control remoto (중남미)"}]   # 3~8개, es는 이 장 단어
scenes: [{es: ..., en: ..., ko: ...}]                          # 4~6개
extras:
  grammar_ko: [...]           # 문법 상자 3~4개 (각 ≤96)
  cognates: [{es: ..., en: ..., note_ko: ...}]                 # 0~4
  false_friend: {es: ..., en: ..., note_ko: ...}               # 선택
  fun_fact_ko: ...            # 선택 (≤62), 확실한 사실만
props:                        # 3~7개
  - kind: postmark            # postmark | stamp | ticket | label | polaroid | chalk | wall | poster | price | hand
    lines: ['CORREO · SEVILLA · 23 MAY']
```

소품 종류별 한 줄 최대 글자 수/최대 줄 수는 `limits.yaml`의 `props`에 있어요. 소품 날짜(예: `23 MAY`)는 여행일정과 같아야 하고, 표(ticket)만 방문일 이후 날짜를 쓸 수 있어요(다음 행선지 표).

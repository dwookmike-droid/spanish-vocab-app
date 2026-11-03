# chNN_extra.yaml — 웹앱 전용 콘텐츠 (상황별 대화 · 짧은 글 읽기)

인쇄본 텍스트(`es/chNN/text/chNN_text.yaml`)는 그대로 두고, 웹앱에만 쓰는 대화·읽기 글을 이 파일에 따로 써요.
검사: `python3 webapp/tools/check_extra.py webapp/content/chNN_extra.yaml`

## 규칙
- 스페인어는 스페인 표준(카스티야). 장의 도시·날짜(`schema/plan_es.yaml`, `es/_book/여행일정.md`)와 장 단어(chNN_text.yaml의 words)를 자연스럽게 많이 써요.
- 한국어는 해요체(대화 안에서 친구끼리면 반말 가능). 번역투 없이 자연스럽게(humanizer-kr 규칙).
- 사실을 지어내지 않아요. 상표·가게 이름 금지. 연도·요일 금지.
- 발음(pron)은 `.claude/skills/spanish-pronunciation-ko` 규칙, 강세는 `**…**`.

## 형식
```yaml
schema_version: 1
chapter: 1
dialogues:                      # 2개
  - id: d1
    title_es: En el hotel, falta una toalla
    title_ko: 호텔에서 수건이 모자랄 때
    setting_ko: 그라나다의 작은 호텔. 샤워하려는데 수건이 하나뿐이에요.   # ≤60
    roles:
      A: {es: Recepcionista, ko: 프런트 직원}
      B: {es: Huésped, ko: 손님}
    lines:                      # 6~10줄, A/B 번갈아
      - who: B
        textbook:               # 교재식: 문법대로 또박또박, 초급자가 배우는 표현
          es: Perdone. ¿Tiene otra toalla, por favor?
          ko: 실례합니다. 수건 하나 더 있나요?
        native:                 # 실제 원어민이 같은 상황에서 흔히 하는 말 (구어, 줄임, 맞장구 포함)
          es: Oye, perdona, ¿me podéis subir otra toalla?
          ko: 저기요, 죄송한데 수건 하나 더 갖다주실 수 있어요?
          note_ko: 스페인에선 직원에게도 tú(perdona)를 많이 써요. podéis는 '그쪽(호텔 사람들)'   # ≤70, 왜 다른지
readings:                       # 2개, 각 60~120단어
  - id: r1
    title_es: Una mañana en Granada
    title_ko: 그라나다의 아침
    level: A1                   # A1 | A2
    paragraphs:                 # 2~4문단
      - es: Son las ocho. Me ducho y me lavo los dientes. ...
        ko: 여덟 시예요. 샤워하고 이를 닦아요. ...
    questions:                  # 이해 확인 2~3개 (객관식)
      - q_ko: 글쓴이는 아침에 무엇을 먼저 했나요?
        choices_ko: [샤워, 아침 식사, 산책]
        answer: 0
glossary:                       # 대화(textbook·native)와 읽기에 나오는 모든 단어 형태
  # 키: 글에 나온 그대로의 형태를 소문자로 (구두점 제외, ¿¡ 제외). 동사 활용형·복수형도 각각 키로.
  # 장 단어(chNN_text.yaml words의 base 단어들)는 여기 없어도 되지만, 활용·복수형은 넣어요.
  me: {lemma: me, ko: 나 자신(을/에게), en: myself, pron: 메}
  ducho: {lemma: ducharse, ko: 샤워하다(나는), en: I shower, pron: **두**초}
  toallas: {lemma: toalla, ko: 수건들, en: towels, pron: 또**아**야스}
```

- glossary의 `pron`은 그 형태 그대로의 발음이에요(관사 없이).
- 숫자(8, 20 등)는 glossary가 필요 없어요.
- 하이픈·아포스트로피가 없는 스페인어 특성상 단어는 공백과 구두점(.,;:!?¡¿«»"()—…)으로 나눠요.

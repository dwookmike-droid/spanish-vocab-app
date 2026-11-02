# AUDIT · ch06 Frutas y verduras (v6, 2026-11-02)

## 텍스트 검수 (Claude Code 산출물)
- 결과: **통과**. validate_text.py 오류 0 · 경고 0 (원본·검수본 둘 다).
- 확인한 것: 스페인 표준 표현(el plátano, la patata, la fresa, la seta, el pimiento — 중남미 형태는 노트·§6 변이에 따로 있음), 관사·성(la uva, el melón, la sandía, el ajo …), EN/KO 뜻, 단어별 직역, 어순 포인트 «수량 + de + 명사»(un kilo de tomates, media docena de huevos, dos kilos de patatas, una bolsa de cebollas, cien gramos de setas — 셀 수 있는 물건은 de 뒤 복수, 숫자만 쓸 때는 de 없음, medio/media는 뒤 명사 성에 맞춤), 연습 5문항 모두 이 포인트. 발음 표기 규칙(p/t/k→ㅃㄸㄲ, c/z→ㅅ, j→ㅎ, ll→야, 강세 굵게), 해요체, 길이 제한, 브랜드 없음. 소품 날짜 7 MAY = Barcelona ch06 일정. 닮은 말 4개, 가짜 친구(fresa ≠ fresh), 12알 포도(uvas de la suerte) 사실 맞아요.
- 사소한 수정 1건 (**box 사본 ch06_text_reviewed.yaml에만 반영**, Mac 원본은 그대로라 Claude Code 쪽에도 반영 필요):
  1. word_order.patterns[0] 직역 `kilo · of · tomatoes` → `a · kilo · of · tomatoes`, `bag · of · oranges` → `a · bag · of · oranges` (스페인어 un/una 칸이 직역에서 빠져 있었어요)
- 참고(수정 안 함): lechuga = '상추'는 스페인 시장의 양상추·로메인까지 넓게 부르는 말이라 그대로 둬요.
- 빌드 스크립트가 reviewed yaml과 원본이 words · practice · sentences · scenes · extras · props에서 같은지 assert해요.

## 페이지 (A4, 6쪽, 책 쪽번호 30–35) · 스킨 Mercado × 바르셀로나 라 보케리아
p30 오프너(보케리아 과일 진열, Bodoni 이탤릭 제목, 흰 가격표 배지 MERCADO · 7 MAY / frutas y verduras) · p31 단어 20(칠판 «Hoy en el puesto», 폴라로이드 «la Boqueria», 크라프트 가격표 manzanas 2,20 €/kg, 손글씨 una bolsa de naranjas, 핵심 카드마다 빨강·초록 차양 줄무늬 테이프, 나머지는 크라프트 꼬리표+끈) · p32 Un kilo de tomates(채소 가판대 장면 라벨 4 + 단어 블록 5 + NOTA + 트렌카디스 띠) · p33 Un kilo, media docena(Nº1 수량+de+명사 직역 포함, Nº2 물건마다 세는 말, ¿Con de o sin de? 칠판 + 피망 누끼, 달걀 사진 + 가격표 media docena 1,90 €, §2 medio/media, 갈색 Gramática 판, 핵심 예문 8) · p34 En el puesto(순서 맞히기·장면 6·지역 변이 7·닮은 말 4·가짜 친구·Curiosidad 12알 포도 + 원형 사진·MERCADO 소인·고추·마늘 타래 띠·정답) · p35 Créditos(사진 26건)
색: 수량(un kilo · media docena · una bolsa …) = 토마토 빨강, de = 호박색, de 뒤 물건 = 초록 (PDF·웹 동일).

## 인쇄 품질
| 항목 | print | screen |
|---|---|---|
| 크기 | 4.01 MB | 1.12 MB |
| 폰트 | 10개 서브셋 전부 임베드, Type 3 = 0 | 동일 |
| 사진 최저 ppi(종이 텍스처 제외) | 원본 기준 330 (오프너, 2732×3864 · 하한 300 통과), PDF에 들어간 사진 317 이상 | 약 150 (목표 150) |
| 최소 글자 (HTML / SVG) | 7.00pt / 7.38pt | 동일 |
| 넘침·겹침 (CHECK + 크레딧 칼럼) | 0 | 0 |

폰트: BodoniModa Regular/Italic, Jost, Gowun Batang Regular/Bold, Caveat, Special Elite, Nanum Pen (전부 CID TrueType 서브셋).
수정 내역: 오프너 배지 글자가 테두리를 넘쳐서 줄임. p31 손글씨가 제목 부제와 겹쳐 칠판 아래로 옮김, 가격표 € 글자가 테두리 밖으로 나가서 넓힘. p32 «Un tomate grande» 점을 토마토 위로 옮김. p33 Nº1 판이 길어 칠판과 겹쳐서 직역을 한국어 뜻 옆 줄로 붙이고 칠판을 12mm 내림. p35 크레딧의 한자 파일 이름(el kilo 저울 사진)이 글꼴에 없어 Type 3로 들어가서, 한자만 빼고 링크는 인코딩 그대로 적음 → Type 3 = 0.

## 사진 처리
- 상표 처리: 오프너 원본 오른쪽의 멜론·수박 브랜드 스티커는 왼쪽만 잘라 써서 빠졌어요. 폴라로이드는 사전(PONS)·주스 간판이 없게 잘랐어요. 저울(el kilo)의 가게 스티커(MCP 로고)는 지우고 배경을 없앴어요(벽 간판·날짜 도장은 크롭으로 제외). el melón은 손글씨 간판이 있는 사진 대신 스티커 없는 피엘 데 사포 사진으로 바꿨어요. 12알 포도 원형 사진은 포장 초콜릿(브랜드 포장지)이 프레임 밖에 오게 잘랐어요.
- 남아 있는 것: 오프너·장면 사진 속 손글씨 가격표(PIÑA 1,50 · SANDÍA 등)는 상표가 아니라 시장 분위기라 그대로 뒀어요.
- 누끼(rembg isnet): 피망·저울·종이봉투(+ 사과는 장식용으로만 만들어 둠).
- 바르셀로나 실사진: 오프너·폴라로이드·p32 채소 가판대·p33 달걀·la naranja/la fresa/el limón/el tomate 카드(모두 보케리아)·p34 고추·마늘 타래. 나머지 카드는 지역 무관 사진.
- 기존 v6 원본 중 맞는 사진이 없어 전부 새로 받았어요(Commons 26건).

## 웹 (web_ch06/, zip 0.9 MB / 폴더 1.2 MB)
단어 20(예문 8 포함, 누끼 3장은 투명 WebP), 장면 사진 3, 단어 블록 5, 수량 패턴 2·대조, 달걀 예문, medio/media, NOTA, Gramática 메모, 순서 맞히기(정답 펼침), 닮은 말·가짜 친구·12알 포도, 장면 6, 지역 변이. 음성 53개(es-ES-ElviraNeural, mono 24kHz 32kbps), WebP 43장. 참조 누락 0.

## 남은 점
- p32 사진 라벨 4개(Un kilo de tomates / Un tomate grande / Dos lechugas / Medio kilo de pimientos)는 디자인 쪽에서 붙인 쉬운 문장이에요(앞 두 개는 원고 문장, 뒤 두 개는 원고 패턴으로 만든 것).
- p31 핵심 카드 02·03의 테이프가 범례 줄 끝(「굵은 글자 = 강세」)을 살짝 가려요. ch02–ch05와 같은 공용 레이아웃이라 그대로 뒀어요.
- 텍스트 수정 1건은 Mac 원본(ch06_text.yaml)에 아직 반영 안 됐어요.

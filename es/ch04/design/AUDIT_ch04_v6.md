# AUDIT · ch04 El dormitorio (v6, 2026-11-02)

## 텍스트 검수 (Claude Code 산출물)
- 결과: **통과**. validate_text.py 오류 0 · 경고 0 (`--humanizer`를 붙이면 humanizer 감사 스크립트가 없다는 경고 1건만 나와요).
- 확인한 것: 스페인 표준(카스티야) 표현, 관사·성, EN/KO 뜻, 단어별 직역, 소유사 어순(mi·mis는 명사 앞 / mío·mía·míos·mías는 명사 뒤·es 뒤, 성·수는 물건에 맞춤, mi는 관사 없이), 연습 5문항 모두 이 포인트를 다뤄요. 발음 규칙(p/t/k→ㅃㄸㄲ, f만 ㅍ, ll/y→야/요, c/z→ㅅ, 강세 굵게), 해요체, 브랜드 없음, 소품 날짜 15 MAY = 여행일정.md(Toledo ch04) 확인. 어원(armarium · balcone · commode · pijama)과 가짜 친구(sábana ≠ sabana), 톨레도 유네스코 사실도 맞아요.
- 사소한 수정 3건 (**box 사본 ch04_text_reviewed.yaml에만 반영**, Mac 원본은 그대로라 Claude Code 쪽에도 반영 필요):
  1. opener.hand `una ventana, un balcón, y a dormir` → `una ventana, un balcón y a dormir` (스페인어는 y 앞에 쉼표를 안 써요)
  2. word_order 문장 1 en `My bed. The bed of mine.` → `My bed. The bed that's mine.`
  3. subject `¿Es tuya?` ko `네 거야?`(반말) → `당신 거예요?`(해요체)
- 참고(수정 안 함): persiana는 스페인에서 바깥 롤러 셔터인 경우가 많아요(원고 뜻 '블라인드'도 틀리진 않음). '자명종'은 조금 옛말 느낌. 연습 2–4는 word_order 문장과 같은 문장.
- 빌드 스크립트가 reviewed yaml과 원본이 words · practice · patterns · 문장 2–5에서 같은지 assert해요.

## 페이지 (A4, 6쪽, 책 쪽번호 18–23) · 스킨 Azulejo · patio × Toledo
p18 오프너(Calle de Santa Isabel 골목과 대성당 탑, Bodoni 이탤릭 제목, 흰 소인 TOLEDO) · p19 단어 20(폴라로이드 «ventanas de Toledo», 레이스 커튼 테이프, 거리 명판 Nº 04 — Toledo, CORREO · TOLEDO · 15 MAY 소인, 다마스키나도 열쇠 꼬리표 LLAVE Nº 15 / la llave mía, 손글씨 메모) · p20 Mi y mío(침실 장면 라벨 5 + 단어 블록 5 + NOTA + 다마스키나도 띠) · p21 Mi cama, la cama mía(명사 앞/뒤 패턴, ¿Mi o mía? 대조 + 여행 가방, ¿De quién es? + 열쇠, Casa de Pizarro 침실, Gramática 메모, 핵심 예문 8) · p22 En el dormitorio(순서 맞히기·장면 6·지역 변이 8·닮은 말 4·가짜 친구·Curiosidad·San Martín 다리·톨레도 야경 띠·정답) · p23 Créditos
색: 명사 앞 mi·tu·su = 코발트, 명사 뒤 mío·mía·tuya = 테라코타, está = 황토 (PDF·웹 동일).

## 인쇄 품질
| 항목 | print | screen |
|---|---|---|
| 크기 | 3.87 MB | 1.12 MB |
| 폰트 | 9개 서브셋 전부 임베드, Type 3 = 0 | 동일 |
| 사진 최저 ppi(종이 텍스처 제외) | 316 (목표 320, 하한 300; 원본은 전부 353ppi 이상) | 약 150 (목표 150) |
| 최소 글자 (HTML / SVG) | 7.00pt / 7.21pt | 동일 |
| 넘침·겹침 (CHECK) | 0 | 0 |

폰트: BodoniModa Regular/Italic, Jost, Gowun Batang Regular/Bold, Caveat, Special Elite (전부 CID TrueType 서브셋).
수정 내역: p19 '전신 거울' 카드 글자가 두 줄로 넘쳐 아래 카드와 겹침 → 그 카드만 글자 7.9pt로. p22 장면 6개가 §7과 겹침 → §4 줄 간격 줄이고 §7 내림. p21 블록 간격 조정, 여행 가방 drop-shadow 필터(래스터화) 제거.
※ p22 띠 캡션의 text-shadow만 회색 흐림 이미지(619×67, 300ppi)로 들어가요. 글자 자체는 벡터.

## 사진 처리
- 오프너: 세로 HOTEL 간판 글자, 맥주 광고판, 작은 호텔 명판, 빨간 표지판, 파란 번지 타일을 리터칭으로 지웠어요(읽히는 글자·로고 없음).
- 누끼(rembg): 옷장·자명종·전신 거울(거울 면 다시 채움)·실내화·충전기·열쇠. 여행 가방은 ch11 누끼 재사용. 옷걸이는 누끼에서 가로대가 사라져 사진 카드로.
- 자명종 문자판의 원래 상표 자리는 흐린 회색으로 남아 있어요(글자 없음). 실내화 안창의 작은 글자는 카드 크기에서 읽히지 않아요.
- 후보에서 뺀 것: 사건 자료 사진, 수용소 줄무늬 옷 '잠옷' 사진, 저해상 담요, 디즈니 침대, 거리 명판 타일 사진(글자).

## 웹 (web_ch04/, zip 0.80 MB / 폴더 1.1 MB)
단어 20(예문 8 포함, 누끼 7장은 투명 WebP), 장면 사진 2, 단어 블록 5, 소유사 패턴 2·대조·¿De quién es?, NOTA, Gramática 메모, 순서 맞히기(정답 펼침), 장면 6, 지역 변이. 음성 53개(es-ES-ElviraNeural, mono 24kHz 32kbps), WebP 42장.

## 남은 점
- p20 사진 라벨 5개(Esta cama es mía. 등)는 디자인 쪽에서 붙인 쉬운 문장이에요. p21 Pizarro 사진 라벨은 원고 문장 1 재사용.
- p20 장면은 영국 Winterbourne House 침실(스페인 아님), p21 작은 장면은 트루히요(카세레스) Casa de Pizarro 침실이에요. 둘 다 '옛 침실' 분위기로 골랐어요.
- 텍스트 수정 3건은 Mac 원본(ch04_text.yaml)에 아직 반영 안 됐어요.

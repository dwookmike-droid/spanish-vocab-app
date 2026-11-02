# AUDIT · ch05 El patio y el jardín (v6, 2026-11-02)

## 텍스트 검수 (Claude Code 산출물)
- 결과: **통과**. validate_text.py 오류 0 · 경고 2 — ① regadera를 중남미어로 표시(오탐: 스페인에서도 '물뿌리개'가 기본 뜻, 멕시코 '샤워기' 뜻은 §6 변이에 이미 있음) ② humanizer 감사 스크립트 없음(ch04와 같음). `--all`도 통과.
- 확인한 것: 스페인 표준(카스티야) 표현, 관사·성(la flor 여성, el césped·el árbol 강세 부호 설명 맞음, jardín→jardines 부호 빠짐 맞음), EN/KO 뜻, 단어별 직역, gran/grande 어순(단수 명사 앞 gran = 평가, 명사 뒤 grande = 크기, 복수 앞 grandes 그대로, viejo·pobre도 자리 따라 뜻 바뀜, 보통 형용사는 명사 뒤), 연습 5문항 모두 이 포인트. 발음 규칙(p/t/k→ㅃㄸㄲ: 빠띠오·뽀소·똘도, f만 ㅍ: 플로르·푸엔떼, ll/y→야: 바야·부간비야, c/z→ㅅ: 마세따·세스뻬드, 강세 굵게), 해요체, 길이 제한, 브랜드 없음. 소품 날짜 4 MAY = 여행일정.md(Córdoba ch05) 확인. 어원 4개·가짜 친구(el banco = 벤치/은행)·파티오 축제(5월, 사실) 맞아요.
- 사소한 수정 1건 (**box 사본 ch05_text_reviewed.yaml에만 반영**, Mac 원본은 그대로라 Claude Code 쪽에도 반영 필요):
  1. extras.grammar_ko[1] `el césped은` → `el césped는` (세스뻬드는 모음으로 끝나서 '는')
- 참고(수정 안 함): fountain 예문 en `in the patio's center`는 40자 제한 때문에 어색해도 그대로. `Hay grandes árboles` = 'great trees/멋진'은 gran 규칙과 일관(실제 회화에서는 그냥 '큰'으로도 많이 써요). 연습 1–4는 패턴·대조 문장과 같음.
- 빌드 스크립트가 reviewed yaml과 원본이 words · practice · word_order · scenes · cognates에서 같은지 assert해요.

## 페이지 (A4, 6쪽, 책 쪽번호 24–29) · 스킨 Azulejo · patio × 코르도바 파티오
p24 오프너(파란 화분 벽과 나무 문, Bodoni 이탤릭 제목, 흰 소인 Nº 05 · EL PATIO · 4 MAY / CÓRDOBA) · p25 단어 20(폴라로이드 «macetas azules», 핵심 카드마다 파란 화분 와시테이프, 거리 명판 Nº 05 — Córdoba / CALLE DE LAS FLORES, CORREO · CÓRDOBA · 4 MAY 소인, 꽃 이름 핀 GERANIO · BUGANVILLA / Nº 05 — Córdoba, 손글씨 un gran patio, muchas flores) · p26 Gran y grande(파티오 장면 라벨 5 + 단어 블록 5 + NOTA + 아줄레주 띠) · p27 Un gran patio, un patio grande(Nº1 gran·grande, Nº2 viejo·pobre, Nº3 보통 형용사 패턴, ¿Gran o grande? 대조 + 물뿌리개, 화분 벽 사진, Gramática 메모, 핵심 예문 8) · p28 En el patio(순서 맞히기·장면 6·지역 변이 5·닮은 말 4·가짜 친구·Curiosidad·메스키타 아치·로마 다리 띠·정답) · p29 Créditos(사진 26건)
색: 명사 앞 gran·grandes·viejo·pobre = 코발트, 명사 뒤(es 뒤) grande·viejo·pobre = 테라코타 (PDF·웹 동일).

## 인쇄 품질
| 항목 | print | screen |
|---|---|---|
| 크기 | 4.66 MB | 1.27 MB |
| 폰트 | 9개 서브셋 전부 임베드, Type 3 = 0 | 동일 |
| 사진 최저 ppi(종이 텍스처 제외) | 312 (오프너, 원본 2736×3648 한계 · 하한 300 통과) · 나머지 317 이상 | 약 150 (목표 150) |
| 최소 글자 (HTML / SVG) | 7.00pt / 7.21pt | 동일 |
| 넘침·겹침 (CHECK + 크레딧 칼럼) | 0 | 0 |

폰트: BodoniModa Regular/Italic, Jost, Gowun Batang Regular/Bold, Caveat, Special Elite (전부 CID TrueType 서브셋).
수정 내역: p25 꽃 이름 핀 막대가 범례 글줄을 가려서 짧게. p26 도입 문단이 두 줄로 넘쳐 사진 테이프와 겹침 → 끝의 point_ko 반복 문구 뺌(같은 내용이 부제에 있음). p27 Gramática 판이 대조 타일(코발트)과 붙어 한 덩어리로 보여서 테라코타색으로 바꾸고 3mm 내림.
카드 크롭 다시 함: la maceta(화분 3개가 다 보이게, 벽 낙서 제외), la reja(창살 + 아줄레주 창턱), el pozo(우물이 잘 보이는 코르도바 파티오 사진으로 교체).

## 사진 처리
- 리터칭 없음: 고른 사진에 읽히는 간판·로고·번호판이 없어요. el banco/la sombra 사진 뒤쪽의 작은 차는 카드 크기에서 알아볼 수 없어요(글자 없음).
- 누끼(rembg isnet): 물뿌리개·잎·호스.
- 코르도바 실사진: 오프너·폴라로이드·p26 장면(Fiesta de los Patios 2015)·p27 화분 벽·el patio(Patio del Zoco)·el jardín(알카사르 정원)·el árbol(오렌지 정원 분수)·la fuente(비아나 궁)·el pozo·la reja(calle del Pañuelo)·메스키타 아치·로마 다리. 나머지 카드(장미·제라늄·벤치·울타리·잔디·레몬나무·부겐빌레아·차양·해먹·그늘)는 지역 무관 사진.
- 기존 v6 원본 중 맞는 사진이 없어 전부 새로 받았어요(Commons 26건).

## 웹 (web_ch05/, zip 1.1 MB / 폴더 1.3 MB)
단어 20(예문 8 포함, 누끼 3장은 투명 WebP), 장면 사진 2, 단어 블록 5, 형용사 패턴 3·대조, 화분 벽 예문, NOTA, Gramática 메모, 순서 맞히기(정답 펼침), 장면 6, 지역 변이. 음성 54개(es-ES-ElviraNeural, mono 24kHz 32kbps), WebP 42장. 참조 누락 0.

## 남은 점
- p26 사진 라벨 5개(Es una fuente grande. / Hay una gran buganvilla. / Una maceta pequeña / Los geranios rojos / Un árbol grande)는 디자인 쪽에서 붙인 쉬운 문장이에요(pequeña는 원고에 없는 단어). p27 화분 벽 라벨은 la maceta 예문 재사용.
- la flor 카드는 장미 사진(꽃 일반), 레몬나무·부겐빌레아는 인도에서 찍은 사진이에요(스페인 특정 아님).
- 텍스트 수정 1건은 Mac 원본(ch05_text.yaml)에 아직 반영 안 됐어요.

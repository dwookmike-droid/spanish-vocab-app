# AUDIT · ch07 Tapas y pintxos (v6, 2026-11-02)

## 텍스트 검수 (Claude Code 산출물)
- 결과: **통과, 수정 0건**. validate_text.py 오류 0 · 경고 0 (Mac 검증기 --humanizer 포함. box에서는 humanizer 스크립트가 없어 경고 1건만 나왔고, Mac 쪽 실행으로 해소). humanizer 감사는 따옴표·괄호 문장부호 참고 메모만 나왔어요(정보용).
- 확인한 것:
  - 스페인 표준 표현: la caña, el camarero, las gambas, el palillo, el vermut, la ración. 중남미·바스크 형태는 노트와 §6 변이에 따로 있어요.
  - 관사·성: la croqueta, el jamón, el pulpo, los calamares, la servilleta, el plato pequeño 등. EN/KO 뜻, 단어별 직역도 확인했어요.
  - 어순 포인트 gustar: 좋아하는 것이 주어라 동사 뒤에 오고, 단수면 gusta·복수면 gustan. no는 me 앞, a mí는 강조, 주어에는 정관사. 문장 5 · 패턴 3 · 대조 3 · 맞장구 4가 모두 이 포인트이고, 연습 5문항 중 4문항이 gustar예요.
  - 발음 규칙: p/t/k→ㅃㄸㄲ, ll→야/요, c/z→ㅅ, j→ㅎ, 강세 굵게. 해요체, 길이 제한, 브랜드 없음.
  - 소품 날짜: 10 MAY / 10 de mayo = Donostia ch07 일정이고, 다음 기착지 11 MAY Donostia(ch16)와도 맞아요.
- word_changes: el pintxo → el pincho. 카스티야 표준 철자이고, 바스크 표기 pintxo는 노트·변이·소품(PINTXOS 소인, «caña + pintxo», «la barra de pintxos»)과 장 제목에 남아 있어요. 타당한 변경이에요.
- 참고(수정 안 함): 패턴 3의 «te gusta — 너는 좋아해»만 반말이에요. tú(너)를 보여 주는 뜻풀이라 일부러 그런 것으로 보고 그대로 뒀어요.
- 빌드는 Mac 원본과 같은 ch07_text.yaml(md5 d1ec5e52…)을 그대로 읽어요. 검수본 사본은 없어요.

## 페이지 (A4, 6쪽, 책 쪽번호 36–41) · 스킨 Mercado × 도노스티아 구시가 핀초 바
- **p36 오프너**: 구시가 핀초 카운터(손글씨 칠판 메뉴) 전면 사진, Bodoni 이탤릭 제목, 흰 이쑤시개 깃발 배지 PINTXOS · 10 MAY / Donostia.
- **p37 단어 20**: 칠판 «Hoy en la barra», 폴라로이드 «la barra de pintxos»(31 de Agosto 거리), 슬레이트 가격판 caña + pintxo 3,50 €, 손글씨 me gustan las croquetas. 핵심 카드 8장은 사진 속 음식에 이쑤시개 깃발이 꽂혀 있고, 나머지 12장은 바 냅킨 카드에 이쑤시개를 꽂았어요.
- **p38 Me gusta, me gustan**: 핀초 바 장면 사진에 gustar 라벨 4개, 단어 블록 5, NOTA, 라 콘차 물결 띠, 이쑤시개 깃발 «jamón · queso / con palillo».
- **p39 Gusta o gustan**:
  - Nº1 gusta + 단수, Nº2 gustan + 복수, 각각 색 블록 me · gusta · el vino / me · gustan · las gambas.
  - Nº3 누가 좋아하나요(2열), 칠판 ¿Qué va primero?(대조 3) + 핀초 누끼.
  - §2 ¿Te gusta?(맞장구 4), 갈색 Gramática 판, 크로케타 사진 띠, 핵심 예문 8.
- **p40 En la barra**: 순서 맞히기, 장면 6, 지역 변이 7, 닮은 말 4, 가짜 친구 tapa ≠ tap, Curiosidad pincho/pinchar + 길다 원형 사진, PINTXOS 소인, 핀초 진열 띠, 정답.
- **p41 Créditos**: 사진 26건.
- 색: 누구에게(me · te · le · nos · a mí) = 파랑, gusta/gustan = 빨강, 좋아하는 것(주어) = 초록, no = 호박색. PDF와 웹이 같아요. 단어 블록에서는 대명사·gustar를 항상 색칠하고, 주어 칸은 원고 highlight를 따라요.

## 인쇄 품질
| 항목 | print | screen |
|---|---|---|
| 크기 | 3.46 MB | 0.99 MB |
| 폰트 | 10개 서브셋 전부 임베드, Type 3 = 0 | 동일 |
| 이미지 최저 ppi (pdfimages) | 300 (종이 텍스처 · 오프너 원본 312ppi, 2579×3648) | 148 (목표 150) |
| 최소 글자 (HTML / SVG) | 7.00pt / 7.38pt | 동일 |
| 넘침·겹침 (CHECK + 크레딧 칼럼 680/680) | 0 | 0 |

- 폰트: BodoniModa Regular/Italic, Jost, Gowun Batang Regular/Bold, Caveat, Special Elite, Nanum Pen. 모두 CID TrueType 서브셋이에요.
- PNG를 보고 고친 것:
  - p37: 핵심 카드 깃발이 범례 줄과 손글씨를 가려서 사진 안(음식에 꽂힌 모양)으로 옮겼어요. 슬레이트가 폴라로이드 캡션을 가려서 내렸고, 폴라로이드 옆 장식 깃발은 뺐어요.
  - p39: Nº1·Nº2 판이 길어 아래 상자와 겹쳤어요. 직역 줄을 블록 옆으로 붙이고, Nº3을 2열로 만들고, 오른쪽 단을 §2 → Gramática → 크로케타 사진 순서로 다시 쌓았어요(DOM 측정으로 겹침 0 확인).
  - p38: 이쑤시개 깃발 라벨 글자가 깃발 밖으로 넘쳐서 키웠고, 제목 오른쪽 위로 옮겼어요.
  - 오프너: 아래쪽 그라데이션을 조금 진하게 해서 제목이 읽히게 했어요.

## 사진 처리
- 상표·가게 이름 처리:
  - el camarero: 셔츠 가슴의 식당 이름(노란 글자)을 지웠어요(inpaint + 노이즈 맞춤).
  - la barra: 오른쪽 아래 음료 상자(브랜드)와 위쪽 병 진열대가 프레임 밖에 오게 잘랐어요.
  - p38 장면: 위쪽 종이 배너를 잘라냈어요.
  - 맥주 브랜드 탭과 가게 간판이 보이는 후보 사진(CC0) 1장은 쓰지 않았어요.
- 남아 있는 것: 오프너 칠판의 손글씨 메뉴(TXISTORRA, CHAMPIÑÓN 등 음식 이름)는 상표가 아니라 바 분위기라 그대로 뒀어요. 장면 사진 속 병 라벨은 읽히지 않는 크기예요.
- 누끼(rembg isnet): 이쑤시개 통, 와인 잔, 작은 접시, 핀초 1개(p39 장식).
- 도노스티아 실사진: 오프너, p38 장면, p40 핀초 진열 띠, 폴라로이드(구시가 31 de Agosto 거리). 나머지 카드는 스페인 바 사진 위주예요(핀초 = 비토리아, 종업원 = 팜플로나, 카운터 = 엘체).
- Commons에서 새로 받은 사진 26건을 썼어요. 카드 사진은 HERO 1000×816 / TAG 800×608이고, PDF에서 577ppi 이상이에요.

## 웹 (web_ch07/, zip 0.87 MB / 폴더 1.1 MB)
- 단어 20(예문 8 포함, 누끼 3장은 투명 WebP), 장면 사진 3(바 장면 · 크로케타 · 길다).
- 단어 블록 5, gusta/gustan 패턴 3, 대조, 맞장구, NOTA, Gramática, 순서 맞히기(정답 펼침), 닮은 말·가짜 친구, 장면 6, 지역 변이.
- 음성 57개(es-ES-ElviraNeural, mono 24kHz 32kbps), WebP 43장. 참조 누락 0.

## 남은 점
- p38 사진 라벨 4개(Me gusta el jamón / el camarero / Me gustan los pinchos / Me gusta el vino)는 디자인 쪽에서 붙인 쉬운 문장이에요(원고 패턴으로 만든 것).
- 이쑤시개 깃발 라벨 «jamón · queso / con palillo»(원고 label 소품)는 p38 제목 옆에 장식으로 두었어요.
- 오프너 사진은 실내 조명이라 따뜻하고 약간 어두워요. 인쇄 전에 교정쇄로 확인하면 좋아요.

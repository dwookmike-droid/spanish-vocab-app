# AUDIT · ch03 El salón (v6, 2026-11-02)

## 텍스트 검수 (Claude Code 산출물)
- 결과: **통과**. 스페인 표준(카스티야) 표현, 관사·성, EN/KO 뜻, 단어별 직역, 위치 표현(al lado de · delante de · detrás de · encima de · debajo de · enfrente de · entre) 어순, de+el=del / a+el=al, está/hay 대조, 발음 규칙(p/t/k→ㅃㄸㄲ, f만 ㅍ, ll/y→야/요, c/z→ㅅ, 강세 굵게), 해요체, 브랜드 없음, 소품 날짜 23 MAY 확인.
- 사소한 수정 1건: variants `el suelo → el piso (같은 뜻)` → `el piso (중남미)` (스페인에서 piso는 주로 '아파트·층'). **box 사본(ch03_text_reviewed.yaml)에만 반영**, Mac 원본 텍스트는 그대로 — Claude Code 쪽에도 반영 필요.
- 참고(수정 안 함): practice 3·4가 word_order 문장 4·5와 같은 문장 / "의자 둘 사이에"는 "의자 두 개 사이에"도 가능.
- 빌드 스크립트에서 reviewed yaml이 원본과 variants 1줄만 다른지 assert.

## 페이지 (A4, 6쪽, 책 쪽번호 12–17) · 스킨 Azulejo × patio
p12 오프너(Casa de Pilatos 안뜰, Bodoni 이탤릭 제목) · p13 단어 20(타일 액자 폴라로이드·거리 명판·소인) · p14 ¿Dónde está?(거실 장면 사진 라벨 5 + 단어 블록 5 + NOTA + 타일 띠) · p15 Al lado, encima, debajo(위치 도식 6·축약 del/al·está/hay 대조·Sin sujeto·핵심 예문 8) · p16 En el salón(순서 맞히기·장면·지역 변이·닮은 말·가짜 친구·Curiosidad·정답) · p17 Créditos

## 인쇄 품질
| 항목 | print | screen |
|---|---|---|
| 크기 | 5.68 MB | 1.56 MB |
| 폰트 | 9개 서브셋 전부 임베드, Type 3 = 0 | 동일 |
| 사진 최저 ppi(종이 텍스처 제외) | 316 (목표 320, 하한 300; 원본은 전부 333ppi 이상) | 149 (목표 150) |
| 최소 글자 (HTML / SVG) | 7.00pt / 7.21pt | 동일 |
| 넘침·겹침 (CHECK) | 0 | 0 |

폰트: BodoniModa Regular/Italic, Jost, Gowun Batang Regular/Bold, Caveat, Special Elite (전부 CID TrueType 서브셋).
수정 내역: p14 §1이 NOTA와 겹침 → 장면 사진 100→90mm, 블록 위로. 소인 원형 글자 6.33pt → 소인 41mm로 키워 7.21pt. 거리 명판이 drop-shadow 필터로 래스터화되던 문제 → SVG 그림자로 바꿔 벡터 유지(리모컨 필터도 제거). p16 소인은 상자와 겹쳐 뺌. 그림 카드에 금색 액자 테두리.
※ p16 타일 띠 캡션의 text-shadow만 회색 흐림 이미지(709×69, 300ppi)로 들어가요. 글자 자체는 벡터.

## 사진 처리
- 시계: 다이얼 상표 글자 지우고 초침 다시 그림. TV: 앞판 상표 필기체 클론으로 지움. 책장: 출판사 글자 읽히지 않게 전체 보기 크롭. 소파 사진: 컵·포장지 크롭 아웃.
- 그림(el cuadro): 처음 고른 Sorolla 「목욕」은 아이 누드라 「Strolling along the Seashore」(퍼블릭 도메인)로 교체.

## 웹 (web_ch03/, zip 820 KB / 폴더 1.1 MB)
단어 20(예문 8 포함, 누끼 6장은 투명 WebP), 장면 사진 2, 단어 블록 5, 위치 패턴·축약·대조, Sin sujeto, NOTA, 순서 맞히기(정답 펼침), 장면 5, 지역 변이. 음성 52개(es-ES-ElviraNeural, mono 24kHz 32kbps), WebP 42장. 색: 위치 표현 코발트, está 황토, hay 빨강.

## 남은 점
- p14 사진 라벨 5개와 p15 그림 사진 라벨은 디자인 쪽에서 붙인 쉬운 문장(텍스트 원고의 word_order 문장 재사용 1개 포함).
- p13 폴라로이드 캡션 "azulejos del patio"는 원고 소품 문구 그대로인데, 사진은 Plaza de España 타일 벤치예요(같은 세비야 아줄레호).
- 벽(la pared) 카드는 알카사르 타일 벽+덧창 디테일이라 썸네일이 조금 어두워요.

# AUDIT · ch02 La cocina (v6, 2026-11-02)

## 텍스트 검수 (Claude Code 산출물)
- 결과: **통과** — 오타 수정 없음. 스페인 표준(카스티야) 표현, 관사·성, EN/KO 뜻, 단어별 직역, hay/está·장소 뒤 어순, 발음 규칙(p/t/k→ㅃㄸㄲ, f만 ㅍ, ll/y→야/요, c/z→ㅅ, 강세 굵게), 해요체, 브랜드 없음, 소품 날짜 5 MAY 확인.
- data_v6.py CH02(es/en/ko/core/발음)와 yaml 일치를 빌드 스크립트에서 assert.

## 페이지 (A4, 6쪽, 책 쪽번호 6–11)
p6 오프너 · p7 단어 20 · p8 Hay y está(장면 사진 라벨 + 단어 블록) · p9 ¿Hay o está?(가격표 패턴·칠판 대조·Hay no cambia·핵심 예문 8) · p10 En la cocina(순서 맞히기·장면·지역 변이·닮은 말·가짜 친구·Curiosidad·정답) · p11 Créditos

## 인쇄 품질
| 항목 | print | screen |
|---|---|---|
| 크기 | 3.83 MB | 1.06 MB |
| 폰트 | 8종 전부 임베드, Type 3 = 0 | 동일 |
| 사진 최저 ppi(종이 텍스처 제외) | 317 (목표 320, 하한 300) | 149 (목표 150) |
| 최소 글자 (HTML / SVG) | 7.00pt / 7.38pt | 동일 |
| 넘침·겹침 (CHECK) | 0 | 0 |

폰트: BodoniModa Regular/Italic, Jost, Gowun Batang Regular/Bold, Caveat, Nanum Pen Script, Special Elite (전부 CID TrueType 서브셋).
수정 내역: 가격표 한글 제목이 Caveat 700→Nanum Pen 가짜 볼드로 Type 3가 되던 문제 → 한글만 Pen 400 span으로 분리. 칠판 'á'·'→' Tinos 대체 → Caveat/Gowun 지정.

## 웹 (web_ch02/, zip 648 KB / 폴더 920 KB)
단어 20(예문 8 포함), 단어 블록 5, 패턴·대조·Hay no cambia, 순서 맞히기(정답 펼침), 장면 5. 음성 51개(es-ES-ElviraNeural, mono 24kHz 32kbps), WebP 1x/2x 41장.

## 남은 점
- 오프너는 v6 결정대로 Mercado Central 정면 사진(작업지시서의 시장 노점 컷 아님).
- p8 사진 라벨 5개(Hay un mortero 등)는 디자인 쪽에서 붙인 쉬운 문장(텍스트 원고에는 없음).
- 냉장고 썸네일은 기존 사진 유지(더 나은 무료 사진 못 찾음).

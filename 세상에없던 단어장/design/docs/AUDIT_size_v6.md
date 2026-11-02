# 용량 최적화 점검 (v6, 2026-11-02 KST)

| 파일 | 이전 | 이후 |
|---|---|---|
| 인쇄용 PDF `…_print.pdf` | 17.91 MB (원본 `…_creditos.pdf`, 백업 유지) | 7.81 MB |
| 화면용 PDF `…_screen.pdf` | – | 2.17 MB |
| 웹 `web/` | 9.13 MB (`_backup/web_v6_full`) | 1.64 MB (이미지 0.83 · 음성 0.77 · HTML 0.04) |

- pdffonts: 3개 PDF 모두 10개 CID TrueType, emb/sub/uni 전부 yes, Type 3 0개
- pdfimages(smask·배경지 제외) 최소 실효 해상도: 원본 312 / print 312 / screen 149 ppi (배경지 텍스처 300ppi, 원래 해상도 유지)
- print: Flate→JPEG 31건, linearized(Optimized: yes), XMP 제거, 11쪽, 추출 단어 수 4681 (원본과 동일)
- 화질(200dpi 렌더 PSNR, 원본 대비): p3 36.3 · p4(텍스트) 48.5 · p8(오프너 사진) 37.8 · p9(사진 카드) 37.3 dB / screen 33.2 · 42.9 · 30.3 · 32.4 dB
- 비교 이미지: `_shots/compare_size_v6.png` (200dpi 크롭: p8 사진, p9 카드, p4 텍스트 / 원본·print·screen)
- 웹: 이미지 60개 깨짐 0, 2x srcset 정상, 음성 85개 메타데이터 로드 85/85, 스크린샷 `_shots/web_v6_opt.png`

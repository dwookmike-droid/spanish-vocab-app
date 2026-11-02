# 빌드 규칙 (v6~, 모든 새 챕터 공통)

`python3 _build/build_all.py` 한 번이면 아래가 순서대로 실행돼요. 새 챕터는 data_v6.py / build_v6.py에 추가만 하면 용량 최적화가 자동 적용돼요.

| 산출물 | 규칙 |
|---|---|
| `*_print.pdf` | 텍스트·선 벡터 유지, 폰트 임베드+서브셋(Type 3 없음). 사진은 배치 크기 기준 실효 해상도를 측정해 330ppi 초과분만 320ppi로 다운샘플(하한 300ppi, 미만이면 빌드 실패). JPEG q86 4:2:0. 컷아웃은 JPEG + 무손실 그레이 SMask. 중복 이미지 병합, XMP 제거, 미사용 리소스 제거, linearize. Ghostscript 미사용(폰트/벡터 변형 방지). |
| `*_screen.pdf` | 150ppi(하한 140), q78. 화면 열람·공유용. |
| `web/` | 카드 박스(260×110 CSS px)에 맞춘 WebP 1x/2x + srcset, loading=lazy, decoding=async, width/height 지정. 음성은 TTS 원본을 `_build/tts_cache`에 두고 배포본은 MP3 mono 24kHz 32kbps, preload=none. |
| 원본 PDF | `render_v6.py` 결과(무최적화)는 비교·백업용으로만 유지. |

핵심 모듈: `_build/optimize.py` (`MEASURE_JS`, `make_assets`, `postprocess`), `_build/render_opt_v6.py`, `_build/web_v6.py`.
점검: `pdffonts`, `pdfimages -list`(smask·배경지 제외 최소 ppi ≥300), 200dpi 크롭 비교(`_shots/compare_size_v6.png`).

# design/ — Grok Bot 전용 (비주얼·디자인·레이아웃·빌드)

Claude Code는 이 폴더를 수정하지 않아요.

| 폴더 | 내용 |
|---|---|
| deliverables/v6/ | 현재 결과물: 인쇄용 PDF(7.8MB, 사진 300ppi 이상), 화면용 PDF(2.2MB, 150ppi), web/(오디오 포함 웹판, 1.6MB) |
| docs/ | 총 목차 TOC_v6, 디자인 시스템, 사진 출처(CREDITS), 점검 기록(AUDIT, 용량 점검) |
| build/v6/ | v6 빌드 스크립트 사본 + README_build.md (실행은 박스에서) |
| build/text_import.py | 텍스트 YAML → 빌드 데이터 변환 |
| build/텍스트_가져오기.md | 텍스트 인계 절차 |
| assets/ | ch01·ch02·ch11 사진·컷아웃, 공용 종이 질감, 폰트 |
| shots/ | 페이지 미리보기 p01~p11, 비교 이미지 |

박스의 대용량 캐시(원본 사진 후보, 썸네일, TTS 원본 등 약 330MB)는 iCloud 용량 때문에 넣지 않았어요. 박스 `/workspace/trilingual/es/v6/_build/`에 그대로 있어요.

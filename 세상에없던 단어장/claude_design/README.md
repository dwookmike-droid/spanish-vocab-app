# claude_design — Claude Code 빌드 폴더 (ch09~ch24, 인쇄용 PDF만)

그록봇 영역(`design/`)과 겹치지 않게 프로젝트 맨 위에 따로 둬요. 그록봇 파일은 여기서 읽기만 하고 고치지 않아요.

v6 디자인 문법(그록봇 `_build`)을 그대로 따르고, 아래 결정만 바꿔요.

## 디자인 결정 (2026-11-02, Mike 승인)
| 항목 | v6 (그록봇) | 바꾼 것 |
|---|---|---|
| 한글 글꼴 | Gowun Batang 400/700 | **Pretendard 400/700** (`fonts/Pretendard-*.ttf`). CSS 글꼴 이름 `'Gowun'`의 src만 바꿔 끼우면 나머지 규칙은 그대로예요. 손글씨용 Nanum Pen은 그대로 |
| 단어 쪽 범례 줄 | 제목이 두 줄이면 1행 카드 테이프·사진에 가려짐 (p25, p31, p37) | 범례 줄과 1행 카드 사이 간격을 제목 줄 수에 맞춰 띄움 — 빌드할 때 겹침 0 확인 |
| 결과물 | 인쇄·화면 PDF, 웹판, 음성 | **인쇄용 PDF만** |

## 글꼴 메모
- Pretendard는 원래 OTF(CFF) 형식이라 Chrome PDF에 넣으면 Type 3 글꼴이 돼요. 그래서 `tools/otf2ttf.py`로 TrueType으로 바꿔서 써요. 바꾼 뒤에는 PDF에 TrueType으로 들어가고 Type 3는 0이에요.
- 원본: `~/Library/Fonts/Pretendard-Regular.otf`, `Pretendard-Bold.otf`. 라이선스는 SIL OFL 1.1이라 형식을 바꿔 PDF에 넣어도 돼요.
- 시험 출력(ch01·ch02 3쪽)에서 v6 레이아웃 칸 안에 그대로 들어갔어요. Noto Sans KR은 폭이 넓어 줄이 넘쳐서 고르지 않았어요.

## 아직 없는 것
- 그록봇 `_build` 코드와 ch03~ch08 사진은 `design/build/v6_handoff/`로 받는 중이에요 (요청서: `그록봇_요청_빌드코드인계.md`).
- 빌드용 Python 환경(playwright, pikepdf, fonttools)은 세션마다 새로 설치해야 해요.

# Vocabulario visual — 웹앱

『Vocabulario visual』 스페인어 편 텍스트와 v6 사진·음성으로 만든 학습 웹앱이에요. 빌드 도구 없이 정적 파일만으로 돌아가요.

## 기능 (장마다)
- **단어**: 사진, 한글 발음(강세 굵게), 뜻, 예문, ▶ 발음 듣기, 전체 듣기, 뜻 가리기, 장면 문장·문법 메모
- **플래시카드**: 스페인어→뜻 / 뜻→스페인어, 알아요·몰라요로 간격 반복(라이트너 5단계)
- **퀴즈**: 뜻 고르기, 스페인어 고르기, 듣고 고르기, 사진 보고 고르기 (10문제, 틀린 단어는 복습함으로)
- **어순**: 블록으로 보는 문장, 블록 눌러 문장 만들기, 패턴 표
- **대화**: 장소별 상황 대화 2개, 교재 표현 / 원어민 표현 / 비교 보기, 단어 누르면 뜻·발음
- **읽기**: 짧은 글 2개(A1~A2), 단어 누르면 뜻·발음·기본형, 번역 보기, 내용 확인 문제
- **복습**: 여러 장에서 복습할 때가 된 카드만 모아서

진도는 브라우저(localStorage)에만 저장돼요. 기기를 바꾸면 처음부터예요.

## 들어 있는 장
사진·음성이 있는 ch01~ch07, ch11에 사진 없는 ch08을 더해 9개 장이에요. 이 목록은 `tools/build_data.py`의 `CHAPTERS`에서 바꿔요.
v6 mp3가 없는 문장(새 대화·읽기, ch08)은 기기에 내장된 스페인어 음성(Web Speech API)으로 읽어요. 테두리가 옅은 ▶가 그 버튼이에요.

## 폴더
```
webapp/
├─ index.html, app.js, app.css   화면 (그대로 배포)
├─ data/                         build_data.py가 만든 JSON (장별)
├─ media/                        build_data.py가 복사한 사진(webp)·음성(mp3)·출처 문서
├─ content/chNN_extra.yaml       웹 전용 대화·읽기·단어 사전 (형식: content/SCHEMA_extra.md)
└─ tools/
   ├─ build_data.py              es/chNN/text + content + design 결과물 → data/, media/
   └─ check_extra.py             chNN_extra.yaml 검사 (대화 줄 수, 읽기 길이, 사전 누락 단어)
```
원본(`es/`, `design/`)은 읽기만 해요.

## 고친 뒤 다시 만들기
```bash
python3 webapp/tools/check_extra.py webapp/content/ch*_extra.yaml
python3 webapp/tools/build_data.py
```

## 내 컴퓨터에서 보기
```bash
cd webapp && python3 -m http.server 8000
```
브라우저에서 http://localhost:8000 을 열어요.

## 배포
`main`에 `webapp/`이 바뀌어 올라가면 `.github/workflows/pages.yml`이 GitHub Pages로 배포해요.
처음 한 번은 GitHub 리포의 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 바꿔야 해요.

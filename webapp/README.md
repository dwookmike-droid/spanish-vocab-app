# Vocabulario visual — 웹앱

『Vocabulario visual』 스페인어 편 텍스트와 v6 사진·음성으로 만든 학습 웹앱이에요. 빌드 도구 없이 정적 파일만으로 돌아가고, `index.html`을 파일로 바로 열어도 동작해요.

## 기능 (장마다)
- **단어**: 사진, 한글 발음(강세 굵게), 뜻, 예문, ▶ 발음 듣기, 전체 듣기, 뜻 가리기, 장면 문장·문법 메모
- **플래시카드**: 스페인어→뜻 / 뜻→스페인어, 알아요·몰라요로 간격 반복(1·2·4·8·16일). 키보드 ←/→
- **퀴즈**: 섞어서 / 객관식(뜻·스페인어·듣기·사진) / 쓰기(강세 키 제공, 강세만 틀리면 '거의 맞음') / el·la 관사 고르기
- **받아쓰기**: 듣고 문장 입력 → 단어별로 맞음·강세 틀림·빠짐 표시와 점수. 짧은/긴 문장, 천천히 듣기, 뜻 힌트
- **말하기**: 단어·문장·원어민 표현을 따라 말하면 음성 인식(es-ES)으로 채점. 내 목소리 녹음해서 원어민과 비교
- **어순**: 블록으로 보는 문장, 블록 눌러 문장 만들기, 패턴 표
- **대화**: 상황 대화 2개, 교재 / 원어민 / 비교 보기, 대화 듣기, **역할극**(내 대사는 가리고 직접 말하기 → 채점)
- **읽기**: 짧은 글 2개(A1~A2), 단어 누르면 뜻·발음·기본형, ☆로 내 단어장에 저장, 번역 보기, 내용 확인 문제

## 전체
- **홈**: 연속 학습일, 오늘 목표 진행, 외운 단어 수, 최근 7일 그래프, 마지막에 하던 곳 이어서 하기
- **복습**: 복습할 때가 된 카드(장 단어 + 내 단어장)만 모아서
- **내 단어장**: 대화·읽기에서 저장한 단어 목록과 플래시카드
- **찾기**: 스페인어·한국어·영어로 전 장 단어와 대화·읽기 단어 검색 (강세 없이 써도 찾아요)
- **설정**: 하루 목표, 듣기 속도, 한글 발음 숨기기, 화면 테마, **진도 백업·불러오기**, 진도 지우기
- **설치·오프라인**: 휴대폰에서 '홈 화면에 추가'하면 앱처럼 열리고, 한 번 연 화면은 인터넷 없이도 돼요 (https로 배포했을 때)

진도는 브라우저(localStorage)에만 저장돼요. 기기를 바꿀 때는 설정에서 백업 파일을 받아 옮겨요.
음성 인식은 Chrome(안드로이드·PC)과 Safari(iPhone)에서 돼요. 마이크 권한을 허용해야 해요.

## 들어 있는 장
사진·음성이 있는 ch01~ch07, ch11에 사진 없는 ch08을 더해 9개 장이에요. 이 목록은 `tools/build_data.py`의 `CHAPTERS`에서 바꿔요.

## 음성
1. `content/audio/gm_*.mp3` — Gemini TTS로 만든 음성 (있으면 이걸 먼저 써요)
2. v6 mp3 — 그록봇이 만든 기존 음성
3. 둘 다 없으면 기기에 내장된 스페인어 음성 (테두리가 옅은 ▶)

Gemini 음성 만들기 (키는 환경 변수로만, 파일에 쓰지 않아요):
```bash
python3 webapp/tools/build_data.py
GEMINI_API_KEY=... python3 webapp/tools/gen_audio_gemini.py
python3 webapp/tools/build_data.py
```
무료 등급은 TTS가 모델당 하루 10번이라, 전체(약 700줄)를 만들려면 결제를 연결한 키가 필요해요. 이미 만든 줄은 건너뛰니 몇 번에 나눠 돌려도 돼요.

## 폴더
```
webapp/
├─ index.html, app.js, app.css   화면
├─ sw.js, manifest.webmanifest, icons/   설치·오프라인
├─ data/                         build_data.py가 만든 JSON + bundle.js
├─ media/                        build_data.py가 복사한 사진·음성·출처 문서
├─ content/chNN_extra.yaml       웹 전용 대화·읽기·단어 사전 (형식: content/SCHEMA_extra.md)
├─ content/audio/                Gemini 음성 원본
└─ tools/
   ├─ build_data.py              es/chNN/text + content + design 결과물 → data/, media/
   ├─ check_extra.py             chNN_extra.yaml 검사
   ├─ gen_audio_gemini.py        Gemini TTS로 음성 만들기
   └─ smoke.js                   모든 화면·기능 자동 점검 (Playwright)
```
원본(`es/`, `design/`)은 읽기만 해요.

## 고친 뒤 다시 만들고 점검하기
```bash
python3 webapp/tools/check_extra.py webapp/content/ch*_extra.yaml
python3 webapp/tools/build_data.py
node webapp/tools/smoke.js
```
`app.js`·`app.css`·데이터를 바꿔서 배포할 때는 `sw.js`의 `VERSION`을 올려야 휴대폰에 새 파일이 내려가요.

## 내 컴퓨터에서 보기
```bash
cd webapp && python3 -m http.server 8000
```
브라우저에서 http://localhost:8000 을 열어요.

## 배포
`main`에 `webapp/`이 바뀌어 올라가면 `.github/workflows/pages.yml`이 GitHub Pages로 배포해요.
처음 한 번은 GitHub 리포의 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 바꿔야 해요.

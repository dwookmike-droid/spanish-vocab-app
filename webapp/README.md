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
24개 장 전부예요. 사진은 ch01~ch07·ch11(v6 웹판)과 ch09(인쇄용 디자인 폴더)에 있고, 나머지 장은 사진 없이 글과 음성으로 공부해요. 장 목록은 `tools/build_data.py`의 `CHAPTERS`에서 바꿔요.

## 음성
기기에 내장된 기계 음성은 쓰지 않아요. 모든 문장과 누를 수 있는 단어에 사람 같은 음성 파일이 있어요.
1. **v6 음성**: 그록봇이 만든 단어·예문·장면 음성 (스페인 여성 목소리). 있으면 이걸 써요.
2. **Kokoro 음성**: 나머지 전부 (대화, 읽기, ch08·ch11 문장, 단어 사전). 오픈소스 모델이라 무료이고 이 컴퓨터에서 바로 만들어요.
   - 목소리 3개를 섞어 써요: 여성 `ef_dora`, 남성 `em_alex`, 남성 `em_santa`
   - 대화는 역할마다 다른 목소리(남녀 한 쌍), 읽기 글은 글마다 한 목소리, 단어는 셋이 돌아가며 읽어요.

글을 고치거나 새 장을 넣은 뒤 음성 만들기:
```bash
pip install kokoro-onnx soundfile
python3 webapp/tools/build_data.py        # 음성이 없는 줄을 content/audio_manifest.json에 적어요
python3 webapp/tools/gen_audio_kokoro.py  # 없는 줄만 만들어요 (처음엔 모델 350MB를 GitHub에서 받아요)
python3 webapp/tools/build_data.py
```
`gen_audio_gemini.py`도 남겨 뒀어요. Gemini 키에 결제가 연결되면 쓸 수 있어요.

claude.ai 미리보기처럼 파일 수가 제한된 곳에 올릴 때는 음성을 장별 묶음으로 합친 사본을 만들어요:
```bash
python3 webapp/tools/build_data.py --preview /tmp/vv-preview
```

## 폴더
```
webapp/
├─ index.html, app.js, app.css   화면
├─ sw.js, manifest.webmanifest, icons/   설치·오프라인
├─ data/                         build_data.py가 만든 JSON + bundle.js
├─ media/                        build_data.py가 복사한 사진·음성·출처 문서
├─ content/chNN_extra.yaml       웹 전용 대화·읽기·단어 사전 (형식: content/SCHEMA_extra.md)
├─ content/audio/                Kokoro 음성 원본 (kk_*.mp3)
└─ tools/
   ├─ build_data.py              es/chNN/text + content + design 결과물 → data/, media/
   ├─ check_extra.py             chNN_extra.yaml 검사
   ├─ gen_audio_kokoro.py        Kokoro로 음성 만들기 (기본)
   ├─ gen_audio_gemini.py        Gemini TTS로 음성 만들기 (결제 키 필요)
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

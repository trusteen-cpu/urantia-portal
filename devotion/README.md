# 오늘의 묵상

하루에 한 편. 낭독 → 강론 → 노래 → 기도 순으로 자동 재생됩니다.

**mp3는 인터넷 아카이브에, 페이지는 깃허브에** 나눠 둡니다.
깃허브에는 텍스트 파일 두 개만 올라가므로 저장소가 몇 십 KB로 유지됩니다.

```
devotion/
├─ generate_audio_daily.py   ← 실행 스크립트 (깃허브에 올리지 않음)
├─ song_lyrics.txt           ← Suno 붙여넣기용 가사
├─ publish.sh                ← 아카이브 업로드 + 깃허브 배포 한 번에
└─ site/                     ← 이 폴더만 깃허브에
   ├─ index.html             ← 한 번 올리면 다시 손댈 일 없음
   ├─ content.js             ← 실행할 때마다 자동 갱신 (아카이브 주소가 들어감)
   ├─ .gitignore             ← audio/ 를 깃허브에서 제외
   └─ audio/                 ← 아카이브로 보낼 mp3 임시 보관함
      ├─ 20260817_01_reading.mp3
      ├─ 20260817_02_sermon.mp3
      ├─ 20260817_03_song.mp3
      └─ 20260817_04_prayer.mp3
```

파일 이름에 날짜가 붙는 이유: 아카이브에 같은 이름으로 덮어쓰면 재처리(derive) 동안
몇 분간 재생이 끊깁니다. 날짜를 붙여 새 파일로 올리면 그런 일이 없고, 지난 날짜 음성도
아카이브에 그대로 남아 나중에 다시 꺼내 쓸 수 있습니다.

현재 들어 있는 것: **2026-08-17 · 153:3.2 「먹을 수 없는 빵, 살아내는 빵」**

---

## 처음 한 번만 하는 준비

**1. 아카이브 항목 만들기**
archive.org 로그인 → Upload → 아무 mp3 하나 올려 항목을 만들고 식별자(identifier)를 정합니다.
예: `urantia-devotion-kr` → 주소는 `https://archive.org/details/urantia-devotion-kr`

스크립트 위쪽의 `ARCHIVE_ITEM` 을 그 식별자로 바꿉니다.

```python
ARCHIVE_ITEM = os.environ.get("ARCHIVE_ITEM", "urantia-devotion-kr")
```

**2. 업로드 명령 설치** (선택이지만 매일 쓰기 편합니다)

```bash
pip install internetarchive
ia configure          # archive.org 계정 입력, 한 번만
```

**3. 깃허브 연결**

```bash
cd site
git init && git branch -M main
git remote add origin https://github.com/<사용자이름>/<저장소>.git
git add . && git commit -m "첫 배포" && git push -u origin main
```

저장소 → Settings → Pages → Source를 `main` / `/ (root)` 로 지정하면 주소가 열립니다.

```
https://<사용자이름>.github.io/<저장소>/
```

---

## 매일 하는 일 (3단계)

### 1단계 — 본문 바꾸고 음성 만들기

`generate_audio_daily.py` 의 `CONTENT` 블록만 그날 것으로 바꿉니다.

| 항목 | 내용 |
|---|---|
| `date` | `2026-08-18` 형식. **비워 두면 실행한 날짜로 자동 설정**됩니다 |
| `reference` | `153:3.2` 같은 편장절 |
| `paper_title` / `section_title` | 편 제목과 절 제목 |
| `theme` / `one_line` | 화면 제목과 한 줄 묵상 |
| `reading` | 본문 구절 전체 |
| `sermon` / `prayer_body` | 강론 500~700자, 기도 300~400자 |

기도 첫머리 호칭은 손대지 않습니다. `INVOCATIONS` 14가지가 날짜에 따라 자동으로 돌아갑니다
(삼위일체 하나님, 사랑이 많으신 하나님 아버지, 자비가 끝이 없으신 아버지 …).

```bash
cd devotion
export ELEVENLABS_API_KEY="발급받은키"      # Windows: set ELEVENLABS_API_KEY=...
python generate_audio_daily.py
```

mp3 세 개가 `site/audio/` 에 날짜 이름으로 만들어지고, `site/content.js` 에는
아카이브 재생 주소가 자동으로 들어갑니다. 실행이 끝나면 노래 파일에 쓸 이름을 화면에 알려줍니다.

### 2단계 — 곡 만들기

`song_lyrics.txt` 를 Style / Title / Lyrics 세 칸에 나눠 붙여넣고 Suno에서 생성합니다.
받은 파일을 화면에 안내된 이름(예: `site/audio/20260817_03_song.mp3`)으로 저장합니다.

### 3단계 — 올리기

```bash
./publish.sh
```

mp3 네 개를 아카이브로 올리고, 페이지를 깃허브에 밀어 넣습니다.
아카이브는 업로드 후 처리에 1~3분쯤 걸립니다. 그 사이에는 플레이어가 본문만 보여줍니다.

`ia` 명령을 설치하지 않으셨다면 화면에 나온 파일 목록을 archive.org 항목 페이지의
**Upload files** 로 직접 끌어다 놓으시면 됩니다. 깃허브 배포는 그대로 진행됩니다.

---

## 모두 깃허브에 두고 싶을 때

용량이 문제되지 않는다면 `ARCHIVE_ITEM = ""` 로 비우면 됩니다.
파일 이름에서 날짜가 빠지고(`01_reading.mp3`) 재생도 `audio/` 를 보게 됩니다.
이때는 `site/.gitignore` 의 `audio/` 한 줄을 지워야 mp3가 함께 올라갑니다.

---

## 플레이어 사용법

| 조작 | 자판 |
|---|---|
| 재생 / 멈춤 | 스페이스 |
| 10초 뒤로 / 앞으로 | ← → |
| 건너뛰기(다음 순서) | N 또는 Shift+→ |
| 이전 순서 | P 또는 Shift+← |
| 반복 방식 바꾸기 | R |

반복 방식 세 가지

- **전체 무한** — 낭독→강론→노래→기도가 끝나면 처음으로 돌아가 계속 이어집니다(기본값)
- **이 항목 무한** — 지금 듣는 항목 하나만 계속 반복합니다
- **한 번만** — 기도가 끝나면 멈춥니다

궤적 위의 점이나 이름을 눌러 원하는 순서로 바로 건너뛸 수 있습니다.
mp3가 아직 올라가지 않은 항목은 본문만 보여주고 읽을 시간만큼 머문 뒤 다음으로 넘어갑니다.

---

## 보안

- `generate_audio_daily.py` 는 `site/` **밖**에 두십시오. 웹에 올라가면 API 키가 노출됩니다.
- 깃허브에는 `site/` 폴더만 올립니다.
- 키는 환경변수로만 쓰고, 파일 안의 기본값은 지워두는 편이 안전합니다.

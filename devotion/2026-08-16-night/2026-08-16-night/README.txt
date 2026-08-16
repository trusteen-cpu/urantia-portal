오늘의 취침 묵상 2026-08-16
먼저 주셨기에 — 유란시아서 149:6.4
제149편 두 번째 전도 여행 · 주에 대한 두려움

────────────────────────────────────────
1단계  소리 만들기
────────────────────────────────────────
이 폴더에서 파워셸 창을 열고 아래 두 줄을 차례로 붙여 넣으십시오.

    pip install requests
    python generate_audio_daily.py

audio 폴더에 01_reading.mp3 · 02_sermon.mp3 · 04_prayer.mp3 가 생깁니다.
이미 있는 파일은 건너뜁니다. 다시 만들려면 그 파일을 지우고 실행하십시오.

────────────────────────────────────────
2단계  노래 만들기
────────────────────────────────────────
lyrics.txt 를 열어 스타일 프롬프트와 가사를 SUNO 에 붙여 넣고
완성된 곡을 audio/03_song.mp3 로 저장하십시오.

────────────────────────────────────────
3단계  올리기
────────────────────────────────────────
(1) mp3 네 개를 인터넷 아카이브(archive.org)에 올립니다.
    항목 이름 예: urantia-devotion-2026-08-16-night

(2) content.py 의 AUDIO_BASE 에 내려받기 주소를 넣고
    python build_index.py 를 다시 실행합니다.

    AUDIO_BASE = "https://archive.org/download/urantia-devotion-2026-08-16-night/"

    이렇게 하면 소리는 아카이브에서 나오고 깃허브에는 mp3가 올라가지 않습니다.

(3) 이 폴더에서 mp3 를 뺀 나머지를 PC 의 devotion 폴더 안에
    2026-08-16-night 라는 이름으로 넣고, 깃허브 데스크탑으로 커밋·푸시합니다.

    주소: https://urantiareaders.com/devotion/2026-08-16-night/

(4) devotion/index.html 의 DAYS 배열에 오늘 날짜를 한 줄 더합니다.

────────────────────────────────────────
파일 안내
────────────────────────────────────────
content.py                본문·강론·가사·기도 (여기만 고치면 됩니다)
generate_audio_daily.py   소리 만들기
build_index.py            index.html 다시 만들기
index.html                묵상 앱 (이미 만들어져 있습니다)
lyrics.txt                SUNO 에 붙여 넣을 가사
audio/                    소리 파일 자리

깃허브에 올릴 때 generate_audio_daily.py 는 빼십시오.
그 안에 API 열쇠가 들어 있습니다.

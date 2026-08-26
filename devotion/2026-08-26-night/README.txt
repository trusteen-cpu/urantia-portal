오늘의 취침 묵상  2026-08-26  아버지의 모습을 바라보다
유란시아서 2:0.1

── 깃허브에 넣는 방법 ───────────────────────────────

1) 이 폴더 전체를 아래 위치에 복사합니다.

   C:\Users\trust\OneDrive\문서\GitHub\urantia-portal\devotion\2026-08-26-night\

2) 이미 R2에는 아래 4개 MP3가 올라가 있으므로 다시 올릴 필요가 없습니다.

   https://audio.urantiareaders.com/devotion/2026-08-26-night/
   - 01_reading.mp3
   - 02_sermon.mp3
   - 03_song.mp3
   - 04_prayer.mp3

3) GitHub Desktop에서 urantia-portal 저장소의 변경사항을 확인하고
   커밋 메시지 예:
      묵상 2026-08-26 취침
   로 커밋한 뒤 Push 합니다.

4) 묵상 목록 페이지에도 오늘 항목을 추가해야 합니다.
   devotion/index.html 의 var DAYS = [ 바로 아래에 아래 두 줄을 추가하세요.

   { folder: "2026-08-26-night", kind: "취침", date: "2026년 8월 26일",
     title: "아버지의 모습을 바라보다", source: "제2편 하나님의 본성 › 서문", verse: "2:0.1" },

5) 배포 후 주소:
   https://urantiareaders.com/devotion/2026-08-26-night/

── 참고 ──────────────────────────────────────

· 페이지는 build_index.py + content.py 구조로 만들었습니다.
· 낭독 → 강론 → 노래 → 기도 자동재생
· 건너뛰기 / 이전 / 전체 반복 / 이 메뉴 반복 / 반복 없음 지원
· 오디오 주소는 R2의 audio.urantiareaders.com 을 사용합니다.
· generate_audio_daily.py 는 다음 회차 재사용을 위해 포함했습니다.

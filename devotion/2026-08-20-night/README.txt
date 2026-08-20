오늘의 묵상  2026-08-20  갈등 속에서 태어나는 것
유란시아서 100:4.1

── 배포 3단계 ────────────────────────────────

1) 음성 만들기
   이 폴더에서 파워셸을 열고 두 줄:

       pip install requests
       python generate_audio_daily.py

   → audio/01_reading.mp3, 02_sermon.mp3, 04_prayer.mp3 가 생깁니다.
   (처음 한 번만 일레븐랩스 키를 물어봅니다. eleven_key.txt 에 저장되며
    이 파일은 절대 깃허브에 올리지 마세요.)

2) 노래 넣기
   lyrics.txt 를 통째로 복사해 Suno 에 붙여 곡을 만든 뒤,
   내려받은 mp3 를 audio/03_song.mp3 로 저장합니다.

3) 올리기
   publish_r2.py 를 실행해 mp3 를 R2 에 올리고,
   mp3 를 뺀 나머지 파일을

       E:\OneDrive\문서\GitHub\urantia-portal\devotion\2026-08-20-night\

   에 복사한 뒤 깃허브 데스크탑에서 커밋·푸시합니다.

   주소: https://urantiareaders.com/devotion/2026-08-20-night/

── 참고 ──────────────────────────────────────

· 원고를 고치려면 content.py 만 고치고  python build_index.py  를 다시 실행.
· 이미 만들어진 mp3 는 다시 만들지 않습니다(지우고 실행하면 새로 만듭니다).
· 목록 페이지(devotion/index.html)의 DAYS 맨 위에 이 회차를 넣어야
  홈페이지 목록에 뜹니다.

오늘의 취침 묵상 2026-08-15 — 환멸 너머의 사랑
유란시아서 83:8.6 (제83편 결혼 제도 · 결혼의 이상화)

배포 3단계
  1. 이 폴더에서 python generate_audio_daily.py 실행
     → audio/01_reading.mp3, 02_sermon.mp3, 04_prayer.mp3 생성
  2. SUNO 에서 「환멸 너머의 사랑」 곡 생성 후 audio/03_song.mp3 로 저장
     (가사와 스타일은 lyrics.txt 에 있습니다)
  3. PC 의 devotion 폴더 안에 이 폴더를 넣고,
     깃허브 데스크탑으로 devotion 폴더째 커밋 → Push origin
     → 1~2분 뒤 https://urantiareaders.com/devotion/2026-08-15-night/ 에서 열립니다
     devotion/index.html 목록에도 이 강의 한 줄을 추가해 주세요.

주의
  - generate_audio_daily.py 에는 API 키가 들어 있습니다.
    남에게 폴더를 통째로 줄 때는 이 파일을 빼고 주세요.
  - 이미 있는 mp3 는 다시 만들지 않습니다. 새로 만들려면 그 파일을 지우세요.
  - content.py 를 고친 뒤에는 python build_index.py 를 실행해 index.html 을 다시 만드세요.

파일
  content.py               본문·강론·가사·기도
  generate_audio_daily.py  음성 생성
  build_index.py           index.html 생성기
  index.html               플레이어
  lyrics.txt               SUNO 붙여넣기용 가사

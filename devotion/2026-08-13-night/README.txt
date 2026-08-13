오늘의 취침 묵상 2026-08-13 — 미미한 불꽃에도
유란시아서 155:6.17 (제155편 북부 갈릴리를 통해 피신 · 종교에 대한 두 번째 설교)

배포 3단계
  1. 이 폴더에서 python generate_audio_daily.py 실행
     → audio/01_reading.mp3, 02_sermon.mp3, 04_prayer.mp3 생성
  2. SUNO 에서 「미미한 불꽃에도」 곡 생성 후 audio/03_song.mp3 로 저장
     (가사와 스타일은 lyrics.txt 에 있습니다)
  3. PC 의 devotion 폴더 안에 이 폴더를 넣고,
     깃허브 저장소에서 Add file → Upload files 로 devotion 폴더째 올리기
     → 1~2분 뒤 .../devotion/2026-08-13-night/ 에서 열립니다

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

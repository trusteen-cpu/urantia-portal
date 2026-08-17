오늘의 취침 묵상 2026-07-29 — 둘씩 보내신 사랑 (유란시아서 193:3.2)

[배포 3단계]
1. 이 폴더에서  python generate_audio_daily.py  실행
   -> audio/01_reading.mp3, 02_sermon.mp3, 04_prayer.mp3 생성
   (이미 있는 파일은 다시 만들지 않습니다 = 재과금 없음)
2. SUNO 에서 lyrics.txt 의 「둘씩 보내신 사랑」 곡을 만든 뒤
   audio/03_song.mp3 로 저장
3. 2026-07-29-night 폴더째 Netlify 에 드래그 앤 드롭

[주의]
* generate_audio_daily.py 에는 API 키가 들어 있습니다.
  Netlify 에 올릴 때는 이 파일(과 content.py, build_index.py)을 빼고
  index.html + audio 폴더만 올리셔도 됩니다.

[원고를 고쳤을 때]
  content.py 를 고친 뒤  python build_index.py  를 실행하면
  index.html 화면 글도 같이 바뀝니다.

[재생기 사용법]
  화면을 누르면 낭독 → 강론 → 노래 → 기도 순으로 자동 재생되고
  '전체 무한 연속'이 켜진 채 시작됩니다.
  ↻ 버튼 : 반복 없음 → 전체 무한 → 한 메뉴만 무한(배지 1)
  ⏮ ⏭ : 건너뛰기 (재생 3초 뒤 ⏮ 는 처음으로)
  위쪽 낭독/강론/노래/기도 단추로 바로 이동
  스페이스 = 재생/정지,  ← → = 건너뛰기
  audio/03_song.mp3 가 없으면 안내 후 자동으로 기도로 넘어갑니다.

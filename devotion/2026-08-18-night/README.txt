오늘의 취침 묵상 2026-08-18 「이웃의 등불에서도」 (유란시아서 92:7.3)

[1단계] 음성 만들기
  폴더에서 파워셸을 열고 아래 두 줄을 차례로 붙여넣으세요.

      pip install requests
      python generate_audio_daily.py

  audio 폴더에 01_reading.mp3, 02_sermon.mp3, 04_prayer.mp3 가 생깁니다.
  일레븐랩스 API 키는 처음 한 번만 물어보고 eleven_key.txt 에 저장됩니다.
  (eleven_key.txt 는 깃허브에 올리지 마세요)

[2단계] 노래
  lyrics.txt 의 가사를 Suno에 붙여넣어 곡을 만든 뒤,
  받은 파일을 audio 폴더에 03_song.mp3 라는 이름으로 저장하세요.

[3단계] 올리기
  1) publish_r2.py 를 실행해 mp3 4개를 R2에 올립니다.
     (index.html 은 이미 R2 주소를 갖고 있어 고칠 것이 없습니다)
  2) 이 폴더에서 audio 폴더와 generate_audio_daily.py, eleven_key.txt 를 뺀
     나머지를 저장소의 devotion/2026-08-18-night/ 로 복사합니다.
     저장소 위치: E:\OneDrive\문서\GitHub\urantia-portal
  3) 깃허브 데스크탑에서 커밋하고 푸시합니다.

  최종 주소: https://urantiareaders.com/devotion/2026-08-18-night/

  devotion/index.html 의 DAYS 목록에 아래 한 줄을 맨 위에 넣어야 목록에 보입니다.
  { folder:"2026-08-18-night", kind:"취침", date:"2026년 8월 18일",
    title:"이웃의 등불에서도", source:"제92편 종교의 후대 진화",
    verse:"92:7.3" },
  직접 고치기 번거로우시면 index.html 을 보내 주세요. 제가 넣어 드리겠습니다.

오늘 업데이트 파일

1) generate_audio_daily.py
   기존 devotion/generate_audio_daily.py와 교체 후:
   python generate_audio_daily.py

2) 생성 결과는 기존 코드 기준 site/audio/에 날짜 접두사(20260826_)가 붙습니다.
   현재 코드는 archive.org용으로 작성되어 있습니다. R2용 업로드 코드는 아직 연결되어 있지 않습니다.

3) Suno:
   suno_lyrics_2026-08-26.txt를 복사해 곡 생성 후 03_song.mp3에 해당하는 파일을 준비합니다.

4) index.html
   오늘 2026-08-26-night 항목을 목록 맨 위에 추가한 버전입니다.

중요:
기존 generate_audio_daily.py 안에 ElevenLabs API 키가 코드 기본값으로 노출되어 있었습니다.
안전을 위해 해당 키를 폐기/재발급하고 환경변수 ELEVENLABS_API_KEY만 사용하도록 바꾸는 것을 권장합니다.

실행 방법

1. 이 폴더에서:
   python -m pip install edge-tts

2. 실행:
   python generate_audio_daily.py

3. 생성:
   audio/01_reading.mp3
   audio/02_sermon.mp3
   audio/04_prayer.mp3

4. Suno에서 노래 생성 후:
   audio/03_song.mp3

참고:
- ELEVENLABS_API_KEY가 정상 설정되어 있으면 ElevenLabs를 먼저 사용합니다.
- 키가 없거나 401 오류가 나면 Edge TTS로 자동 전환합니다.
- 코드 안에는 API 키를 넣지 않았습니다.

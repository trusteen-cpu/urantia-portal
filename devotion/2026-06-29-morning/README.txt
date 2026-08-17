오늘의 묵상 · 2026-06-29 · 모론시아로 가는 문 (유란시아서 47:10)
================================================================

구성 (순서: 낭독 → 강론 → 노래 → 기도)
- index.html              : 묵상 페이지. 본문 47:10.1~47:10.7 전체 표시,
                            오디오 낭독은 47:10.7절만. 낭독-강론-노래-기도 순차 재생.
- content.py              : 본문/낭독/강론/노래 가사/기도 원문
- generate_audio_daily.py : ElevenLabs 음성 생성 (한국어 voice ZNSVYmudV9pOqphY0x8C,
                            model eleven_multilingual_v2, 이미 있으면 건너뜀)
- audio/                  : 생성될 음성 폴더
    audio/01_reading.mp3  낭독 (47:10.7절만)
    audio/02_sermon.mp3   강론
    audio/03_prayer.mp3   기도
- song.mp3                : 노래 — Mureka로 만들어 이 폴더에 직접 넣어 주세요 (제목: 유리 바다를 건너)

진행 순서
1) python3 generate_audio_daily.py   (낭독·강론·기도 음성 생성)
2) Mureka로 만든 song.mp3 를 이 폴더에 추가
3) 이 폴더(오늘의묵상_0629_모론시아의문)를 통째로 Netlify에 새로 배포

※ generate_audio_daily.py 상단 API_KEY를 기존에 쓰시던 ElevenLabs 키로 확인해 주세요
   (환경변수 ELEVENLABS_API_KEY 사용 가능).

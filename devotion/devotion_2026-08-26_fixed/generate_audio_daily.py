#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-08-26 취침 묵상 MP3 생성기
- 기본: ElevenLabs (ELEVENLABS_API_KEY 환경변수)
- 키가 없거나 401이면 Edge TTS로 자동 대체
- 출력:
  audio/01_reading.mp3
  audio/02_sermon.mp3
  audio/04_prayer.mp3
"""

import os
import re
import json
import asyncio
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

DATE = "2026-08-26"
REFERENCE = "2:0.1"

READING = (
    "근원적이고 무한한 인격에 대한 인간의 사유와 이상 속에는 하나님에 대한 가장 고귀한 개념이 포함되어 있으므로, "
    "신의 품성을 이루는 신성한 본성의 몇 가지 특성을 탐구하는 일은 가능할 뿐 아니라 유익하다. "
    "하나님의 본성은 네바돈의 미가엘이 다방면의 가르침과 육체로서 살아낸 그 탁월한 필사 생애 속에서 계시한 "
    "아버지의 모습에서 가장 잘 이해될 수 있다. "
    "신성한 본성은 또한 인간이 자신을 하나님의 자녀로 인식하고 파라다이스 창조주를 진정한 영적 아버지로 바라볼 때 "
    "더 잘 이해될 수 있다."
)

SERMON = (
    "오늘 말씀은 하나님을 멀리 있는 추상적 존재로 생각하지 말고, 우리를 사랑으로 품으시는 인격적 아버지로 바라보라고 초대합니다. "
    "인간의 생각이 아무리 높아져도 무한하신 하나님을 모두 담을 수는 없지만, 우리가 품을 수 있는 가장 고귀한 진리와 선함과 사랑의 이상 속에서 하나님을 향한 길은 열려 있습니다. "
    "그리고 그 길을 가장 분명하게 보여 준 분이 네바돈의 미가엘, 곧 예수의 생애입니다. "
    "예수는 하나님을 말로만 설명하지 않고 사람을 대하는 태도와 용서, 자비, 용기, 섬김과 진실함을 통해 아버지의 성품을 삶으로 보여 주었습니다. "
    "그러므로 하나님을 알고 싶다면 예수의 삶을 바라보는 동시에 내가 하나님의 자녀라는 사실을 마음 깊이 받아들여야 합니다. "
    "하나님을 두려움의 통치자가 아니라 영적 아버지로 인식할 때 신앙은 의무에서 관계로, 불안에서 신뢰로, 자기중심에서 사랑과 봉사로 옮겨 갑니다. "
    "오늘 하루를 돌아보며 나는 하나님을 어떤 분으로 생각하며 살았는지, 그리고 그 아버지의 성품을 내 말과 행동 속에 얼마나 드러냈는지 조용히 살펴봅시다."
)

PRAYER = (
    "사랑이 충만하신 삼위일체 하나님, 오늘도 저희를 자녀로 품어 주시고 아버지의 성품을 더 깊이 알게 하시니 감사합니다. "
    "예수의 삶 속에 나타난 사랑과 자비와 진실을 바라보며, 하나님을 두려움이 아니라 신뢰와 사랑으로 대하게 하소서. "
    "저희 마음속의 좁은 생각과 왜곡된 하나님 이미지를 바로잡아 주시고, 매일의 말과 행동 속에서 아버지의 친절과 용서와 섬김을 드러내게 하소서. "
    "오늘 부족했던 일들을 돌아보며 고칠 것은 고치게 하시고, 받은 사랑을 내일 만나는 사람들에게 나누게 하소서. "
    "잠드는 이 밤 저희의 생각과 마음을 평안으로 지켜 주시며, 내일도 하나님의 자녀답게 진리와 사랑의 길을 걷게 하소서. "
    "예수의 이름으로 기도드립니다. 아멘."
)

_ONES = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
_UNITS = [(1000, "천"), (100, "백"), (10, "십")]

def sino_kr(n: int) -> str:
    if n == 0:
        return "영"
    out = ""
    rest = n
    for value, name in _UNITS:
        q, rest = divmod(rest, value)
        if q:
            out += ("" if q == 1 else _ONES[q]) + name
    if rest:
        out += _ONES[rest]
    return out

def spoken_reference(ref: str) -> str:
    m = re.fullmatch(r"\s*(\d+):(\d+)\.(\d+)\s*", ref)
    if m:
        p, c, v = map(int, m.groups())
        return f"{sino_kr(p)}편 {sino_kr(c)}장 {sino_kr(v)}절"
    return ref

def elevenlabs_tts(text: str, out_path: Path) -> bool:
    api_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not api_key:
        return False

    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "ZNSVYmudV9pOqphY0x8C")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.62,
            "similarity_boost": 0.80,
            "style": 0.15,
            "use_speaker_boost": True,
            "speed": 0.92
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=payload, method="POST",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as res:
            out_path.write_bytes(res.read())
        return True
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")
        print(f"  ElevenLabs 실패 HTTP {e.code}: {detail[:180]}")
        return False
    except Exception as e:
        print(f"  ElevenLabs 실패: {e}")
        return False

async def edge_tts_save(text: str, out_path: Path):
    try:
        import edge_tts
    except ImportError:
        raise SystemExit(
            "\nedge-tts가 설치되어 있지 않습니다.\n"
            "먼저 실행하세요:\n"
            "  python -m pip install edge-tts\n"
        )
    voice = os.environ.get("EDGE_TTS_VOICE", "ko-KR-SunHiNeural")
    communicate = edge_tts.Communicate(
        text=text, voice=voice, rate="-8%", volume="+0%", pitch="-2Hz"
    )
    await communicate.save(str(out_path))

async def make_track(label: str, text: str, filename: str):
    out = AUDIO_DIR / filename
    print(f"▸ {label} 생성 중...")
    if elevenlabs_tts(text, out):
        print(f"  ✓ {label} → {out}")
        return
    print("  → ElevenLabs 키 없음/실패. Edge TTS로 생성합니다.")
    await edge_tts_save(text, out)
    print(f"  ✓ {label} → {out}")

async def main():
    print("────────────────────────────────────────────")
    print(f"오늘의 취침 묵상 {DATE} / {REFERENCE}")
    print(f"낭독 표기: {spoken_reference(REFERENCE)}")
    print(f"강론 {len(SERMON)}자 · 기도 {len(PRAYER)}자")
    print("────────────────────────────────────────────")

    reading_tts = f"{spoken_reference(REFERENCE)}. {READING}"

    await make_track("낭독", reading_tts, "01_reading.mp3")
    await make_track("강론", SERMON, "02_sermon.mp3")
    await make_track("기도", PRAYER, "04_prayer.mp3")

    print("────────────────────────────────────────────")
    print("완료")
    print("Suno에서 곡을 만든 뒤 아래 이름으로 저장하세요:")
    print("  audio/03_song.mp3")
    print("────────────────────────────────────────────")

if __name__ == "__main__":
    asyncio.run(main())

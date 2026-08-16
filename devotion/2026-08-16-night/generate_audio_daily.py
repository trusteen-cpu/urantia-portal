# -*- coding: utf-8 -*-
"""
오늘의 취침 묵상 2026-08-16 (유란시아서 149:6.4) — 음성 생성

준비 (처음 한 번만)
    pip install requests

실행
    python generate_audio_daily.py

만들어지는 것
    audio/01_reading.mp3   낭독
    audio/02_sermon.mp3    강론
    audio/04_prayer.mp3    기도

노래(audio/03_song.mp3)는 SUNO에서 만들어 직접 넣으십시오.
이미 있는 mp3는 건너뜁니다(다시 만들려면 그 파일을 지우고 실행).
"""

import os
import re
import sys
import time

try:
    import requests
except ImportError:
    print("requests 가 없습니다.  먼저 이것을 실행하세요:  pip install requests")
    sys.exit(1)

import content as C

# ── 설정 ──────────────────────────────────────────────────
API_KEY = "sk_1fead37308afe2bfa470da53024abec6d0467425d31071e2"
VOICE_ID = "ZNSVYmudV9pOqphY0x8C"
MODEL_ID = "eleven_multilingual_v2"

OUT_DIR = "audio"
SETTINGS = {
    "stability": 0.45,
    "similarity_boost": 0.80,
    "style": 0.30,
    "use_speaker_boost": True,
}

# ── 편장절을 한국어로 읽기 ─────────────────────────────────
_ONES = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]


def sino(n):
    """숫자를 한국어 한자음으로. 149 → 백사십구"""
    n = int(n)
    if n == 0:
        return "영"
    out = ""
    if n >= 100:
        h = n // 100
        out += ("" if h == 1 else _ONES[h]) + "백"
        n %= 100
    if n >= 10:
        t = n // 10
        out += ("" if t == 1 else _ONES[t]) + "십"
        n %= 10
    if n:
        out += _ONES[n]
    return out


def read_one_citation(paper, chap, verse):
    head = "머리말" if int(paper) == 0 else sino(paper) + "편"
    return "%s %s장 %s절" % (head, sino(chap), sino(verse))


def read_citation(cit):
    """149:6.4 → 백사십구편 육장 사절
       149:6.4-6.6 → 백사십구편 육장 사절부터 육절까지
       0:8.9 → 머리말 팔장 구절"""
    cit = cit.strip()
    m = re.match(r"^(\d+):(\d+)\.(\d+)\s*[-~]\s*(?:(\d+)\.)?(\d+)$", cit)
    if m:
        paper, chap, v1, chap2, v2 = m.groups()
        base = read_one_citation(paper, chap, v1)
        if chap2 and chap2 != chap:
            return base + "부터 " + sino(chap2) + "장 " + sino(v2) + "절까지"
        return base + "부터 " + sino(v2) + "절까지"
    m = re.match(r"^(\d+):(\d+)\.(\d+)$", cit)
    if m:
        return read_one_citation(*m.groups())
    return cit


# ── 음성 원고 다듬기 ───────────────────────────────────────
def to_speech(text):
    """따옴표·줄표처럼 읽으면 어색한 기호를 정리"""
    t = text
    t = t.replace("“", "").replace("”", "").replace("‘", "").replace("’", "")
    t = t.replace('"', "").replace("—", ", ").replace("–", ", ")
    t = re.sub(r"\n{2,}", "\n\n", t)
    return t.strip()


def speech_of(key):
    if key == "01_reading":
        return read_citation(C.CITATION) + ".\n\n" + to_speech(C.READING)
    if key == "02_sermon":
        return to_speech(C.SERMON)
    if key == "04_prayer":
        return to_speech(C.PRAYER)
    return None


# ── 생성 ──────────────────────────────────────────────────
def tts(text, path):
    url = "https://api.elevenlabs.io/v1/text-to-speech/%s" % VOICE_ID
    r = requests.post(
        url,
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json={"text": text, "model_id": MODEL_ID, "voice_settings": SETTINGS},
        timeout=300,
    )
    if r.status_code != 200:
        print("  실패 %s — %s" % (r.status_code, r.text[:300]))
        return False
    with open(path, "wb") as f:
        f.write(r.content)
    return True


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("오늘의 %s 묵상 %s — 유란시아서 %s" % (C.KIND, C.DATE, C.CITATION))
    print("낭독 첫머리: %s\n" % read_citation(C.CITATION))

    for key, label, _ in C.SEGMENTS:
        path = os.path.join(OUT_DIR, key + ".mp3")
        if key == "03_song":
            if os.path.exists(path):
                print("[노래] 이미 있습니다 — 건너뜁니다")
            else:
                print("[노래] SUNO에서 만들어 %s 로 넣으십시오" % path)
            continue
        if os.path.exists(path):
            print("[%s] 이미 있습니다 — 건너뜁니다" % label)
            continue
        text = speech_of(key)
        print("[%s] 만드는 중... (%d자)" % (label, len(text)))
        if tts(text, path):
            print("  완료 → %s" % path)
        time.sleep(1)

    print("\n끝났습니다. audio 폴더를 확인하십시오.")


if __name__ == "__main__":
    main()

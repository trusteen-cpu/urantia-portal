# -*- coding: utf-8 -*-
"""
오늘의 취침 묵상 2026-08-15 — 환멸 너머의 사랑 (유란시아서 83:8.6)

폴더 안에서 실행하세요.
    python generate_audio_daily.py

만들어지는 파일
    audio/01_reading.mp3   낭독 (편장절 + 본문)
    audio/02_sermon.mp3    강론
    audio/04_prayer.mp3    기도

노래(audio/03_song.mp3)는 SUNO에서 만들어 직접 넣으세요.
이미 있는 mp3는 건너뜁니다(재과금 방지). 다시 만들려면 그 파일을 지우세요.
"""

import os
import re
import sys
import json
import urllib.request

import content as C

# ── 설정 ────────────────────────────────────────────────
API_KEY = "sk_1fead37308afe2bfa470da53024abec6d0467425d31071e2"
VOICE_ID = "ZNSVYmudV9pOqphY0x8C"
MODEL_ID = "eleven_multilingual_v2"

OUT_DIR = "audio"

# ── 편장절 사이노 낭독 ──────────────────────────────────
_ONES = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]


def sino(n):
    """숫자를 한국어 한자음으로. 예) 83 → 팔십삼"""
    n = int(n)
    if n == 0:
        return "영"
    out = ""
    hundreds, rest = divmod(n, 100)
    if hundreds:
        out += ("" if hundreds == 1 else _ONES[hundreds]) + "백"
    tens, ones = divmod(rest, 10)
    if tens:
        out += ("" if tens == 1 else _ONES[tens]) + "십"
    if ones:
        out += _ONES[ones]
    return out


def read_one_citation(cit):
    """83:8.6 → 팔십삼편 팔장 육절 / 0:8.9 → 머리말 팔장 구절"""
    m = re.match(r"^\s*(\d+):(\d+)\.(\d+)\s*$", cit)
    if not m:
        return cit
    paper, sec, par = m.group(1), m.group(2), m.group(3)
    head = "머리말" if int(paper) == 0 else sino(paper) + "편"
    return "%s %s장 %s절" % (head, sino(sec), sino(par))


def read_citation(cit):
    """단일 절과 범위(83:8.6-8.8) 모두 처리"""
    m = re.match(r"^\s*(\d+):(\d+)\.(\d+)\s*-\s*(?:(\d+)\.)?(\d+)\s*$", cit)
    if m:
        paper, sec, par1, sec2, par2 = m.groups()
        head = "머리말" if int(paper) == 0 else sino(paper) + "편"
        if sec2 and sec2 != sec:
            return "%s %s장 %s절부터 %s장 %s절까지" % (
                head, sino(sec), sino(par1), sino(sec2), sino(par2))
        return "%s %s장 %s절부터 %s절까지" % (head, sino(sec), sino(par1), sino(par2))
    return read_one_citation(cit)


# ── TTS 원고 다듬기 ─────────────────────────────────────
def clean(text):
    """음성 원고에서 따옴표를 없애고 줄표를 쉼표로 바꿉니다."""
    t = text.replace("\n\n", "\n")
    for q in ["“", "”", "‘", "’", "\"", "'"]:
        t = t.replace(q, "")
    t = t.replace("—", ", ").replace("–", ", ")
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


SEGMENTS = [
    ("01_reading", read_citation(C.CITATION) + ".\n" + clean(C.READING)),
    ("02_sermon", clean(C.SERMON)),
    ("04_prayer", clean(C.PRAYER)),
]


# ── 일레븐랩스 호출 ─────────────────────────────────────
def tts(text, path):
    url = "https://api.elevenlabs.io/v1/text-to-speech/%s" % VOICE_ID
    body = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.80,
            "style": 0.20,
            "use_speaker_boost": True,
        },
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("xi-api-key", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "audio/mpeg")
    with urllib.request.urlopen(req, timeout=300) as res:
        data = res.read()
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("오늘의 %s 묵상 %s — %s" % (C.KIND, C.DATE, C.TITLE))
    print("본문 %s (%s)" % (C.CITATION, read_citation(C.CITATION)))
    print("-" * 52)

    for name, text in SEGMENTS:
        path = os.path.join(OUT_DIR, name + ".mp3")
        if os.path.exists(path) and os.path.getsize(path) > 0:
            print("건너뜀  %s (이미 있음)" % path)
            continue
        print("만드는 중  %s  (%d자)" % (path, len(text)))
        try:
            size = tts(text, path)
            print("        완료  %.1f KB" % (size / 1024.0))
        except Exception as e:
            print("        실패  %s" % e)
            sys.exit(1)

    song = os.path.join(OUT_DIR, "03_song.mp3")
    print("-" * 52)
    if os.path.exists(song):
        print("노래 파일 있음: %s" % song)
    else:
        print("노래는 SUNO에서 만들어 %s 로 넣어 주세요." % song)
        print("가사는 lyrics.txt 에 있습니다.")
    print("끝났습니다. index.html 을 열어 확인하세요.")


if __name__ == "__main__":
    main()

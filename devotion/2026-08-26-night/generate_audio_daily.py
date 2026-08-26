# -*- coding: utf-8 -*-
"""
오늘의 묵상 음성 만들기 (일레븐랩스)

  audio/01_reading.mp3  낭독
  audio/02_sermon.mp3   강론
  audio/04_prayer.mp3   기도

03_song.mp3 는 Suno 에서 만들어 직접 넣는다.

파워셸에 이 두 줄:
    pip install requests
    python generate_audio_daily.py

키는 파일에 적지 않는다. 처음 실행할 때 한 번 물어보고 eleven_key.txt 에 둔다.
이미 만들어진 mp3 는 건너뛴다(다시 만들려면 그 파일을 지우고 실행).
"""
import os, re, sys, json, time

try:
    import requests
except ImportError:
    print("[오류] requests 가 없습니다.  pip install requests  를 먼저 하세요.")
    sys.exit(1)

import content

VOICE_ID = "ZNSVYmudV9pOqphY0x8C"      # 한국어 목소리
MODEL    = "eleven_multilingual_v2"
KEY_FILE = "eleven_key.txt"
OUT_DIR  = "audio"

# ---------------------------------------------------------------- 편장절 읽기
ONE = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]

def sino(n):
    """숫자를 한자어로: 2→이, 15→십오, 146→백사십육"""
    n = int(n)
    if n == 0:
        return "영"
    out = ""
    for unit, name in ((100, "백"), (10, "십"), (1, "")):
        d = n // unit % 10
        if d:
            out += ("" if d == 1 and unit > 1 else ONE[d]) + name
    return out

def read_one(cit):
    """146:3.1 → 백사십육편 삼장 일절"""
    m = re.match(r"^\s*(\d+):(\d+)\.(\d+)\s*$", cit)
    if not m:
        return cit
    p, s, v = m.groups()
    return "%s편 %s장 %s절" % (sino(p), sino(s), sino(v))

def read_citation(cit):
    """범위도 처리: 151:4.2-4.7 → 백오십일편 사장 이절부터 칠절까지"""
    m = re.match(r"^\s*(\d+):(\d+)\.(\d+)\s*[-~]\s*(?:(\d+)\.)?(\d+)\s*$", cit)
    if m:
        p, s, v1, s2, v2 = m.groups()
        head = "%s편 %s장 %s절부터" % (sino(p), sino(s), sino(v1))
        if s2 and s2 != s:
            return head + " %s장 %s절까지" % (sino(s2), sino(v2))
        return head + " %s절까지" % sino(v2)
    return read_one(cit)

# ---------------------------------------------------------------- 원고 만들기
def reading_script():
    parts = []
    if content.READING:
        parts.append(read_citation(content.READING[0][0]))
    for _, text in content.READING:
        parts.append(text)
    return "\n".join(parts)

def plain(t):
    return re.sub(r"\n{2,}", "\n", t).strip()

SEGMENTS = [
    ("01_reading", reading_script()),
    ("02_sermon",  plain(content.SERMON)),
    ("04_prayer",  plain(content.PRAYER)),
]

# ---------------------------------------------------------------- 만들기
def tidy_key(k):
    """공백·줄바꿈을 없애고, 두 번 붙여 넣은 키는 앞의 하나만 남긴다."""
    k = re.sub(r"\s+", "", k or "")
    if k.count("sk_") > 1:                       # sk_xxxx sk_xxxx 처럼 겹쳐 들어온 경우
        k = "sk_" + k.split("sk_")[1]
        print("  [알림] 키가 두 번 붙어 있어 앞의 하나만 씁니다.")
    return k

def get_key():
    if os.path.exists(KEY_FILE):
        k = tidy_key(open(KEY_FILE, encoding="utf-8").read())
        if k:
            return k
    k = tidy_key(input("일레븐랩스 API 키를 붙여 넣고 엔터: "))
    open(KEY_FILE, "w", encoding="utf-8").write(k)
    print("키를 %s 에 저장했습니다. 이 파일은 깃허브에 올리지 마세요." % KEY_FILE)
    return k

def make(key, name, text, tries=4):
    path = os.path.join(OUT_DIR, name + ".mp3")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print("  건너뜀 (이미 있음): %s" % path)
        return
    for n in range(1, tries + 1):
        try:
            r = requests.post(
                "https://api.elevenlabs.io/v1/text-to-speech/" + VOICE_ID,
                headers={"xi-api-key": key, "Content-Type": "application/json"},
                json={"text": text, "model_id": MODEL,
                      "voice_settings": {"stability": 0.45, "similarity_boost": 0.8,
                                         "style": 0.15, "use_speaker_boost": True}},
                timeout=300,
            )
        except requests.exceptions.SSLError:
            print("  [연결 끊김] %d/%d - 20초 뒤 다시 시도합니다." % (n, tries))
            if n == tries:
                print("     계속 끊기면 백신·방화벽의 '보안 접속 검사(HTTPS 검사)'를 잠시 끄고")
                print("     다시 해 보세요. 회사·학교 인터넷이면 그쪽 차단일 수 있습니다.")
                return
            time.sleep(20); continue
        except requests.exceptions.RequestException as e:
            print("  [연결 문제] %d/%d  %s" % (n, tries, type(e).__name__))
            if n == tries:
                return
            time.sleep(20); continue

        if r.status_code == 401:
            print("  [실패] 키가 맞지 않습니다. %s 를 지우고 다시 실행하세요." % KEY_FILE)
            return
        if r.status_code != 200:
            print("  [실패] %s  %s  %s" % (name, r.status_code, r.text[:200]))
            if n == tries:
                return
            time.sleep(10); continue

        open(path, "wb").write(r.content)
        print("  만듦: %s  (%.1f MB)" % (path, len(r.content) / 1048576.0))
        return

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("=== 오늘의 묵상 음성 만들기 ===")
    print("%s  %s" % (content.DATE, content.TITLE))
    key = get_key()
    for name, text in SEGMENTS:
        print("- %s  (%d자)" % (name, len(text)))
        make(key, name, text)
    print()
    print("끝났습니다. 노래는 Suno 에서 만들어 audio/03_song.mp3 로 넣으세요.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_audio_daily.py
오늘의 묵상 — 낭독 / 강론 / 기도 MP3 생성기 (ElevenLabs multilingual v2)

하루에 한 편만 유지합니다. 매일 아래 CONTENT 블록만 바꾸고 다시 실행하면
같은 파일들이 그날 것으로 덮어써집니다.

실행:  python generate_audio_daily.py
결과:  site/audio/01_reading.mp3
       site/audio/02_sermon.mp3
       site/audio/04_prayer.mp3
       site/content.js   (플레이어가 읽는 본문 데이터 자동 갱신)

※ 03_song.mp3 는 Suno에서 생성해 site/audio/ 에 직접 넣으십시오.
※ 보안: 이 파일은 site/ 폴더 밖에 두십시오. 깃허브에 올릴 때는 .gitignore 에 추가하거나
   API 키를 환경변수로만 사용하십시오.  (export ELEVENLABS_API_KEY="...")
"""

import os
import re
import sys
import json
import datetime
import urllib.request
import urllib.error
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# 1. 설정
# ─────────────────────────────────────────────────────────────
API_KEY = os.environ.get(
    "ELEVENLABS_API_KEY",
    "sk_1fead37308afe2bfa470da53024abec6d0467425d31071e2",
)
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "ZNSVYmudV9pOqphY0x8C")
MODEL_ID = "eleven_multilingual_v2"

BASE_DIR = Path(__file__).resolve().parent
SITE_DIR = BASE_DIR / "site"
AUDIO_DIR = SITE_DIR / "audio"

# ── mp3 호스팅 ────────────────────────────────────────────────
# 인터넷 아카이브 식별자(identifier)를 넣으면 mp3는 아카이브에서 재생됩니다.
# 깃허브에는 index.html 과 content.js 만 올라가므로 저장소가 가벼워집니다.
# 비워 두면("") 같은 폴더의 audio/ 를 그대로 씁니다.
ARCHIVE_ITEM = os.environ.get("ARCHIVE_ITEM", "urantia-devotion-kr")

# 아카이브에 매일 같은 이름으로 덮어쓰면 재처리(derive) 때문에 잠시 재생이 끊깁니다.
# 날짜를 붙여 새 파일로 올리면 그런 일이 없고 지난 날짜도 그대로 남습니다.
DATE_PREFIX = True


def audio_base() -> str:
    return f"https://archive.org/download/{ARCHIVE_ITEM}/" if ARCHIVE_ITEM else "audio/"


def fname(base: str) -> str:
    """'01_reading.mp3' → '20260817_01_reading.mp3'"""
    if ARCHIVE_ITEM and DATE_PREFIX:
        return f"{CONTENT['date'].replace('-', '')}_{base}"
    return base


# 취침 묵상용 음성 설정 — 느리고 안정적인 톤
VOICE_SETTINGS = {
    "stability": 0.62,
    "similarity_boost": 0.80,
    "style": 0.15,
    "use_speaker_boost": True,
    "speed": 0.92,
}

# ─────────────────────────────────────────────────────────────
# 2. 오늘의 본문 (매일 이 블록만 교체하면 됩니다)
# ─────────────────────────────────────────────────────────────
CONTENT = {
    "date": "2026-08-17",   # 비워 두면("") 실행하는 날짜로 자동 설정됩니다
    "reference": "153:3.2",
    "paper_title": "제153편 가버나움에서의 위기",
    "section_title": "후속 모임",
    "theme": "먹을 수 없는 빵, 살아내는 빵",
    "keyword": "체험의 실체",
    "one_line": "하늘의 빵은 삼키는 것이 아니라 하나 되는 것입니다.",

    # ── 낭독 : 본문 구절 전체 ──
    "reading": (
        "방문 중이던 바리새인 중 한 명이 등불 받침대 위로 올라가 소리쳤다: "
        "“당신은 자신이 생명의 빵이라고 말했소. 그렇다면 당신의 살을 우리에게 먹게 하고, "
        "당신의 피를 마시게 할 수 있겠소? 당신의 가르침이 실행될 수 없다면 무슨 소용이 있겠소?” "
        "예수는 이 질문에 답하며 말했다: "
        "“나는 내 살이 생명의 빵이요, 내 피가 그 빵의 물이라고 가르치지 않았다. "
        "그러나 나는 내가 육신 안에서 살아가는 나의 삶이 하늘의 빵을 베푸는 것이라고 말했다. "
        "하나님의 말씀이 육신으로 베풀어지는 사실과 하나님의 뜻에 복종하는 사람의 아들의 현상은, "
        "신성한 양식과 맞먹는 체험의 실체를 이룬다. "
        "너희는 내 살을 먹을 수도, 내 피를 마실 수도 없지만, "
        "너희는 내가 아버지와 영적으로 하나인 것처럼 나와 영적으로 하나가 될 수 있다. "
        "너희는 참으로 생명의 빵이며 필사자의 모습으로 베풀어진 하나님의 영원한 말씀에 의해 양육될 수 있고, "
        "진정한 생명의 물인 신성한 영에 의해 혼이 적셔질 수 있다. "
        "아버지께서 나를 이 세상에 보내신 것은 그가 모든 사람 안에 내주하며 이끌고자 하시는 뜻을 "
        "드러내기 위함이며, 나는 모든 사람이 마찬가지로 내주하시는 하늘 아버지의 뜻을 알고 행하기를 "
        "늘 추구하도록 영감을 주고자, 육신의 이 삶을 그렇게 살았다.”"
    ),

    # ── 강론 : 500~700자 ──
    "sermon": (
        "오늘 밤 예수께서 마주하신 것은 문자만 듣는 귀였습니다. "
        "등불 받침대 위로 올라간 바리새인은 살과 피를 문자 그대로 붙들고 물었습니다. "
        "실행할 수 없는 가르침이라면 무슨 소용이 있느냐고. "
        "예수의 대답은 부드럽지만 단호합니다. "
        "나는 내 살이 생명의 빵이라고 가르치지 않았다. "
        "내가 육신 안에서 살아가는 그 삶이 하늘의 빵을 베푸는 것이다.\n\n"
        "여기에 계시의 핵심이 있습니다. 신성한 양식은 의식도 물질도 아니며 체험의 실체입니다. "
        "하나님의 말씀이 육신으로 베풀어진 사실과, 아버지의 뜻에 복종한 사람의 아들의 삶, "
        "이 둘이 만나는 자리에서 우리는 비로소 먹고 마십니다. "
        "먹는다는 것은 삼키는 일이 아니라 하나 되는 일입니다.\n\n"
        "오늘 하루 우리는 얼마나 자주 문자에 걸려 넘어졌습니까. "
        "손에 잡히는 것만 실체로 여기지는 않았습니까. "
        "그러나 밤은 다른 감각을 가르칩니다. 눈을 감아야 보이는 것이 있습니다. "
        "진정한 생명의 물인 신성한 영이 지금도 조용히 우리 혼을 적시고 있습니다.\n\n"
        "아버지께서 아들을 보내신 목적은 하나였습니다. "
        "모든 사람 안에 내주하며 이끌고자 하시는 뜻을 드러내는 것. "
        "그 뜻은 지금 당신 안에도 계십니다. 잠들기 전에 조용히 물으십시오. "
        "오늘 나는 내주하시는 아버지의 뜻을 알고 행하기를 추구했는가. "
        "그 물음 자체가 이미 하늘의 빵을 떼어 무는 일입니다. "
        "편히 잠드십시오. 당신을 먹이시는 분이 당신 안에 깨어 계십니다."
    ),

    # ── 기도 본문 : 호칭은 아래 INVOCATIONS 에서 날짜별로 자동 교체 ──
    "prayer_body": (
        "하루의 끝에 서서 당신 앞에 조용히 앉습니다. "
        "오늘도 저는 붙잡을 수 있는 것만 믿으려 했고, 보이는 것만 실체로 여겼습니다. "
        "문자에 걸려 넘어진 저의 좁은 마음을 용서하여 주옵소서. "
        "살과 피가 아니라 삶으로 베풀어지는 하늘의 빵을 이 밤 제게 먹여 주옵소서. "
        "진정한 생명의 물인 당신의 영으로 메마른 제 혼을 적셔 주옵소서. "
        "아들이 아버지와 하나이신 것처럼 저도 그분과 영적으로 하나 되게 하옵소서. "
        "잠든 사이에도 제 안에 내주하시며 저를 이끄시는 당신의 뜻을 알게 하시고, "
        "내일 아침 눈뜰 때 그 뜻을 행하는 사람으로 일어서게 하옵소서. "
        "이 밤 온 세상의 지친 혼들 위에도 당신의 평화를 덮어 주옵소서. "
        "예수의 이름으로 기도드립니다. 아멘."
    ),

    # ── 노래 (Suno) ──
    "song_title": "삼키지 못한 빵",
    "song_style": (
        "Korean sacred lullaby, ambient gospel, 62 BPM, warm female lead vocal, "
        "felt piano, soft strings, brushed cymbals, deep reverb, night air, hymn-like"
    ),
}

# 기도 호칭 14종 — 날짜에 따라 순환
INVOCATIONS = [
    "은혜로우신 하나님 아버지",          # 0
    "사랑이 많으신 하나님 아버지",        # 1
    "삼위일체 하나님",                   # 2
    "만유의 아버지시여",                 # 3
    "빛이시며 생명이신 하나님",           # 4
    "자비가 끝이 없으신 아버지",          # 5
    "진리의 근원이신 하나님",             # 6
    "영원하신 아버지 하나님",             # 7
    "우리 안에 내주하시는 아버지시여",     # 8
    "거룩하신 삼위일체 하나님",           # 9
    "지혜의 근원이신 하나님 아버지",       # 10
    "평화의 하나님 아버지",              # 11
    "창조주 아버지 하나님",              # 12
    "인자하신 아버지 하나님",            # 13
]


def pick_invocation(date_str: str) -> str:
    """날짜(연중 일수) 기준으로 기도 호칭을 순환시킵니다."""
    d = datetime.date.fromisoformat(date_str)
    return INVOCATIONS[d.timetuple().tm_yday % len(INVOCATIONS)]


# ─────────────────────────────────────────────────────────────
# 3. 편·장·절 읽기 변환   (2:7.5 → 이편 칠장 오절)
# ─────────────────────────────────────────────────────────────
_ONES = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
_UNITS = [(1000, "천"), (100, "백"), (10, "십")]


def sino_kr(n: int) -> str:
    """숫자를 한자음 한글로 (153 → 백오십삼)."""
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
    """'153:3.2' → '백오십삼편 삼장 이절'"""
    m = re.fullmatch(r"\s*(\d+):(\d+)\.(\d+)\s*", ref)
    if m:
        p, c, v = (int(x) for x in m.groups())
        return f"{sino_kr(p)}편 {sino_kr(c)}장 {sino_kr(v)}절"
    m = re.fullmatch(r"\s*(\d+):(\d+)\s*", ref)
    if m:
        p, c = (int(x) for x in m.groups())
        return f"{sino_kr(p)}편 {sino_kr(c)}장"
    return ref


def expand_references(text: str) -> str:
    """본문 안에 섞여 있는 모든 편장절 표기를 읽는 방식으로 바꿉니다."""
    text = re.sub(
        r"(\d+):(\d+)\.(\d+)",
        lambda m: f"{sino_kr(int(m.group(1)))}편 {sino_kr(int(m.group(2)))}장 "
                  f"{sino_kr(int(m.group(3)))}절",
        text,
    )
    text = re.sub(
        r"(\d+):(\d+)(?![\d.])",
        lambda m: f"{sino_kr(int(m.group(1)))}편 {sino_kr(int(m.group(2)))}장",
        text,
    )
    return text


# ─────────────────────────────────────────────────────────────
# 4. ElevenLabs 호출
# ─────────────────────────────────────────────────────────────
def synthesize(text: str, out_path: Path, label: str) -> bool:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    payload = json.dumps(
        {
            "text": text,
            "model_id": MODEL_ID,
            "voice_settings": VOICE_SETTINGS,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as res:
            audio = res.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")[:400]
        print(f"  ✕ {label} 실패 (HTTP {e.code})")
        print(f"    {detail}")
        return False
    except Exception as e:  # noqa: BLE001
        print(f"  ✕ {label} 실패: {e}")
        return False

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(audio)
    kb = len(audio) / 1024
    print(f"  ✓ {label} → {out_path.name}  ({kb:,.0f} KB, {len(text):,}자)")
    return True


# ─────────────────────────────────────────────────────────────
# 5. 플레이어용 content.js 생성
# ─────────────────────────────────────────────────────────────
def write_content_js(invocation: str, prayer_full: str) -> None:
    data = {
        "date": CONTENT["date"],
        "reference": CONTENT["reference"],
        "referenceSpoken": spoken_reference(CONTENT["reference"]),
        "paperTitle": CONTENT["paper_title"],
        "sectionTitle": CONTENT["section_title"],
        "theme": CONTENT["theme"],
        "keyword": CONTENT["keyword"],
        "oneLine": CONTENT["one_line"],
        "invocation": invocation,
        # 오디오 위치: 아카이브 식별자가 있으면 아카이브 주소, 없으면 로컬 audio/
        "audioBase": audio_base(),
        "tracks": [
            {
                "id": "reading",
                "label": "낭독",
                "sub": CONTENT["reference"],
                "file": fname("01_reading.mp3"),
                "text": CONTENT["reading"],
            },
            {
                "id": "sermon",
                "label": "강론",
                "sub": CONTENT["theme"],
                "file": fname("02_sermon.mp3"),
                "text": CONTENT["sermon"],
            },
            {
                "id": "song",
                "label": "노래",
                "sub": CONTENT["song_title"],
                "file": fname("03_song.mp3"),
                "text": SONG_DISPLAY,
            },
            {
                "id": "prayer",
                "label": "기도",
                "sub": invocation,
                "file": fname("04_prayer.mp3"),
                "text": prayer_full,
            },
        ],
    }
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    js = "window.MEDITATION = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    (SITE_DIR / "content.js").write_text(js, encoding="utf-8")
    print(f"  ✓ 본문 데이터 → site/content.js")


# 노래 화면 표시용 (지시어 대괄호는 제거된 가사만)
SONG_DISPLAY = """등불 아래 남은 물음 하나
붙잡을 수 없는 것을 붙잡으려 했네
삼키려 한 그 빵은 손에 잡히지 않고
당신은 삶으로 그것을 떼어 주셨네

먹을 수 없는 빵, 마실 수 없는 잔
그러나 하나 될 수 있는 사랑
아버지와 아들이 하나이신 것처럼
이 밤 나도 당신 안에 잠듭니다

생명의 물이 내 혼을 적시고
내주하시는 뜻이 나를 이끄시니
내일 아침 눈을 뜨면
그 뜻을 살아내는 사람 되게 하소서"""


# ─────────────────────────────────────────────────────────────
# 6. 실행
# ─────────────────────────────────────────────────────────────
def main() -> int:
    if not CONTENT.get("date"):
        CONTENT["date"] = datetime.date.today().isoformat()
    date_str = CONTENT["date"]
    invocation = pick_invocation(date_str)
    prayer_full = f"{invocation}, {CONTENT['prayer_body']}"

    print("─" * 58)
    print(f"  오늘의 묵상  {date_str}   {CONTENT['reference']}")
    print(f"  기도 호칭: {invocation}")
    print(f"  강론 {len(CONTENT['sermon']):,}자 · 기도 {len(prayer_full):,}자")
    print("─" * 58)

    if not API_KEY or API_KEY.startswith("여기에"):
        print("  ✕ API 키가 없습니다. ELEVENLABS_API_KEY 환경변수를 설정하십시오.")
        return 1

    reading_tts = (
        f"{spoken_reference(CONTENT['reference'])}.\n\n"
        + expand_references(CONTENT["reading"])
    )
    sermon_tts = expand_references(CONTENT["sermon"])
    prayer_tts = expand_references(prayer_full)

    jobs = [
        (reading_tts, AUDIO_DIR / fname("01_reading.mp3"), "낭독"),
        (sermon_tts, AUDIO_DIR / fname("02_sermon.mp3"), "강론"),
        (prayer_tts, AUDIO_DIR / fname("04_prayer.mp3"), "기도"),
    ]

    ok = 0
    for text, path, label in jobs:
        if synthesize(text, path, label):
            ok += 1

    write_content_js(invocation, prayer_full)

    print("─" * 58)
    print(f"  완료: {ok}/{len(jobs)} 트랙")
    print(f"  노래는 Suno에서 만들어 아래 이름으로 저장하십시오.")
    print(f"    site/audio/{fname('03_song.mp3')}")
    if ARCHIVE_ITEM:
        print()
        print(f"  mp3 4개를 인터넷 아카이브 '{ARCHIVE_ITEM}' 항목에 올리십시오.")
        print(f"    ia upload {ARCHIVE_ITEM} site/audio/{CONTENT['date'].replace('-', '')}_*.mp3")
        print(f"  재생 주소: {audio_base()}")
        print(f"  깃허브에는 site/index.html 과 site/content.js 만 올리면 됩니다.")
    print("─" * 58)
    return 0 if ok == len(jobs) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
set_youtube.py
유튜브에 올린 영상 주소를 홈페이지에 연결합니다.

실행:
    python set_youtube.py https://youtu.be/E4G2Bt3EIQk

주소는 어떤 형태든 됩니다.
    https://youtu.be/아이디
    https://www.youtube.com/watch?v=아이디
    아이디만 적어도 됩니다
"""

import json
import re
import sys
from pathlib import Path

CJS = Path(__file__).resolve().parent / "site" / "content.js"


def extract_id(s: str) -> str:
    s = s.strip()
    m = re.search(r"(?:youtu\.be/|v=|/embed/|/shorts/)([A-Za-z0-9_-]{11})", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    return ""


def main() -> int:
    if len(sys.argv) < 2:
        print("주소를 함께 적어주십시오.")
        print("    python set_youtube.py https://youtu.be/E4G2Bt3EIQk")
        return 1

    vid = extract_id(sys.argv[1])
    if not vid:
        print(f"✕ 주소에서 영상 번호를 찾지 못했습니다: {sys.argv[1]}")
        return 1

    if not CJS.exists():
        print("✕ site/content.js 가 없습니다. 먼저 generate_audio_daily.py 를 실행하십시오.")
        return 1

    raw = CJS.read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";")
    data = json.loads(raw)
    data["youtubeId"] = vid

    if "start" not in data["tracks"][0]:
        print("  ! 구간 시각이 없습니다. make_video.py 를 먼저 실행하시면")
        print("    낭독·강론·노래·기도 건너뛰기가 됩니다. 지금은 영상만 재생됩니다.")

    CJS.write_text(
        "window.MEDITATION = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"  ✓ 연결했습니다: https://youtu.be/{vid}")
    print("  이제 깃허브 데스크탑에서 커밋하고 푸시하시면 홈페이지에 반영됩니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

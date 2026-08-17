#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_video.py
site/audio 의 mp3 네 개와 site/content.js 의 본문으로 유튜브용 MP4를 만듭니다.
가사 비디오처럼 글이 음성에 맞춰 넘어갑니다.

준비(처음 한 번만):
    pip install pillow imageio-ffmpeg mutagen

실행:
    python make_video.py

결과:
    video/20260817_묵상.mp4     ← 유튜브에 올릴 영상
    video/youtube_info.txt      ← 제목·설명·챕터(복사해서 붙여넣기)
"""

import json
import math
import random
import re
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
    import imageio_ffmpeg
    from mutagen.mp3 import MP3
except ImportError:
    print("필요한 것이 없습니다. 아래를 먼저 실행하십시오.")
    print("    pip install pillow imageio-ffmpeg mutagen")
    sys.exit(1)

BASE = Path(__file__).resolve().parent
SITE = BASE / "site"
AUDIO = SITE / "audio"
BUILD = BASE / "build"
OUT = BASE / "video"

W, H = 1920, 1080
FPS = 30

# 색 (플레이어 화면과 같은 밤 색조)
INK = (8, 13, 31)
INK_TOP = (27, 42, 85)
MOON = (242, 235, 218)
LAMP = (232, 169, 78)
WATER = (111, 169, 162)
DIM = (127, 138, 180)
VEIL = (36, 48, 92)

# 한 화면에 넣을 글자 수
CHUNK_MAX = 78
LINE_MAX = 26
MIN_SEC = 2.2


# ─────────────────────────────────────────────────────────────
# 글꼴
# ─────────────────────────────────────────────────────────────
FONT_CANDIDATES = [
    # 윈도우
    "C:/Windows/Fonts/malgunbd.ttf",
    "C:/Windows/Fonts/malgun.ttf",
    "C:/Windows/Fonts/batang.ttc",
    # 맥
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/Library/Fonts/AppleGothic.ttf",
    # 리눅스
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf",
]


def find_font() -> str:
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return p
    print("✕ 한글 글꼴을 찾지 못했습니다. FONT_CANDIDATES 에 글꼴 경로를 넣어주십시오.")
    sys.exit(1)


FONT_PATH = find_font()
_cache: dict = {}


def font(size: int):
    if size not in _cache:
        try:
            _cache[size] = ImageFont.truetype(FONT_PATH, size)
        except OSError:
            _cache[size] = ImageFont.truetype(FONT_PATH, size, index=0)
    return _cache[size]


def text_w(draw, s, f) -> float:
    return draw.textbbox((0, 0), s, font=f)[2]


# ─────────────────────────────────────────────────────────────
# 본문 나누기
# ─────────────────────────────────────────────────────────────
def split_sentences(text: str):
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r'(?<=[.?!”"])\s+', text)
    return [p.strip() for p in parts if p.strip()]


def chunk_text(text: str, is_song: bool = False):
    """화면 하나에 올릴 덩어리로 나눕니다."""
    if is_song:
        blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
        out = []
        for b in blocks:
            lines = [l.strip() for l in b.split("\n") if l.strip()]
            for i in range(0, len(lines), 4):
                out.append("\n".join(lines[i:i + 4]))
        return out or [text]

    out, cur = [], ""
    for s in split_sentences(text):
        if not cur:
            cur = s
        elif len(cur) + len(s) + 1 <= CHUNK_MAX:
            cur += " " + s
        else:
            out.append(cur)
            cur = s
        while len(cur) > CHUNK_MAX * 1.6:          # 아주 긴 문장은 잘라냄
            cut = cur.rfind(" ", 0, CHUNK_MAX)
            cut = cut if cut > 20 else CHUNK_MAX
            out.append(cur[:cut].strip())
            cur = cur[cut:].strip()
    if cur:
        out.append(cur)
    return out


def wrap(draw, text: str, f, max_w: int):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(" "), ""
        for w in words:
            test = (cur + " " + w).strip()
            if text_w(draw, test, f) <= max_w or not cur:
                cur = test
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


# ─────────────────────────────────────────────────────────────
# 배경
# ─────────────────────────────────────────────────────────────
def make_background() -> Image.Image:
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        k = max(0.0, 1 - t * 1.9)
        c = tuple(int(INK[i] + (INK_TOP[i] - INK[i]) * k * 0.55) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)

    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(760, 0, -20):
        a = int(26 * (1 - r / 760) ** 2)
        gd.ellipse([W // 2 - r * 1.5, -r, W // 2 + r * 1.5, r], fill=(a, a + 4, a + 12))
    img = Image.blend(img, Image.blend(img, glow, 0.0), 0)
    d = ImageDraw.Draw(img)

    rnd = random.Random(20260817)
    for _ in range(560):
        x, y = rnd.randint(0, W), rnd.randint(0, int(H * 0.82))
        r = rnd.random() * 1.7 + 0.4
        k = rnd.random() * 0.7 + 0.15
        col = LAMP if rnd.random() > 0.9 else MOON
        c = tuple(int(INK[i] + (col[i] - INK[i]) * k) for i in range(3))
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)
    return img


# ─────────────────────────────────────────────────────────────
# 한 화면 그리기
# ─────────────────────────────────────────────────────────────
def draw_frame(bg, data, ti, track, body, progress):
    img = bg.copy()
    d = ImageDraw.Draw(img)

    f_eyebrow = font(26)
    f_theme = font(40)
    f_label = font(34)
    f_body = font(54)
    f_small = font(24)

    # 머리
    eyebrow = f"오늘의 묵상   {data['date'].replace('-', '.')}"
    d.text((120, 84), eyebrow, font=f_eyebrow, fill=DIM)
    d.text((120, 130), data["theme"], font=f_theme, fill=MOON)
    ref = f"{data['paperTitle']}  ·  {data['reference']}"
    d.text((120, 190), ref, font=f_small, fill=LAMP)

    # 지금 순서
    lab = track["label"]
    lw = text_w(d, lab, f_label)
    d.text((W - 120 - lw, 130), lab, font=f_label, fill=LAMP)
    sw = text_w(d, track["sub"], f_small)
    d.text((W - 120 - sw, 192), track["sub"], font=f_small, fill=DIM)

    # 본문
    lines = wrap(d, body, f_body, W - 460)
    lh = 96
    total = len(lines) * lh
    y = (H - total) // 2 + 20
    for ln in lines:
        w = text_w(d, ln, f_body)
        d.text(((W - w) // 2, y), ln, font=f_body, fill=(228, 222, 206))
        y += lh

    # 아래 진행 막대
    bx0, bx1, by = 220, W - 220, H - 118
    n = len(data["tracks"])
    d.line([(bx0, by), (bx1, by)], fill=VEIL, width=3)
    px = bx0 + (bx1 - bx0) * progress
    d.line([(bx0, by), (px, by)], fill=WATER, width=3)
    for i, t in enumerate(data["tracks"]):
        cx = bx0 + (bx1 - bx0) * ((i + 0.5) / n)
        active = i == ti
        if not active:                      # 지금 순서는 달이 대신 표시합니다
            col = WATER if i < ti else VEIL
            d.ellipse([cx - 6, by - 6, cx + 6, by + 6], fill=col)
        f_st = font(26)
        tw = text_w(d, t["label"], f_st)
        d.text((cx - tw / 2, by + 26), t["label"],
               font=f_st, fill=MOON if active else DIM)
    # 달
    for rr, a in ((26, 0.10), (16, 0.20)):
        c = tuple(int(INK[i] + (MOON[i] - INK[i]) * a) for i in range(3))
        d.ellipse([px - rr, by - rr, px + rr, by + rr], fill=c)
    d.ellipse([px - 8, by - 8, px + 8, by + 8], fill=MOON)
    return img


# ─────────────────────────────────────────────────────────────
def hms(sec: float) -> str:
    sec = int(sec)
    return f"{sec // 60}:{sec % 60:02d}"


def main() -> int:
    cjs = SITE / "content.js"
    if not cjs.exists():
        print("✕ site/content.js 가 없습니다. 먼저 generate_audio_daily.py 를 실행하십시오.")
        return 1
    raw = cjs.read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";")
    data = json.loads(raw)

    # mp3 확인
    paths = []
    for t in data["tracks"]:
        p = AUDIO / t["file"]
        if not p.exists():
            print(f"✕ 없는 파일: site/audio/{t['file']}")
            return 1
        paths.append(p)

    durs = [MP3(str(p)).info.length for p in paths]
    total = sum(durs)
    print(f"  전체 길이 {hms(total)}  (" +
          ", ".join(f"{t['label']} {hms(dd)}" for t, dd in zip(data["tracks"], durs)) + ")")

    BUILD.mkdir(exist_ok=True)
    for old in BUILD.glob("*.png"):
        old.unlink()
    OUT.mkdir(exist_ok=True)

    bg = make_background()
    entries, chapters, clock, idx = [], [], 0.0, 0

    for ti, (track, dur) in enumerate(zip(data["tracks"], durs)):
        chapters.append((clock, track["label"]))
        chunks = chunk_text(track["text"], is_song=(track["id"] == "song"))
        weights = [max(len(c), 12) for c in chunks]
        s = sum(weights)
        secs = [dur * w / s for w in weights]

        # 너무 짧은 화면은 앞뒤로 시간을 나눠 받음
        for i, v in enumerate(secs):
            if v < MIN_SEC and len(secs) > 1:
                need = MIN_SEC - v
                j = max(range(len(secs)), key=lambda k: secs[k])
                if secs[j] - need > MIN_SEC:
                    secs[j] -= need
                    secs[i] = MIN_SEC
        scale = dur / sum(secs)
        secs = [v * scale for v in secs]

        elapsed = 0.0
        for body, sec in zip(chunks, secs):
            prog = (clock + elapsed + sec / 2) / total
            frame = draw_frame(bg, data, ti, track, body, prog)
            fp = BUILD / f"{idx:05d}.png"
            frame.save(fp)
            entries.append((fp, sec))
            elapsed += sec
            idx += 1
            print(f"\r  화면 {idx}장 그리는 중…", end="", flush=True)
        clock += dur

    print(f"\r  화면 {idx}장 완성.            ")

    # 목록 파일
    lst = BUILD / "frames.txt"
    with lst.open("w", encoding="utf-8") as f:
        for fp, sec in entries:
            f.write(f"file '{fp.as_posix()}'\nduration {sec:.3f}\n")
        f.write(f"file '{entries[-1][0].as_posix()}'\n")

    out_mp4 = OUT / f"{data['date'].replace('-', '')}_묵상.mp4"
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff, "-y", "-f", "concat", "-safe", "0", "-i", str(lst)]
    for p in paths:
        cmd += ["-i", str(p)]
    cmd += [
        "-filter_complex", "[1:a][2:a][3:a][4:a]concat=n=4:v=0:a=1[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
        "-crf", "21", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-movflags", "+faststart", str(out_mp4),
    ]
    print("  영상 만드는 중… (몇 분 걸립니다)")
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode != 0:
        print("✕ 영상 만들기 실패")
        print(r.stderr.decode("utf-8", "ignore")[-1500:])
        return 1

    mb = out_mp4.stat().st_size / 1024 / 1024
    print(f"  ✓ {out_mp4.relative_to(BASE)}  ({mb:,.1f} MB)")

    # 구간 시각을 content.js 에 적어둡니다 (홈페이지 건너뛰기·반복에 씁니다)
    clock = 0.0
    for t, dur in zip(data["tracks"], durs):
        t["start"] = round(clock, 2)
        t["end"] = round(clock + dur, 2)
        clock += dur
    data["totalSec"] = round(clock, 2)
    data.setdefault("youtubeId", "")
    cjs.write_text(
        "window.MEDITATION = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"  ✓ site/content.js 에 구간 시각 기록 (낭독 0:00 / " +
          " / ".join(f"{t['label']} {hms(t['start'])}" for t in data["tracks"][1:]) + ")")

    # 유튜브에 붙여넣을 정보
    desc = [
        f"유란시아서 {data['reference']}  {data['paperTitle']} · {data['sectionTitle']}",
        "",
        data["oneLine"],
        "",
        "── 순서 ──",
    ]
    for t0, lab in chapters:
        desc.append(f"{hms(t0)} {lab}")
    desc += [
        "",
        "── 낭독 본문 ──",
        data["tracks"][0]["text"],
        "",
        "#유란시아서 #묵상 #오늘의묵상",
    ]
    info = OUT / "youtube_info.txt"
    info.write_text(
        f"[제목]\n오늘의 묵상 {data['date']} · {data['theme']} ({data['reference']})\n\n"
        f"[설명]\n" + "\n".join(desc) + "\n",
        encoding="utf-8",
    )
    print(f"  ✓ {info.relative_to(BASE)}  (제목·설명·챕터)")
    print("  유튜브에 올린 뒤 주소를 알려주시면 홈페이지에 연결해 드립니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

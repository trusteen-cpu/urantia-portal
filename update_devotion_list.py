# -*- coding: utf-8 -*-
"""
묵상 목록(devotion/index.html) 다시 채우기
================================================================
업로드는 이미 끝난 것으로 하고, devotion 폴더 안에 실제로 만들어져 있는
날짜 폴더들을 읽어서 devotion/index.html 의 날짜 목록만 다시 만듭니다.
아무것도 archive.org 에 올리지 않습니다. 인터넷 접속도 필요 없습니다.

쓰는 법
    python update_devotion_list.py
"""

import io
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

# ══════════════════════════════════════════════════════════════
REPO = r"E:\OneDrive\문서\GitHub\urantia-portal"
PROGRESS = "publish_progress.json"
# ══════════════════════════════════════════════════════════════


def read_text(path):
    for enc in ("utf-8", "utf-8-sig", "cp949"):
        try:
            with io.open(path, encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, LookupError):
            continue
    with io.open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def write_text(path, s):
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(s)


def grab(src, name):
    m = re.search(r'^%s\s*=\s*"""(.*?)"""' % name, src, re.S | re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r"^%s\s*=\s*[\"'](.*?)[\"']\s*$" % name, src, re.M)
    return m.group(1).strip() if m else ""


def korean_date(d):
    y, mo, da = d.split("-")
    return "%s년 %d월 %d일" % (y, int(mo), int(da))


def slug_to_date_kind(slug):
    m = re.match(r"^(\d{4}-\d{2}-\d{2})-(night|morning)$", slug)
    if not m:
        return None, None
    date, en = m.groups()
    return date, ("취침" if en == "night" else "아침")


def load_existing_entries(html):
    """devotion/index.html 안의 DAYS 배열을 읽어 옵니다."""
    m = re.search(r"var DAYS = (\[[\s\S]*?\n\]);", html)
    if not m:
        return [], None, None
    block = m.group(1)
    entries = []
    for em in re.finditer(
        r'folder:\s*"([^"]*)"\s*,\s*kind:\s*"([^"]*)"\s*,\s*date:\s*"([^"]*)"\s*,\s*'
        r'title:\s*"([^"]*)"\s*,\s*source:\s*"([^"]*)"\s*,\s*verse:\s*"([^"]*)"',
        block,
    ):
        folder, kind, date, title, source, verse = em.groups()
        entries.append(dict(folder=folder, kind=kind, date=date,
                             title=title, source=source, verse=verse))
    return entries, m.start(), m.end()


def load_from_deployed_folder(repo, slug):
    """devotion/<slug>/content.py 를 읽어 제목·출처·절을 가져옵니다."""
    date, kind = slug_to_date_kind(slug)
    if not date:
        return None
    cpath = os.path.join(repo, "devotion", slug, "content.py")
    title = source = citation = ""
    if os.path.exists(cpath):
        src = read_text(cpath)
        title = grab(src, "TITLE")
        source = grab(src, "SOURCE")
        citation = grab(src, "CITATION")
        k = grab(src, "KIND")
        if k:
            kind = k
    if not title:
        ipath = os.path.join(repo, "devotion", slug, "index.html")
        if os.path.exists(ipath):
            h = read_text(ipath)
            m = re.search(r"<title>(.*?)</title>", h, re.S)
            if m:
                t = m.group(1)
                title = t.split("\u00b7")[-1].strip() or t.strip()
    return dict(folder=slug, kind=kind, date=korean_date(date),
                title=title or date, source=source, verse=citation)


def entry_sort_key(e):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})-", e["folder"])
    if m:
        return (m.group(1), m.group(2), m.group(3), e["kind"])
    return ("0000", "00", "00", "")


def build_days_block(entries):
    lines = []
    for e in entries:
        lines.append(
            '  { folder: "%s", kind: "%s", date: "%s",\n'
            '    title: "%s", source: "%s", verse: "%s" }'
            % (e["folder"], e["kind"], e["date"], e["title"], e["source"], e["verse"])
        )
    return "var DAYS = [\n" + ",\n".join(lines) + "\n];"


def main():
    print("=" * 60)
    print("devotion 목록 다시 채우기")
    print("=" * 60)

    idx_path = os.path.join(REPO, "devotion", "index.html")
    if not os.path.exists(idx_path):
        print("devotion/index.html 을 찾을 수 없습니다: %s" % idx_path)
        sys.exit(1)
    if not os.path.exists(PROGRESS):
        print("%s 를 찾을 수 없습니다. publish_devotions.py 와 같은 폴더에서 실행하십시오." % PROGRESS)
        sys.exit(1)

    html = read_text(idx_path)
    existing, start, end = load_existing_entries(html)
    if start is None:
        print("devotion/index.html 안에서 DAYS 목록을 찾지 못했습니다.")
        sys.exit(1)

    print("\n기존 목록: %d개" % len(existing))
    for e in existing:
        print("  (기존) %-22s %s" % (e["folder"], e["title"]))

    have = set(e["folder"] for e in existing)
    progress = json.loads(read_text(PROGRESS))

    added = []
    for slug in progress:
        if slug in have:
            continue
        entry = load_from_deployed_folder(REPO, slug)
        if entry is None:
            print("  [건너뜀] 이름 형식을 알 수 없습니다: %s" % slug)
            continue
        added.append(entry)

    print("\n새로 더할 항목: %d개" % len(added))
    for e in sorted(added, key=entry_sort_key):
        print("  (추가) %-22s %-4s %-20s %s" % (e["folder"], e["kind"], e["title"][:20], e["verse"]))

    all_entries = existing + added
    all_entries.sort(key=entry_sort_key, reverse=True)

    new_block = build_days_block(all_entries)
    new_html = html[:start] + new_block + html[end:]
    write_text(idx_path, new_html)

    print("\n" + "=" * 60)
    print("완료. devotion/index.html 을 새로 썼습니다.")
    print("전체 목록: %d개" % len(all_entries))
    print("깃허브 데스크탑에서 devotion 폴더를 커밋, 푸시하십시오.")
    print("=" * 60)


if __name__ == "__main__":
    main()

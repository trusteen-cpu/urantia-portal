# -*- coding: utf-8 -*-
"""
지난 묵상 한꺼번에 올리기
================================================================
PC에 쌓여 있는 7월·8월 묵상 폴더를 훑어서

  1) audio 폴더의 mp3를 인터넷 아카이브에 올리고
  2) index.html이 그 아카이브 주소를 부르도록 고치고
  3) 고친 것을 깃허브 폴더의 devotion/ 안에 복사하고
  4) devotion/index.html의 목록(DAYS)을 전부 다시 만듭니다.

mp3는 깃허브에 올라가지 않습니다. 저장소가 무거워지지 않습니다.

────────────────────────────────────────────────────────────────
처음 한 번만 (파워셸에 붙여 넣기)
────────────────────────────────────────────────────────────────
    pip install internetarchive
    ia configure

  ia configure 는 archive.org 이메일과 비밀번호를 묻습니다.
  한 번 넣으면 다음부터는 묻지 않습니다.

────────────────────────────────────────────────────────────────
쓰는 법
────────────────────────────────────────────────────────────────
    (1) 아래 ROOTS 와 REPO 의 경로를 실제 경로로 고칩니다.
    (2) DRY_RUN = True 인 채로 한 번 실행해 목록만 확인합니다.
            python publish_devotions.py
    (3) 목록이 맞으면 DRY_RUN = False 로 바꾸고 다시 실행합니다.

  중간에 끊겨도 괜찮습니다. 이미 끝난 폴더는 건너뜁니다
  (publish_progress.json 에 기록됩니다).

  ※ 접속이 불안정해서 "끝남"으로 기록됐는데 실제로는 archive.org에
     안 올라간 경우가 있었던 문제를 고쳤습니다(올린 뒤 실제로 다시
     확인하는 절차를 추가). 이 문제를 겪으셨다면 다시 실행하기 전에
     publish_progress.json 파일을 지우거나 이름을 바꾸고 처음부터
     다시 실행하십시오. 지우지 않으면 잘못 기록된 항목들이 계속
     건너뛰어집니다.
"""

import io
import json
import os
import re
import shutil
import sys
import time
import traceback

import requests

# cmd.exe(한글 Windows)는 기본으로 cp949를 씁니다. 이 코드 방식으로 표현 안 되는
# 글자를 print()로 찍으면 프로그램이 그 자리에서 멈춥니다. 화면에 어떤 글자가
# 나와도 멈추지 않도록 UTF-8로 강제하고, 그래도 안 되면 깨진 글자로 대신 표시합니다.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

# ══════════════════════════════════════════════════════════════
# 여기만 고치십시오
# ══════════════════════════════════════════════════════════════

# 묵상 폴더들이 들어 있는 곳. 여러 개면 줄을 더하십시오.
#   (경로, 저녁이면 "취침" 아침이면 "아침")
ROOTS = [
    (r"E:\OneDrive\내 문서\유란시아\저녁 명상", "취침"),
    (r"E:\OneDrive\내 문서\유란시아\아침 명상", "아침"),
]

# 깃허브 데스크탑이 관리하는 저장소 폴더
REPO = r"E:\OneDrive\문서\GitHub\urantia-portal"

DRY_RUN = False          # True 면 아무것도 올리지 않고 목록만 보여 줍니다
UPLOAD_AUDIO = True     # False 면 아카이브 업로드를 건너뛰고 파일 정리만 합니다

# 깃허브에 복사할 파일 (API 열쇠가 든 generate_audio_daily.py 는 뺍니다)
COPY_FILES = ["index.html", "content.py", "build_index.py", "lyrics.txt", "README.txt"]

PROGRESS = "publish_progress.json"
ERROR_LOG = "publish_errors.log"

# ══════════════════════════════════════════════════════════════

DATE_RE = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")


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
    """content.py 에서 NAME = "..." 값을 뽑습니다 (import 하지 않습니다)."""
    m = re.search(r'^%s\s*=\s*"""(.*?)"""' % name, src, re.S | re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r"^%s\s*=\s*[\"'](.*?)[\"']\s*$" % name, src, re.M)
    return m.group(1).strip() if m else ""


def korean_date(d):
    y, mo, da = d.split("-")
    return "%s년 %d월 %d일" % (y, int(mo), int(da))


def find_folders():
    """날짜 이름을 가진 폴더를 모두 찾습니다."""
    found = []
    for root, kind in ROOTS:
        if not os.path.isdir(root):
            print("  [건너뜀] 폴더가 없습니다: %s" % root)
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            if "index.html" not in filenames:
                continue
            m = DATE_RE.search(os.path.basename(dirpath))
            if not m:
                continue
            found.append({
                "path": dirpath,
                "date": "%s-%s-%s" % m.groups(),
                "kind": kind,
            })
    found.sort(key=lambda x: (x["date"], x["kind"]))
    return found


def describe(item):
    """content.py 와 index.html 에서 제목·출처·절을 읽어 옵니다."""
    cpath = os.path.join(item["path"], "content.py")
    title = source = citation = ""
    kind = item["kind"]
    if os.path.exists(cpath):
        src = read_text(cpath)
        title = grab(src, "TITLE")
        source = grab(src, "SOURCE")
        citation = grab(src, "CITATION")
        k = grab(src, "KIND")
        if k:
            kind = k
    if not title:
        h = read_text(os.path.join(item["path"], "index.html"))
        m = re.search(r"<title>(.*?)</title>", h, re.S)
        if m:
            t = m.group(1)
            title = t.split("·")[-1].strip() or t.strip()
    item["title"] = title or item["date"]
    item["source"] = source
    item["citation"] = citation
    item["kind"] = kind
    item["slug"] = "%s-%s" % (item["date"], "night" if kind == "취침" else "morning")
    item["archive_id"] = "urantia-devotion-%s" % item["slug"]
    item["mp3s"] = sorted(
        f for f in os.listdir(os.path.join(item["path"], "audio"))
        if f.lower().endswith(".mp3")
    ) if os.path.isdir(os.path.join(item["path"], "audio")) else []
    return item


def patch_html(html, base):
    """index.html 안의 audio/ 경로를 아카이브 주소로 바꿉니다."""
    if not base.endswith("/"):
        base += "/"
    n = 0

    # 새 형식: audioBase 값이 들어 있는 경우
    def repl_base(m):
        return m.group(1) + base + m.group(3)
    html2, c = re.subn(r'("audioBase"\s*:\s*")([^"]*)(")', repl_base, html)
    n += c

    # 옛 형식: "audio/01_reading.mp3" 같은 직접 경로
    html2, c = re.subn(r'(["\'])audio/([0-9A-Za-z_\-]+\.mp3)\1',
                       lambda m: m.group(1) + base + m.group(2) + m.group(1), html2)
    n += c

    # "audio/" + key + ".mp3" 처럼 이어 붙이는 경우
    html2, c = re.subn(r'(["\'])audio/\1', lambda m: m.group(1) + base + m.group(1), html2)
    n += c

    return html2, n


def patch_content(src, base):
    if re.search(r"^AUDIO_BASE\s*=", src, re.M):
        return re.sub(r'^AUDIO_BASE\s*=\s*".*?"',
                      'AUDIO_BASE = "%s"' % base, src, count=1, flags=re.M)
    return src


def log_error(slug, e):
    with io.open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 40 + "\n")
        f.write("%s  [%s]\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), slug))
        if e is not None:
            try:
                lines = traceback.format_exception(type(e), e, getattr(e, "__traceback__", None))
                f.write("".join(lines))
            except Exception:
                f.write(repr(e) + "\n")
        else:
            f.write("(원인 정보 없음)\n")


def verify_upload(archive_id, local_files, tries=4, wait=15):
    """서버가 '성공'이라 답해도 실제로는 파일이 덜 올라갈 수 있습니다.
    직접 내려받기 주소를 두드려 크기가 맞는지 다시 확인합니다.
    (방금 올린 직후엔 목록에 아직 안 뜰 수 있어 몇 번 다시 확인합니다.)"""
    for attempt in range(tries):
        if attempt:
            time.sleep(wait)
        ok = True
        for p in local_files:
            name = os.path.basename(p)
            url = "https://archive.org/download/%s/%s" % (archive_id, name)
            try:
                r = requests.head(url, timeout=30, allow_redirects=True)
                want = os.path.getsize(p)
                got = int(r.headers.get("Content-Length", -1))
                if r.status_code != 200 or got != want:
                    ok = False
                    break
            except Exception:
                ok = False
                break
        if ok:
            return True
    return False


def upload(item):
    from internetarchive import upload as ia_upload
    files = [os.path.join(item["path"], "audio", f) for f in item["mp3s"]]
    md = {
        "title": "오늘의 %s 묵상 %s %s" % (item["kind"], item["date"], item["title"]),
        "mediatype": "audio",
        "collection": "opensource_audio",
        "subject": ["유란시아서", "묵상", "Urantia"],
        "creator": "Jay Han",
        "date": item["date"],
        "language": "Korean",
    }
    last_err = None
    for attempt in range(1, 4):
        try:
            res = ia_upload(
                item["archive_id"], files=files, metadata=md, verbose=False,
                retries=3, retries_sleep=15,
                request_kwargs={"timeout": 120},
            )
            ok = all(getattr(r, "status_code", 200) in (200, None) for r in res)
            if ok:
                print("  올라간 것을 다시 확인하는 중...")
                if verify_upload(item["archive_id"], files):
                    return True
                last_err = Exception("서버는 성공이라 했지만 실제 파일 확인에 실패했습니다 (접속 불안정 의심)")
            else:
                last_err = Exception("서버가 성공이 아닌 응답을 돌려주었습니다")
        except Exception as e:
            last_err = e
        if attempt < 3:
            print("  %d번째 시도 실패 - 20초 뒤 다시 시도합니다..." % attempt)
            time.sleep(20)
    log_error(item["slug"], last_err)
    print("  업로드 실패(3회 시도) - 자세한 내용은 %s 에 기록했습니다" % ERROR_LOG)
    return False


def build_days(entries):
    lines = []
    for e in entries:
        lines.append(
            '  { folder: "%s", kind: "%s", date: "%s",\n'
            '    title: "%s", source: "%s", verse: "%s" }'
            % (e["slug"], e["kind"], korean_date(e["date"]),
               e["title"], e["source"], e["citation"])
        )
    return "var DAYS = [\n" + ",\n".join(lines) + "\n];"


def update_list_page(entries):
    path = os.path.join(REPO, "devotion", "index.html")
    if not os.path.exists(path):
        print("  [주의] %s 가 없어 목록은 건드리지 않았습니다." % path)
        return
    html = read_text(path)
    m = re.search(r"var DAYS = \[[\s\S]*?\n\];", html)
    if not m:
        print("  [주의] DAYS 목록을 찾지 못했습니다. 목록은 그대로 둡니다.")
        return
    newest_first = sorted(entries, key=lambda e: (e["date"], e["kind"]), reverse=True)
    write_text(path, html[:m.start()] + build_days(newest_first) + html[m.end():])
    print("  목록 갱신: %d개" % len(newest_first))


def main():
    print("=" * 60)
    print("지난 묵상 한꺼번에 올리기   %s" % ("[시험 실행]" if DRY_RUN else "[실제 실행]"))
    print("=" * 60)

    if not os.path.isdir(REPO):
        print("깃허브 폴더를 찾을 수 없습니다: %s" % REPO)
        sys.exit(1)

    done = {}
    if os.path.exists(PROGRESS):
        done = json.loads(read_text(PROGRESS))

    items = [describe(x) for x in find_folders()]
    if not items:
        print("묵상 폴더를 찾지 못했습니다. ROOTS 경로를 확인하십시오.")
        sys.exit(1)

    # 같은 날짜·같은 종류(취침/아침)가 두 폴더에서 나오면 겹칩니다.
    # mp3가 더 많이 든 쪽을 진짜로 보고, 나머지는 알려 주고 건너뜁니다.
    by_slug = {}
    for it in items:
        prev = by_slug.get(it["slug"])
        if prev is None or len(it["mp3s"]) > len(prev["mp3s"]):
            by_slug[it["slug"]] = it
    if len(by_slug) != len(items):
        print("\n[중복 폴더 발견 - mp3가 더 많은 쪽만 씁니다]")
        for it in items:
            if by_slug[it["slug"]] is not it:
                print("  건너뜀: %s  (%s, mp3 %d개)" % (it["path"], it["slug"], len(it["mp3s"])))
    items = sorted(by_slug.values(), key=lambda x: (x["date"], x["kind"]))

    print("\n찾은 묵상 %d개\n" % len(items))
    for it in items:
        mark = "이미 끝남" if it["slug"] in done else ("mp3 %d개" % len(it["mp3s"]))
        print("  %-22s %-4s %-18s %-10s %s"
              % (it["slug"], it["kind"], it["title"][:16], it["citation"], mark))

    if DRY_RUN:
        print("\n시험 실행이라 여기서 멈춥니다.")
        print("목록이 맞으면 파일 위쪽의 DRY_RUN 을 False 로 바꾸고 다시 실행하십시오.")
        return

    print("")
    for it in items:
        slug = it["slug"]
        if slug in done:
            print("[%s] 이미 끝남 - 건너뜁니다" % slug)
            continue
        print("[%s] %s" % (slug, it["title"]))

        base = "https://archive.org/download/%s/" % it["archive_id"]

        if UPLOAD_AUDIO and it["mp3s"]:
            print("  아카이브 업로드 %d개..." % len(it["mp3s"]))
            if not upload(it):
                print("  이 폴더는 건너뜁니다 - 나중에 다시 실행하면 재시도합니다")
                continue
        elif not it["mp3s"]:
            print("  mp3가 없습니다 - 파일만 정리합니다")

        dest = os.path.join(REPO, "devotion", slug)
        os.makedirs(dest, exist_ok=True)

        html, n = patch_html(read_text(os.path.join(it["path"], "index.html")), base)
        write_text(os.path.join(dest, "index.html"), html)
        print("  index.html 주소 %d곳 교체" % n)

        for name in COPY_FILES:
            if name == "index.html":
                continue
            src_path = os.path.join(it["path"], name)
            if not os.path.exists(src_path):
                continue
            if name == "content.py":
                write_text(os.path.join(dest, name),
                           patch_content(read_text(src_path), base))
            else:
                shutil.copy2(src_path, os.path.join(dest, name))

        done[slug] = base
        write_text(PROGRESS, json.dumps(done, ensure_ascii=False, indent=1))
        print("  완료 -> devotion/%s/" % slug)
        time.sleep(2)

    update_list_page(items)

    print("\n" + "=" * 60)
    print("끝났습니다.")
    print("깃허브 데스크탑을 열어 커밋하고 푸시하십시오.")
    print("주소: https://urantiareaders.com/devotion/<날짜>-night/")
    print("=" * 60)


if __name__ == "__main__":
    main()

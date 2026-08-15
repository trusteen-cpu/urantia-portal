# -*- coding: utf-8 -*-
"""
유란시아 핵심교리 오디오북을 인터넷 아카이브에 올리고
각 강의 index.html이 그 주소의 음성을 쓰도록 자동으로 고칩니다.

준비 (한 번만 하면 됩니다)
    1) archive.org 에서 무료 계정을 만듭니다 (없으면).
    2) 명령 프롬프트나 파워셸에서:
           pip install internetarchive
           ia configure
       ia configure 를 실행하면 archive.org 이메일과 비밀번호를 물어봅니다.
       한 번만 하면 다음부터는 안 물어봅니다.

쓰는 법
    1) 아래 ROOT_KR, ROOT_EN 을 여러분 PC의 실제 폴더 경로로 고칩니다.
    2) 먼저 딱 한 강만 시험해 보려면 TEST_ONLY_FIRST = True 로 둔 채 실행합니다.
    3) 잘 되면 TEST_ONLY_FIRST = False 로 바꾸고 다시 실행하면 나머지 전부가
       한 번에 올라갑니다. 이미 끝난 강은 자동으로 건너뜁니다.

           python publish_audiobook.py

결과
    out 폴더 아래에 강마다 "손질된" index.html 만 생깁니다.
    (음성은 이제 인터넷 아카이브에 있으므로 audio 폴더는 만들지 않습니다)
    이 out 폴더를 그대로 깃허브의 audiobook 폴더 자리에 올리면 됩니다.
        out/audiobook/kr/ch01/index.html
        out/audiobook/kr/ch02/index.html ...
        out/audiobook/en/ch01/index.html ...
"""

import os
import re
import sys
import glob
import json

try:
    from internetarchive import upload
except ImportError:
    sys.exit(
        "internetarchive 모듈이 없습니다.\n"
        "명령 프롬프트에서 다음을 먼저 실행하세요:\n"
        "    pip install internetarchive\n"
        "    ia configure\n"
    )

# ── 여기 두 줄을 여러분 PC 경로로 고치세요 ──────────────────
# 강 폴더들이 바로 이 안에 들어있어야 합니다 (1강_영생, 2강_..., ...).
# 해당 언어가 없으면 빈 문자열 "" 로 두세요.
ROOT_KR = r"E:\OneDrive\내 문서\유란시아\책쓰기\유란시아서 핵심\유란시아서 핵심 개념 비데오\음성전자책"
ROOT_EN = r"E:\OneDrive\내 문서\유란시아\책쓰기\유란시아서 핵심\Urantia Core Truth Video\Core Theme Reader"

# 처음에는 True 로 두어 한 강만 시험하고, 잘 되면 False 로 바꿔 전체를 돌리세요.
# (이번 파일은 이미 False 로 되어 있어 실행하면 바로 전체가 시작됩니다)
TEST_ONLY_FIRST = False

ITEM_PREFIX = "urantia-coretruth-audiobook"   # archive.org 항목 이름의 앞부분
PROGRESS_FILE = "publish_progress.json"        # 끝난 강을 기록해 두어 다시 돌릴 때 건너뜀
OUT_DIR = "out"


def chapter_number(folder_name, fallback):
    """'3강_...', 'cd11_...' 처럼 폴더 이름 어디에 있든 숫자를 찾아 뽑습니다.
    못 찾으면 순서대로 매깁니다."""
    m = re.search(r"(\d+)", folder_name)
    return int(m.group(1)) if m else fallback


def find_chapters(root, lang):
    if not root or not os.path.isdir(root):
        return []
    out = []
    subs = sorted(os.listdir(root))
    for i, name in enumerate(subs, 1):
        chap_dir = os.path.join(root, name)
        if not os.path.isdir(chap_dir):
            continue
        index_path = os.path.join(chap_dir, "index.html")
        audio_dir = os.path.join(chap_dir, "audio")
        if not os.path.exists(index_path) or not os.path.isdir(audio_dir):
            continue
        num = chapter_number(name, i)
        code = "ch%02d" % num
        out.append({
            "dir": chap_dir,
            "index": index_path,
            "audio": audio_dir,
            "lang": lang,
            "code": code,
            "title": name,
        })
    out.sort(key=lambda c: c["code"])
    return out


def chapter_title(folder_name):
    """'ch04_하늘왕국' 같은 폴더 이름에서 뒤쪽 제목만 뽑습니다. 못 찾으면 폴더 이름 전체를 씁니다."""
    m = re.match(r"^[A-Za-z]*\d+[_\-\s]*(.+)$", folder_name)
    title = m.group(1).strip() if m else folder_name
    return title if title else folder_name


PLAYER_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — 유란시아 핵심교리 오디오북</title>
<style>
:root{{--navy:#1f3f52;--gold:#d8b45a;--ink:#20272c;--line:#dfe6ea;--bg:#f6f8f9}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
 font-family:"Malgun Gothic","맑은 고딕",system-ui,-apple-system,sans-serif;line-height:1.6}}
.hd{{background:linear-gradient(160deg,#16303f,#1f3f52 60%,#264a5c);color:#fff;
 border-bottom:3px solid var(--gold);padding:16px 20px}}
.hd .in{{max-width:720px;margin:0 auto}}
.hd .crumb{{font-size:12px;color:#b9cdd8;margin-bottom:6px}}
.hd .crumb a{{color:#b9cdd8;text-decoration:none}}
.hd h1{{margin:0;font-size:20px}}
.wrap{{max-width:720px;margin:0 auto;padding:22px 20px 50px}}
.player{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px;margin-bottom:20px}}
.player .now{{font-size:13.5px;color:#5d6b73;margin-bottom:10px}}
audio{{width:100%}}
.bar{{display:flex;gap:8px;margin-top:12px}}
.bar button{{flex:1;background:var(--navy);color:#fff;border:0;border-radius:20px;
 padding:9px;font-size:13.5px;font-family:inherit;cursor:pointer}}
.bar button:disabled{{background:#c7d1d8;cursor:default}}
.list{{display:flex;flex-direction:column;gap:6px}}
.item{{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:8px;
 border:1px solid var(--line);background:#fff;cursor:pointer;font-size:13.5px}}
.item:hover{{border-color:var(--navy)}}
.item.on{{border-color:var(--gold);background:#fffaf0}}
.item .n{{flex:none;width:26px;color:var(--navy);font-weight:700;font-size:12px}}
.foot{{margin-top:24px;font-size:12px;color:#8a97a0;text-align:center}}
.foot a{{color:var(--navy);text-decoration:none;border-bottom:1px solid #c2d0d7}}
</style>
</head>
<body>
<div class="hd"><div class="in">
  <div class="crumb"><a href="/">홈</a> › 핵심교리 오디오북</div>
  <h1>{title}</h1>
</div></div>
<div class="wrap">
  <div class="player">
    <div class="now" id="now">1 / {count}</div>
    <audio id="au" controls></audio>
    <div class="bar">
      <button id="prev">◀ 이전</button>
      <button id="play">재생</button>
      <button id="next">다음 ▶</button>
    </div>
  </div>
  <div class="list" id="list"></div>
  <div class="foot"><a href="/audiobook.html">오디오북 목록</a> · <a href="/">포털 첫 화면</a></div>
</div>
<script>
var BASE = "{base_url}";
var FILES = {files_json};
var au = document.getElementById('au'), list = document.getElementById('list'),
    now = document.getElementById('now'), playBtn = document.getElementById('play'),
    cur = 0;

FILES.forEach(function(f, i) {{
  var d = document.createElement('div');
  d.className = 'item';
  d.innerHTML = '<span class="n">' + (i + 1) + '</span><span>슬라이드 ' + (i + 1) + '</span>';
  d.onclick = function() {{ load(i, true); }};
  list.appendChild(d);
}});

function load(i, autoplay) {{
  cur = (i + FILES.length) % FILES.length;
  au.src = BASE + '/' + FILES[cur];
  now.textContent = (cur + 1) + ' / ' + FILES.length;
  [].forEach.call(list.children, function(el, n) {{ el.className = 'item' + (n === cur ? ' on' : ''); }});
  if (autoplay) {{ au.play(); playBtn.textContent = '정지'; }}
}}

au.addEventListener('ended', function() {{ if (cur < FILES.length - 1) load(cur + 1, true); }});
playBtn.onclick = function() {{
  if (au.paused) {{ au.play(); playBtn.textContent = '정지'; }}
  else {{ au.pause(); playBtn.textContent = '재생'; }}
}};
document.getElementById('prev').onclick = function() {{ load(cur - 1, true); }};
document.getElementById('next').onclick = function() {{ load(cur + 1, true); }};

load(0, false);
</script>
</body>
</html>
"""


def build_player(title, lang, base_url, filenames):
    return PLAYER_TEMPLATE.format(
        title=title,
        lang_attr="ko" if lang == "kr" else "en",
        count=len(filenames),
        base_url=base_url,
        files_json=json.dumps(filenames, ensure_ascii=False),
    )


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        return json.load(open(PROGRESS_FILE, encoding="utf-8"))
    return {}


def save_progress(done):
    json.dump(done, open(PROGRESS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def main():
    chapters = find_chapters(ROOT_KR, "kr") + find_chapters(ROOT_EN, "en")
    if not chapters:
        sys.exit("강 폴더를 하나도 못 찾았습니다. ROOT_KR / ROOT_EN 경로를 확인하세요.")

    print("찾은 강: %d개" % len(chapters))
    for c in chapters:
        print("  [%s-%s] %s" % (c["lang"], c["code"], c["title"]))

    if TEST_ONLY_FIRST:
        chapters = chapters[:1]
        print("\nTEST_ONLY_FIRST = True 라서 첫 강만 시험합니다.\n")

    done = load_progress()
    os.makedirs(OUT_DIR, exist_ok=True)

    for c in chapters:
        item_id = "%s-%s-%s" % (ITEM_PREFIX, c["lang"], c["code"])

        if done.get(item_id):
            print("건너뜀 (이미 끝남):", item_id)
            continue

        print("=" * 56)
        print(c["title"], "→", item_id)

        files = sorted(glob.glob(os.path.join(c["audio"], "*.mp3")))
        if not files:
            print("  ! mp3가 없습니다:", c["audio"])
            continue

        print("  올리는 중 (%d개 파일, 시간이 좀 걸립니다)..." % len(files))
        try:
            results = upload(
                item_id,
                files=files,
                metadata={
                    "title": "유란시아 핵심교리 오디오북 " + c["title"],
                    "mediatype": "audio",
                    "collection": "opensource_audio",
                    "creator": "Jay Han (한종인)",
                    "subject": "Urantia Book; Urantia; 유란시아서; 핵심교리",
                    "language": "kor" if c["lang"] == "kr" else "eng",
                },
                verbose=True,
            )
        except Exception as e:
            print("  ! 업로드 실패:", e)
            continue

        ok = all(getattr(r, "status_code", 200) in (None, 200) for r in results)
        if not ok:
            print("  ! 일부 파일 업로드에 문제가 있었습니다. 위 로그를 보세요.")
            continue

        base_url = "https://archive.org/download/%s" % item_id
        filenames = sorted(os.path.basename(f) for f in files)
        title = chapter_title(c["title"])
        html = build_player(title, c["lang"], base_url, filenames)

        out_path = os.path.join(OUT_DIR, "audiobook", c["lang"], c["code"], "index.html")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        open(out_path, "w", encoding="utf-8").write(html)

        done[item_id] = True
        save_progress(done)
        print("  완료 → %s  (%d개 트랙, 제목: %s)" % (out_path, len(filenames), title))

    print("=" * 56)
    print("끝났습니다.")
    print("'%s' 폴더를 그대로 깃허브의 audiobook 폴더 자리에 올리세요." % OUT_DIR)
    if TEST_ONLY_FIRST:
        print("첫 강이 잘 되면 이 파일 위쪽의 TEST_ONLY_FIRST 를 False 로 바꾸고")
        print("다시 실행하세요. 이미 끝난 강은 건너뛰고 나머지만 올라갑니다.")


if __name__ == "__main__":
    main()

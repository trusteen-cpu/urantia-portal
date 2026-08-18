# -*- coding: utf-8 -*-
"""content.py를 읽어 index.html을 만듭니다.  실행: python build_index.py"""

import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import content as C

HERE = os.path.dirname(os.path.abspath(__file__))

base = C.AUDIO_BASE.rstrip("/")
src = (lambda k: f"{base}/{k}.mp3") if base else (lambda k: f"audio/{k}.mp3")

lyric_blocks = []
for block in C.LYRICS.strip().split("\n\n"):
    lines = [x for x in block.split("\n") if x.strip()]
    if not lines:
        continue
    tag = lines[0].strip() if lines[0].strip().startswith("[") else ""
    body = lines[1:] if tag else lines
    lyric_blocks.append({"tag": tag, "lines": body})

DATA = {
    "date": C.DATE,
    "kind": C.KIND,
    "title": C.TITLE,
    "source": C.SOURCE,
    "citation": C.CITATION,
    "songTitle": C.SONG_TITLE,
    "reading": C.READING,
    "sermon": C.SERMON,
    "lyrics": lyric_blocks,
    "prayer": C.PRAYER,
    "segments": [{"key": s["key"], "label": s["label"], "title": s["title"],
                  "src": src(s["key"])} for s in C.SEGMENTS],
}

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>오늘의 취침 묵상 __DATE__ · __TITLE__</title>
<style>
  * { box-sizing: border-box; }
  html, body { margin:0; padding:0; height:100%; }
  body {
    font-family: 'Noto Serif KR','맑은 고딕',serif;
    color:#e8ecf6;
    background: linear-gradient(180deg,#0b1020 0%,#121a33 55%,#1c2647 100%);
    min-height:100%;
  }
  #sky { position:fixed; inset:0; z-index:0; pointer-events:none; }
  .wrap { position:relative; z-index:1; max-width:820px; margin:0 auto; padding:28px 20px 120px; }
  header { text-align:center; padding:18px 0 10px; }
  header .kind { font-size:13px; letter-spacing:4px; color:#c8b06a; }
  header h1 { margin:10px 0 6px; font-size:30px; font-weight:700; }
  header .src { font-size:13px; color:#9fb0d0; line-height:1.7; }
  .menu { display:flex; gap:8px; justify-content:center; margin:22px 0 18px; flex-wrap:wrap; }
  .menu button {
    background:rgba(18,26,51,.42); color:#cfd8ee; border:1px solid rgba(200,176,106,.35);
    border-radius:999px; padding:8px 18px; font-size:14px; cursor:pointer;
    font-family:inherit;
  }
  .menu button.on { background:#c8b06a; color:#141a2c; border-color:#c8b06a; font-weight:700; }
  .panel {
    background:rgba(18,26,51,.42); border:1px solid rgba(255,255,255,.08);
    border-radius:18px; padding:26px 24px; line-height:2.0; font-size:17px;
  }
  .panel h2 { margin:0 0 16px; font-size:19px; color:#c8b06a; font-weight:700; }
  .panel p { margin:0 0 16px; }
  .panel p:last-child { margin-bottom:0; }
  .verse { color:#e8ecf6; }
  .cite { color:#c8b06a; font-size:14px; margin-bottom:14px; }
  .tag { color:#c8b06a; font-size:14px; margin:18px 0 6px; }
  .prayer p { margin:0; }
  .bar {
    position:fixed; left:0; right:0; bottom:0; z-index:2;
    background:rgba(9,13,26,.92); border-top:1px solid rgba(255,255,255,.08);
    padding:12px 16px 16px;
  }
  .bar .inner { max-width:820px; margin:0 auto; }
  .prog { height:6px; background:rgba(255,255,255,.12); border-radius:4px; cursor:pointer; }
  .prog span { display:block; height:100%; width:0; background:#c8b06a; border-radius:4px; }
  .ctrls { display:flex; align-items:center; gap:10px; margin-top:10px; flex-wrap:wrap; }
  .ctrls button {
    background:transparent; color:#cfd8ee; border:1px solid rgba(255,255,255,.18);
    border-radius:999px; padding:7px 14px; font-size:13px; cursor:pointer; font-family:inherit;
  }
  .ctrls .now { flex:1; font-size:13px; color:#9fb0d0; min-width:120px; }
  #overlay {
    position:fixed; inset:0; z-index:9; background:rgba(6,9,18,.94);
    display:flex; flex-direction:column; align-items:center; justify-content:center; gap:18px;
    text-align:center; padding:24px;
  }
  #overlay h2 { font-size:24px; margin:0; }
  #overlay p { color:#9fb0d0; margin:0; font-size:15px; line-height:1.9; }
  #overlay button {
    margin-top:8px; background:#c8b06a; color:#141a2c; border:0; border-radius:999px;
    padding:14px 34px; font-size:17px; font-weight:700; cursor:pointer; font-family:inherit;
  }
</style>
</head>
<body>
<canvas id="sky"></canvas>
<div class="wrap">
  <header>
    <div class="kind">오늘의 취침 묵상 · __DATE__</div>
    <h1>__TITLE__</h1>
    <div class="src">__SOURCE__<br>유란시아서 __CITATION__</div>
  </header>
  <div class="menu" id="menu"></div>
  <div class="panel" id="panel"></div>
</div>

<div class="bar">
  <div class="inner">
    <div class="prog" id="prog"><span id="progFill"></span></div>
    <div class="ctrls">
      <button id="btnPlay">일시정지</button>
      <button id="btnPrev">이전</button>
      <button id="btnNext">건너뛰기</button>
      <button id="btnRepeat">반복: 전체</button>
      <button id="btnMute">소리 끄기</button>
      <div class="now" id="now"></div>
    </div>
  </div>
</div>

<div id="overlay">
  <h2>오늘의 취침 묵상</h2>
  <p>__TITLE__<br>낭독 · 강론 · 노래 · 기도가 이어서 재생됩니다.</p>
  <button id="btnStart">시작하기</button>
</div>

<audio id="au"></audio>

<script>
var DATA = __DATA__;

/* 밤하늘 */
(function () {
  var c = document.getElementById('sky'), x = c.getContext('2d');
  function draw() {
    c.width = innerWidth; c.height = innerHeight;
    var mx = c.width - 90, my = 90;
    var g = x.createRadialGradient(mx, my, 10, mx, my, 160);
    g.addColorStop(0, 'rgba(255,246,214,.30)');
    g.addColorStop(1, 'rgba(255,246,214,0)');
    x.fillStyle = g; x.beginPath(); x.arc(mx, my, 160, 0, 7); x.fill();
    var g2 = x.createRadialGradient(mx, my, 5, mx, my, 60);
    g2.addColorStop(0, 'rgba(255,250,230,.9)');
    g2.addColorStop(1, 'rgba(255,250,230,0)');
    x.fillStyle = g2; x.beginPath(); x.arc(mx, my, 60, 0, 7); x.fill();
    x.fillStyle = '#fff8e2'; x.beginPath(); x.arc(mx, my, 43, 0, 7); x.fill();
    var seed = 7;
    function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }
    for (var i = 0; i < 150; i++) {
      var px = rnd() * c.width, py = rnd() * c.height * 0.85;
      if (Math.hypot(px - mx, py - my) < 150) continue;
      x.globalAlpha = 0.25 + rnd() * 0.6;
      x.fillStyle = '#ffffff';
      x.beginPath(); x.arc(px, py, rnd() * 1.3 + 0.3, 0, 7); x.fill();
    }
    x.globalAlpha = 1;
  }
  draw(); addEventListener('resize', draw);
})();

var au = document.getElementById('au');
var panel = document.getElementById('panel');
var menu = document.getElementById('menu');
var now = document.getElementById('now');
var progFill = document.getElementById('progFill');
var idx = 0, repeat = 0, missing = {};
var REPEAT_LABEL = ['반복: 전체', '반복: 이 메뉴', '반복: 없음'];

DATA.segments.forEach(function (s, i) {
  var b = document.createElement('button');
  b.textContent = s.label;
  b.onclick = function () { go(i, true); };
  menu.appendChild(b);
});

function esc(t) {
  return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function render(i) {
  var s = DATA.segments[i], h = '';
  if (s.key === '01_reading') {
    h += '<h2>낭독</h2><div class="cite">유란시아서 ' + esc(DATA.citation) + '</div>';
    DATA.reading.forEach(function (p) { h += '<p class="verse">' + esc(p) + '</p>'; });
  } else if (s.key === '02_sermon') {
    h += '<h2>강론</h2>';
    DATA.sermon.forEach(function (p) { h += '<p>' + esc(p) + '</p>'; });
  } else if (s.key === '03_song') {
    h += '<h2>' + esc(DATA.songTitle) + '</h2>';
    DATA.lyrics.forEach(function (b) {
      if (b.tag) h += '<div class="tag">' + esc(b.tag) + '</div>';
      h += '<p>' + b.lines.map(esc).join('<br>') + '</p>';
    });
  } else {
    h += '<h2>기도</h2><div class="prayer">';
    DATA.prayer.forEach(function (l) { h += '<p>' + esc(l) + '</p>'; });
    h += '</div>';
  }
  panel.innerHTML = h;
  Array.prototype.forEach.call(menu.children, function (b, k) {
    b.className = (k === i ? 'on' : '');
  });
  now.textContent = s.title;
}

function go(i, play) {
  idx = ((i % DATA.segments.length) + DATA.segments.length) % DATA.segments.length;
  var s = DATA.segments[idx];
  render(idx);
  au.src = s.src;
  if (play) { au.play().catch(function () {}); }
}

function nextIndex(from) {
  for (var k = 1; k <= DATA.segments.length; k++) {
    var j = (from + k) % DATA.segments.length;
    if (!missing[DATA.segments[j].key]) return j;
  }
  return from;
}

au.addEventListener('ended', function () {
  if (repeat === 1) { au.currentTime = 0; au.play(); return; }
  var j = nextIndex(idx);
  if (repeat === 2 && j <= idx) { render(idx); return; }
  go(j, true);
});

au.addEventListener('error', function () {
  missing[DATA.segments[idx].key] = true;      /* 노래가 아직 없으면 자동으로 넘어감 */
  var j = nextIndex(idx);
  if (j !== idx) go(j, true);
});

au.addEventListener('timeupdate', function () {
  if (au.duration) progFill.style.width = (au.currentTime / au.duration * 100) + '%';
});

document.getElementById('prog').onclick = function (e) {
  if (!au.duration) return;
  var r = this.getBoundingClientRect();
  au.currentTime = (e.clientX - r.left) / r.width * au.duration;
};
document.getElementById('btnPlay').onclick = function () {
  if (au.paused) { au.play(); this.textContent = '일시정지'; }
  else { au.pause(); this.textContent = '재생'; }
};
document.getElementById('btnNext').onclick = function () { go(nextIndex(idx), true); };
document.getElementById('btnPrev').onclick = function () { go(idx - 1, true); };
document.getElementById('btnRepeat').onclick = function () {
  repeat = (repeat + 1) % 3;
  this.textContent = REPEAT_LABEL[repeat];
};
document.getElementById('btnMute').onclick = function () {
  au.muted = !au.muted;
  this.textContent = au.muted ? '소리 켜기' : '소리 끄기';
};
document.addEventListener('keydown', function (e) {
  if (e.code === 'Space') { e.preventDefault(); document.getElementById('btnPlay').click(); }
  if (e.code === 'ArrowRight') go(nextIndex(idx), true);
  if (e.code === 'ArrowLeft') go(idx - 1, true);
});

document.getElementById('btnStart').onclick = function () {
  document.getElementById('overlay').style.display = 'none';
  go(0, true);
};

render(0);
</script>
</body>
</html>
"""

html = (HTML
        .replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
        .replace("__DATE__", C.DATE)
        .replace("__TITLE__", C.TITLE)
        .replace("__SOURCE__", C.SOURCE)
        .replace("__CITATION__", C.CITATION))

with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("index.html 생성 완료")

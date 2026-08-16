# -*- coding: utf-8 -*-
"""
index.html 만들기 (밤하늘 취침 테마)
    python build_index.py
content.py 를 고친 뒤 이것을 실행하면 index.html 이 새로 만들어집니다.
"""

import json
import content as C

DATA = {
    "date": C.DATE,
    "kind": C.KIND,
    "title": C.TITLE,
    "citation": C.CITATION,
    "source": C.SOURCE,
    "audioBase": C.AUDIO_BASE,
    "reading": C.READING,
    "sermon": C.SERMON,
    "songTitle": C.SONG_TITLE,
    "song": C.SONG_LYRICS,
    "prayer": C.PRAYER,
}

TPL = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>오늘의 __KIND__ 묵상 __DATE__ · __TITLE__</title>
<style>
:root {
  --gold:#e8c479; --goldD:#c9a24f; --ink:#eef1fb; --dim:#a8b0cd;
  --panel:rgba(18,26,51,.42); --line:rgba(232,196,121,.28);
}
* { box-sizing:border-box; margin:0; padding:0; }
html, body { height:100%; }
body {
  background:linear-gradient(180deg,#0b1020 0%,#121a33 52%,#1c2647 100%);
  color:var(--ink);
  font-family:'Noto Serif KR','Nanum Myeongjo','\\B9D1\\C740 \\ACE0\\B515',serif;
  line-height:1.9; min-height:100%; position:relative; overflow-x:hidden;
}
#sky { position:fixed; inset:0; z-index:0; pointer-events:none; }
.moon {
  position:fixed; top:46px; right:56px; width:86px; height:86px; border-radius:50%;
  background:radial-gradient(circle at 36% 34%, #fdf6e0 0%, #f0dfae 52%, #d9bd7a 100%);
  box-shadow:0 0 120px 40px rgba(232,196,121,.13), 0 0 300px 120px rgba(232,196,121,.07);
  z-index:0;
}
.wrap { position:relative; z-index:2; max-width:820px; margin:0 auto; padding:44px 22px 120px; }

header { text-align:center; margin-bottom:26px; }
.eyebrow { color:var(--gold); letter-spacing:.26em; font-size:12.5px; font-weight:700; }
h1 { font-size:38px; margin:16px 0 10px; letter-spacing:.02em; }
.rule { width:78px; height:3px; background:var(--gold); margin:14px auto; border-radius:2px; }
.src { color:var(--dim); font-size:14px; }
.cit { color:var(--gold); font-size:14.5px; font-weight:700; margin-top:4px; }

.tabs { display:flex; gap:9px; justify-content:center; flex-wrap:wrap; margin:26px 0 18px; }
.tab {
  background:transparent; color:var(--dim); border:1.4px solid var(--line);
  border-radius:22px; padding:8px 20px; font-family:inherit; font-size:14.5px; cursor:pointer;
}
.tab.on { background:var(--gold); color:#101731; border-color:var(--gold); font-weight:700; }

.panel {
  background:var(--panel); border:1px solid var(--line); border-radius:18px;
  padding:30px 30px 26px; min-height:260px;
  box-shadow:0 6px 30px rgba(0,0,0,.28); backdrop-filter:blur(3px);
}
.label { color:var(--gold); font-size:13px; letter-spacing:.2em; font-weight:700; margin-bottom:14px; }
.body { font-size:17px; white-space:pre-wrap; }
.body.verse { font-size:17.5px; line-height:2.05; }
.songtitle { color:var(--gold); font-size:19px; font-weight:700; margin-bottom:12px; }
.tag { color:var(--goldD); font-size:13.5px; letter-spacing:.12em; display:block; margin:16px 0 4px; }

.bar {
  position:fixed; left:0; right:0; bottom:0; z-index:5;
  background:rgba(9,13,28,.93); border-top:1px solid var(--line);
  padding:12px 18px 16px; backdrop-filter:blur(6px);
}
.barin { max-width:820px; margin:0 auto; }
.prog { height:5px; background:rgba(232,196,121,.16); border-radius:3px; cursor:pointer; overflow:hidden; }
.progin { height:100%; width:0; background:var(--gold); border-radius:3px; }
.ctrls { display:flex; gap:9px; align-items:center; justify-content:center; flex-wrap:wrap; margin-top:11px; }
.btn {
  background:transparent; color:var(--ink); border:1.4px solid var(--line);
  border-radius:20px; padding:7px 16px; font-family:inherit; font-size:14px; cursor:pointer;
}
.btn:hover { border-color:var(--gold); color:var(--gold); }
.btn.play { background:var(--gold); color:#101731; border-color:var(--gold); font-weight:700; padding:7px 24px; }
.btn.on { border-color:var(--gold); color:var(--gold); }
.time { color:var(--dim); font-size:13px; min-width:96px; text-align:center; }

.gate {
  position:fixed; inset:0; z-index:20; background:rgba(6,9,20,.93);
  display:flex; align-items:center; justify-content:center; text-align:center; padding:24px;
}
.gate .in { max-width:440px; }
.gate h2 { font-size:27px; margin-bottom:12px; }
.gate p { color:var(--dim); font-size:15px; margin-bottom:24px; }
.gate button {
  background:var(--gold); color:#101731; border:none; border-radius:26px;
  padding:14px 38px; font-family:inherit; font-size:17px; font-weight:700; cursor:pointer;
}
.hint { color:var(--dim); font-size:12.5px; text-align:center; margin-top:9px; }

@media (max-width:560px) {
  h1 { font-size:29px; }
  .panel { padding:22px 20px; }
  .moon { width:62px; height:62px; top:26px; right:26px; }
  .body { font-size:16px; }
}
</style>
</head>
<body>
<canvas id="sky"></canvas>
<div class="moon"></div>

<div class="wrap">
  <header>
    <div class="eyebrow">오늘의 __KIND__ 묵상 · __DATE__</div>
    <h1>__TITLE__</h1>
    <div class="rule"></div>
    <div class="src">__SOURCE__</div>
    <div class="cit">유란시아서 __CITATION__</div>
  </header>

  <div class="tabs" id="tabs"></div>
  <div class="panel">
    <div class="label" id="label"></div>
    <div class="body" id="body"></div>
  </div>
  <div class="hint">스페이스 재생·멈춤 · 좌우 화살표 이동</div>
</div>

<div class="bar">
  <div class="barin">
    <div class="prog" id="prog"><div class="progin" id="progin"></div></div>
    <div class="ctrls">
      <button class="btn" id="prev">◀ 이전</button>
      <button class="btn play" id="play">▶ 재생</button>
      <button class="btn" id="next">건너뛰기 ▶</button>
      <span class="time" id="time">0:00 / 0:00</span>
      <button class="btn" id="loop">🔁 전체 반복</button>
      <button class="btn" id="mute">🔊</button>
    </div>
  </div>
</div>

<div class="gate" id="gate">
  <div class="in">
    <h2>__TITLE__</h2>
    <p>낭독 · 강론 · 노래 · 기도가<br>차례로 이어서 재생됩니다.</p>
    <button id="start">묵상 시작하기</button>
  </div>
</div>

<audio id="au"></audio>

<script>
var DATA = __DATA__;

var SEGS = [
  { key:"01_reading", label:"낭독", get:function(){ return readingHtml(); } },
  { key:"02_sermon",  label:"강론", get:function(){ return esc(DATA.sermon); } },
  { key:"03_song",    label:"노래", get:function(){ return songHtml(); } },
  { key:"04_prayer",  label:"기도", get:function(){ return esc(DATA.prayer); } }
];

var LOOPS = ["off", "all", "one"];
var LOOPTXT = { off:"🔁 반복 없음", all:"🔁 전체 반복", one:"🔂 이 메뉴 반복" };

var cur = 0, loop = 1, started = false;
var au = document.getElementById("au");

function esc(s){
  return String(s == null ? "" : s)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}
function src(key){
  var base = DATA.audioBase || "audio/";
  if (base && base.charAt(base.length-1) !== "/") base += "/";
  return base + key + ".mp3";
}
function readingHtml(){
  return '<span class="tag">유란시아서 ' + esc(DATA.citation) + '</span>' + esc(DATA.reading);
}
function songHtml(){
  var out = '<div class="songtitle">' + esc(DATA.songTitle) + '</div>';
  var lines = String(DATA.song).split("\\n");
  for (var i = 0; i < lines.length; i++){
    var t = lines[i].trim();
    if (t.charAt(0) === "[" && t.charAt(t.length-1) === "]"){
      out += '<span class="tag">' + esc(t) + '</span>';
    } else {
      out += esc(lines[i]) + "\\n";
    }
  }
  return out;
}

function paint(){
  var tabs = document.getElementById("tabs");
  var html = "";
  for (var i = 0; i < SEGS.length; i++){
    html += '<button class="tab' + (i === cur ? " on" : "") + '" data-i="' + i + '">'
          + SEGS[i].label + '</button>';
  }
  tabs.innerHTML = html;
  document.getElementById("label").textContent = SEGS[cur].label;
  var b = document.getElementById("body");
  b.className = "body" + (cur === 0 ? " verse" : "");
  b.innerHTML = SEGS[cur].get();
}

function load(i, autoplay, depth){
  depth = depth || 0;
  if (depth >= 3) { pause(); return; }
  cur = (i + SEGS.length) % SEGS.length;
  paint();
  au.src = src(SEGS[cur].key);
  au.load();
  if (autoplay){
    var p = au.play();
    if (p && p.catch) p.catch(function(){ load(cur + 1, true, depth + 1); });
  }
}

function pause(){
  au.pause();
  document.getElementById("play").textContent = "▶ 재생";
}

document.getElementById("play").addEventListener("click", function(){
  if (au.paused){
    au.play();
    this.textContent = "⏸ 멈춤";
  } else {
    pause();
  }
});
document.getElementById("next").addEventListener("click", function(){ load(cur + 1, true); });
document.getElementById("prev").addEventListener("click", function(){ load(cur - 1, true); });

document.getElementById("tabs").addEventListener("click", function(e){
  var t = e.target.getAttribute("data-i");
  if (t !== null) load(parseInt(t, 10), true);
});

document.getElementById("loop").addEventListener("click", function(){
  loop = (loop + 1) % 3;
  this.textContent = LOOPTXT[LOOPS[loop]];
  this.className = "btn" + (loop === 0 ? "" : " on");
});

document.getElementById("mute").addEventListener("click", function(){
  au.muted = !au.muted;
  this.textContent = au.muted ? "🔇" : "🔊";
});

au.addEventListener("ended", function(){
  var mode = LOOPS[loop];
  if (mode === "one"){ load(cur, true); return; }
  if (cur === SEGS.length - 1 && mode === "off"){ pause(); return; }
  load(cur + 1, true);
});
au.addEventListener("error", function(){
  if (!started) return;
  load(cur + 1, true, 1);
});
au.addEventListener("play", function(){
  document.getElementById("play").textContent = "⏸ 멈춤";
});

function fmt(s){
  if (!isFinite(s)) return "0:00";
  var m = Math.floor(s / 60), r = Math.floor(s % 60);
  return m + ":" + (r < 10 ? "0" : "") + r;
}
au.addEventListener("timeupdate", function(){
  var d = au.duration || 0;
  document.getElementById("progin").style.width = (d ? (au.currentTime / d * 100) : 0) + "%";
  document.getElementById("time").textContent = fmt(au.currentTime) + " / " + fmt(d);
});
document.getElementById("prog").addEventListener("click", function(e){
  var r = this.getBoundingClientRect();
  if (au.duration) au.currentTime = (e.clientX - r.left) / r.width * au.duration;
});

document.addEventListener("keydown", function(e){
  if (e.code === "Space"){ e.preventDefault(); document.getElementById("play").click(); }
  if (e.code === "ArrowRight") load(cur + 1, true);
  if (e.code === "ArrowLeft") load(cur - 1, true);
});

document.getElementById("start").addEventListener("click", function(){
  document.getElementById("gate").style.display = "none";
  started = true;
  load(0, true);
});

/* 밤하늘 */
(function(){
  var cv = document.getElementById("sky");
  if (!cv || !cv.getContext) return;
  var ctx = cv.getContext("2d");
  function draw(){
    var w = cv.width = window.innerWidth, h = cv.height = window.innerHeight;
    ctx.clearRect(0, 0, w, h);
    var mx = w - 56 - 43, my = 46 + 43;
    for (var i = 0; i < 150; i++){
      var x = Math.random() * w, y = Math.random() * h;
      if (Math.sqrt((x - mx) * (x - mx) + (y - my) * (y - my)) < 150) continue;
      var r = Math.random() * 1.4 + 0.25;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(255,255,255," + (Math.random() * 0.72 + 0.12) + ")";
      ctx.fill();
    }
  }
  draw();
  window.addEventListener("resize", draw);
})();

paint();
document.getElementById("loop").textContent = LOOPTXT[LOOPS[loop]];
document.getElementById("loop").className = "btn on";
</script>
</body>
</html>
"""


def build():
    html = TPL
    html = html.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
    for k, v in [
        ("__KIND__", C.KIND),
        ("__DATE__", C.DATE),
        ("__TITLE__", C.TITLE),
        ("__SOURCE__", C.SOURCE),
        ("__CITATION__", C.CITATION),
    ]:
        html = html.replace(k, v)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html 을 만들었습니다. (%d자)" % len(html))


if __name__ == "__main__":
    build()

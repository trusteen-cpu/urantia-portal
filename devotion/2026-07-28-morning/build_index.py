# -*- coding: utf-8 -*-
"""
content.py 의 원고를 그대로 읽어 index.html 을 생성합니다.
원고를 고쳤으면  python build_index.py  를 다시 실행하세요.
(화면 글과 음성 원고가 100% 일치하도록 보장합니다)
"""

import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C

BASE = os.path.dirname(os.path.abspath(__file__))


def js(s):
    return json.dumps(s, ensure_ascii=False)


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>오늘의 __KIND__ 묵상 __DATE__ · __TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{
  --gold:#e7c163;
  --gold-soft:#f2dca4;
  --ink:#fdf6e6;
  --ink-dim:rgba(253,246,230,.72);
  --panel:rgba(255,255,255,.07);
  --panel-line:rgba(231,193,99,.30);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0;height:100%}
body{
  font-family:'Noto Serif KR',serif;
  color:var(--ink);
  background:linear-gradient(180deg,#1b2547 0%,#2c3159 32%,#6b5470 62%,#c98f5c 84%,#f0b96e 100%);
  background-attachment:fixed;
  min-height:100%;
  overflow-x:hidden;
}
#sky{position:fixed;inset:0;z-index:0;pointer-events:none}
#sun{
  position:fixed;right:-90px;bottom:-140px;width:420px;height:420px;border-radius:50%;
  background:radial-gradient(circle at 50% 50%,rgba(255,226,160,.95) 0%,rgba(255,198,110,.55) 38%,rgba(255,180,90,.18) 62%,rgba(255,180,90,0) 74%);
  z-index:0;pointer-events:none;filter:blur(1px);
}
.wrap{position:relative;z-index:2;max-width:760px;margin:0 auto;padding:26px 20px 120px}

header{text-align:center;padding:18px 0 8px}
.eyebrow{font-family:'Noto Sans KR',sans-serif;font-size:12.5px;letter-spacing:.34em;color:var(--gold);font-weight:500}
h1{font-size:29px;margin:12px 0 6px;font-weight:700;letter-spacing:-.01em}
.date{font-family:'Noto Sans KR',sans-serif;font-size:13.5px;color:var(--ink-dim);letter-spacing:.06em}
.cite{margin-top:14px;display:inline-block;padding:6px 15px;border:1px solid var(--panel-line);border-radius:999px;
  font-family:'Noto Sans KR',sans-serif;font-size:12.5px;color:var(--gold-soft);letter-spacing:.04em}
.source{margin-top:9px;font-family:'Noto Sans KR',sans-serif;font-size:12px;color:var(--ink-dim)}
.rule{width:64px;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:20px auto 6px}

nav.menu{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:22px 0 20px}
nav.menu button{
  font-family:'Noto Sans KR',sans-serif;font-size:13.5px;font-weight:500;
  padding:9px 20px;border-radius:999px;cursor:pointer;
  border:1px solid var(--panel-line);background:var(--panel);color:var(--ink-dim);
  transition:.22s;
}
nav.menu button:hover{color:var(--ink);border-color:var(--gold)}
nav.menu button.on{background:var(--gold);border-color:var(--gold);color:#2a2033;font-weight:700}
nav.menu button.missing{opacity:.42}

section.pane{display:none;animation:fade .5s ease}
section.pane.on{display:block}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

.card{
  background:var(--panel);border:1px solid var(--panel-line);border-radius:18px;
  padding:30px 26px;backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);
  box-shadow:0 10px 34px rgba(20,18,40,.22);
}
.label{font-family:'Noto Sans KR',sans-serif;font-size:11.5px;letter-spacing:.3em;color:var(--gold);margin-bottom:16px;font-weight:500}
.body{font-size:18.5px;line-height:2.06;white-space:pre-wrap;word-break:keep-all}
.body.reading{font-size:19.5px;line-height:2.12}
.body.prayer{text-align:center;line-height:2.16}
.body.song{text-align:center;line-height:2.14;font-size:18px}
.songtitle{text-align:center;font-size:20px;color:var(--gold-soft);margin-bottom:18px;font-weight:700}
.note{margin-top:18px;font-family:'Noto Sans KR',sans-serif;font-size:12.5px;color:var(--ink-dim);text-align:center}

.player{
  position:fixed;left:0;right:0;bottom:0;z-index:9;
  background:linear-gradient(180deg,rgba(24,26,52,.55),rgba(24,26,52,.90));
  border-top:1px solid var(--panel-line);
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
  padding:12px 16px calc(14px + env(safe-area-inset-bottom));
}
.pbar{height:5px;border-radius:99px;background:rgba(255,255,255,.16);cursor:pointer;overflow:hidden}
.pfill{height:100%;width:0;background:linear-gradient(90deg,var(--gold),var(--gold-soft));border-radius:99px}
.ctrls{display:flex;align-items:center;gap:10px;justify-content:center;margin-top:11px;max-width:760px;margin-left:auto;margin-right:auto}
.ctrls .now{font-family:'Noto Sans KR',sans-serif;font-size:12px;color:var(--ink-dim);min-width:92px}
.ctrls .time{font-family:'Noto Sans KR',sans-serif;font-size:11.5px;color:var(--ink-dim);min-width:82px;text-align:right}
.btn{
  border:1px solid var(--panel-line);background:rgba(255,255,255,.08);color:var(--ink);
  width:40px;height:40px;border-radius:50%;cursor:pointer;font-size:15px;display:flex;align-items:center;justify-content:center;
  transition:.2s;position:relative;flex:0 0 auto;
}
.btn:hover{border-color:var(--gold);color:var(--gold-soft)}
.btn.play{width:50px;height:50px;background:var(--gold);border-color:var(--gold);color:#2a2033;font-size:18px}
.btn.act{border-color:var(--gold);color:var(--gold)}
.badge{position:absolute;top:-4px;right:-4px;background:var(--gold);color:#2a2033;font-family:'Noto Sans KR',sans-serif;
  font-size:9.5px;font-weight:700;border-radius:99px;padding:1px 5px;line-height:1.4}

#gate{position:fixed;inset:0;z-index:50;background:rgba(16,18,40,.92);display:flex;align-items:center;justify-content:center;
  backdrop-filter:blur(4px);text-align:center;padding:24px}
#gate .inner{max-width:420px}
#gate h2{font-size:23px;margin:0 0 12px}
#gate p{font-family:'Noto Sans KR',sans-serif;font-size:14px;color:var(--ink-dim);line-height:1.9;margin:0 0 26px}
#gate button{font-family:'Noto Sans KR',sans-serif;font-size:15px;font-weight:700;padding:14px 34px;border-radius:999px;
  border:none;background:var(--gold);color:#2a2033;cursor:pointer}
footer{text-align:center;font-family:'Noto Sans KR',sans-serif;font-size:11.5px;color:var(--ink-dim);margin-top:26px;line-height:1.9}
@media(max-width:520px){
  h1{font-size:24px}
  .card{padding:24px 19px;border-radius:15px}
  .body{font-size:17px;line-height:1.98}
  .body.reading{font-size:17.5px}
  .ctrls .now,.ctrls .time{display:none}
}
</style>
</head>
<body>
<canvas id="sky"></canvas>
<div id="sun"></div>

<div class="wrap">
  <header>
    <div class="eyebrow">URANTIA CORE TRUTH</div>
    <h1>오늘의 __KIND__ 묵상</h1>
    <div class="date">__DATE_KO__</div>
    <div class="rule"></div>
    <div class="cite">유란시아서 __CITATION__</div>
    <div class="source">__SOURCE__</div>
    <div style="margin-top:16px;font-size:20px;color:var(--gold-soft);font-weight:700">__TITLE__</div>
  </header>

  <nav class="menu" id="menu"></nav>

  <section class="pane" id="pane-reading">
    <div class="card"><div class="label">낭 독</div><div class="body reading" id="t-reading"></div></div>
  </section>
  <section class="pane" id="pane-sermon">
    <div class="card"><div class="label">강 론</div><div class="body" id="t-sermon"></div></div>
  </section>
  <section class="pane" id="pane-song">
    <div class="card"><div class="label">노 래</div>
      <div class="songtitle">__SONG_TITLE__</div>
      <div class="body song" id="t-song"></div>
      <div class="note" id="song-note" style="display:none">audio/03_song.mp3 가 아직 없어 노래는 자동으로 건너뜁니다.</div>
    </div>
  </section>
  <section class="pane" id="pane-prayer">
    <div class="card"><div class="label">기 도</div><div class="body prayer" id="t-prayer"></div></div>
  </section>

  <footer>Urantia Core Truth · 오늘의 묵상<br>한국 유란시아 독자회</footer>
</div>

<div class="player">
  <div class="pbar" id="pbar"><div class="pfill" id="pfill"></div></div>
  <div class="ctrls">
    <div class="now" id="now">낭독</div>
    <button class="btn" id="prev" title="이전 (←)">&#9198;</button>
    <button class="btn play" id="play" title="재생 / 일시정지 (스페이스)">&#9654;</button>
    <button class="btn" id="next" title="다음 (→)">&#9197;</button>
    <button class="btn" id="rep" title="반복: 없음 → 전체 → 한 메뉴">&#8635;</button>
    <button class="btn" id="mute" title="음소거">&#128266;</button>
    <div class="time" id="time">0:00 / 0:00</div>
  </div>
</div>

<div id="gate"><div class="inner">
  <h2>오늘의 __KIND__ 묵상</h2>
  <p>낭독 → 강론 → 노래 → 기도<br>순서대로 자동으로 이어집니다.</p>
  <button id="start">시작하기</button>
</div></div>

<audio id="au" preload="none"></audio>

<script>
var DATA = [
  {id:"reading", label:"낭독", file:"audio/01_reading.mp3", text:__T_READING__},
  {id:"sermon",  label:"강론", file:"audio/02_sermon.mp3",  text:__T_SERMON__},
  {id:"song",    label:"노래", file:"audio/03_song.mp3",    text:__T_SONG__},
  {id:"prayer",  label:"기도", file:"audio/04_prayer.mp3",  text:__T_PRAYER__}
];

/* 본문 채우기 */
for(var i=0;i<DATA.length;i++){
  document.getElementById("t-"+DATA[i].id).textContent = DATA[i].text;
}

var au   = document.getElementById("au");
var menu = document.getElementById("menu");
var idx  = 0;
var repeatMode = 1;           /* 0 없음 · 1 전체 · 2 한 메뉴 */
var missing = {};             /* 파일 없는 구간 */
var started = false;

/* 메뉴 만들기 */
var btns = [];
DATA.forEach(function(seg,i){
  var b = document.createElement("button");
  b.textContent = seg.label;
  b.onclick = function(){ go(i, started); };
  menu.appendChild(b);
  btns.push(b);
});

function paint(){
  DATA.forEach(function(seg,i){
    btns[i].className = (i===idx? "on":"") + (missing[seg.id]? " missing":"");
    var p = document.getElementById("pane-"+seg.id);
    if(i===idx){ p.classList.add("on"); } else { p.classList.remove("on"); }
  });
  document.getElementById("now").textContent = DATA[idx].label;
  window.scrollTo({top:0,behavior:"smooth"});
}

function go(i, autoplay){
  idx = (i + DATA.length) % DATA.length;
  paint();
  au.src = DATA[idx].file;
  au.load();
  if(autoplay){
    var pr = au.play();
    if(pr && pr.catch){ pr.catch(function(){}); }
  }
}

/* 다음 구간 (반복 모드 반영) */
function advance(){
  if(repeatMode===2){ au.currentTime=0; au.play(); return; }
  var n = idx + 1;
  if(n >= DATA.length){
    if(repeatMode===1){ n = 0; }
    else { au.pause(); setPlayIcon(false); return; }
  }
  go(n, true);
}

/* 파일이 없으면 자동 건너뛰기 */
var skipGuard = 0;
au.addEventListener("error", function(){
  missing[DATA[idx].id] = true;
  if(DATA[idx].id==="song"){ document.getElementById("song-note").style.display="block"; }
  paint();
  skipGuard++;
  if(skipGuard >= DATA.length){ au.pause(); setPlayIcon(false); skipGuard=0; return; }
  if(started){ setTimeout(function(){ advance(); }, 250); }
});
au.addEventListener("playing", function(){ skipGuard = 0; });
au.addEventListener("ended", advance);

/* 재생 버튼 */
var playBtn = document.getElementById("play");
function setPlayIcon(playing){
  playBtn.innerHTML = playing ? "&#10074;&#10074;" : "&#9654;";
}
playBtn.onclick = function(){
  if(au.paused){ started = true; au.play(); } else { au.pause(); }
};
au.addEventListener("play",  function(){ setPlayIcon(true);  started = true; });
au.addEventListener("pause", function(){ setPlayIcon(false); });

/* 건너뛰기 */
document.getElementById("next").onclick = function(){ go(idx+1, true); };
document.getElementById("prev").onclick = function(){
  if(au.currentTime > 3){ au.currentTime = 0; return; }
  go(idx-1, true);
};

/* 반복 3단 토글 */
var repBtn = document.getElementById("rep");
function paintRep(){
  repBtn.innerHTML = "&#8635;";
  repBtn.className = "btn" + (repeatMode? " act":"");
  if(repeatMode===2){
    var s = document.createElement("span");
    s.className = "badge"; s.textContent = "1";
    repBtn.appendChild(s);
  }
  repBtn.title = ["반복 없음","전체 무한 반복","한 메뉴 무한 반복"][repeatMode];
}
repBtn.onclick = function(){ repeatMode = (repeatMode+1)%3; paintRep(); };
paintRep();

/* 음소거 */
var muteBtn = document.getElementById("mute");
muteBtn.onclick = function(){
  au.muted = !au.muted;
  muteBtn.innerHTML = au.muted ? "&#128263;" : "&#128266;";
  muteBtn.className = "btn" + (au.muted? " act":"");
};

/* 진행바 */
var pbar = document.getElementById("pbar"), pfill = document.getElementById("pfill");
function fmt(t){
  if(!isFinite(t)||isNaN(t)) return "0:00";
  var m = Math.floor(t/60), s = Math.floor(t%60);
  return m + ":" + (s<10? "0":"") + s;
}
au.addEventListener("timeupdate", function(){
  var d = au.duration || 0;
  pfill.style.width = (d? (au.currentTime/d*100):0) + "%";
  document.getElementById("time").textContent = fmt(au.currentTime) + " / " + fmt(d);
});
pbar.onclick = function(e){
  var d = au.duration;
  if(!d) return;
  var r = pbar.getBoundingClientRect();
  au.currentTime = (e.clientX - r.left) / r.width * d;
};

/* 키보드 */
document.addEventListener("keydown", function(e){
  if(e.code==="Space"){ e.preventDefault(); playBtn.onclick(); }
  if(e.code==="ArrowRight"){ go(idx+1,true); }
  if(e.code==="ArrowLeft"){ document.getElementById("prev").onclick(); }
});

/* 시작 오버레이 */
document.getElementById("start").onclick = function(){
  document.getElementById("gate").style.display = "none";
  started = true;
  go(0, true);
};

/* 새벽 별 */
(function(){
  var c = document.getElementById("sky"), x = c.getContext("2d"), stars = [];
  function size(){
    c.width = innerWidth; c.height = innerHeight;
    stars = [];
    for(var i=0;i<70;i++){
      stars.push({
        x: Math.random()*c.width,
        y: Math.random()*c.height*0.55,
        r: Math.random()*1.25+0.3,
        a: Math.random()*0.5+0.15,
        s: Math.random()*0.012+0.003
      });
    }
  }
  function tick(){
    x.clearRect(0,0,c.width,c.height);
    for(var i=0;i<stars.length;i++){
      var st = stars[i];
      st.a += st.s;
      if(st.a>0.68 || st.a<0.10) st.s *= -1;
      var fade = 1 - (st.y/(c.height*0.62));
      x.beginPath();
      x.arc(st.x, st.y, st.r, 0, 6.2832);
      x.fillStyle = "rgba(255,246,214," + (st.a*Math.max(fade,0)) + ")";
      x.fill();
    }
    requestAnimationFrame(tick);
  }
  size(); tick();
  addEventListener("resize", size);
})();

paint();
</script>
</body>
</html>
"""


def main():
    html = TEMPLATE
    d = C.DATE.split("-")
    date_ko = "%s년 %s월 %s일" % (d[0], int(d[1]), int(d[2]))
    reps = {
        "__KIND__": C.KIND,
        "__DATE_KO__": date_ko,
        "__DATE__": C.DATE,
        "__TITLE__": C.TITLE,
        "__CITATION__": C.CITATION,
        "__SOURCE__": C.SOURCE,
        "__SONG_TITLE__": "「%s」" % C.SONG_TITLE,
        "__T_READING__": js(C.READING),
        "__T_SERMON__": js(C.SERMON),
        "__T_SONG__": js(C.SONG),
        "__T_PRAYER__": js(C.PRAYER),
    }
    for k, v in reps.items():
        html = html.replace(k, v)
    out = os.path.join(BASE, "index.html")
    io.open(out, "w", encoding="utf-8").write(html)
    print("index.html 생성 완료 (%d bytes)" % os.path.getsize(out))


if __name__ == "__main__":
    main()

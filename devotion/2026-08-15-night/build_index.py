# -*- coding: utf-8 -*-
"""content.py 를 읽어 index.html 을 만듭니다 (밤하늘 취침 테마).

    python build_index.py
"""

import json
import content as C

DATA = {
    "date": C.DATE,
    "kind": C.KIND,
    "title": C.TITLE,
    "source": C.SOURCE,
    "citation": C.CITATION,
    "reading": C.READING,
    "sermon": C.SERMON,
    "songTitle": C.SONG_TITLE,
    "songLyrics": C.SONG_LYRICS,
    "prayer": C.PRAYER,
}

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>오늘의 __KIND__ 묵상 __DATE__ — __TITLE__</title>
<style>
:root{
  --gold:#e8c479; --ink:#f2f5fa; --dim:#b9c4dc;
  --panel:rgba(18,26,51,.42); --line:rgba(232,196,121,.28);
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; color:var(--ink); overflow-x:hidden;
  font-family:"Noto Serif KR","Malgun Gothic","맑은 고딕",serif; line-height:1.85;
  background:linear-gradient(180deg,#0b1020 0%,#121a33 52%,#1c2647 100%);
  background-attachment:fixed;
}
.moon{
  position:fixed; top:64px; right:74px; width:86px; height:86px; border-radius:50%;
  background:radial-gradient(circle at 36% 34%,#fff6dd,#f0d79a 60%,#d9bd7a 100%);
  box-shadow:0 0 90px 34px rgba(240,215,154,.20), 0 0 220px 90px rgba(240,215,154,.10);
  pointer-events:none; z-index:0;
}
#stars{position:fixed; inset:0; pointer-events:none; z-index:0}
.star{position:absolute; background:#fff; border-radius:50%; animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.22}50%{opacity:.9}}
.wrap{position:relative; z-index:1; max-width:760px; margin:0 auto; padding:34px 22px 70px}
header{text-align:center; margin-bottom:26px}
header .k{font-size:12.5px; letter-spacing:.32em; color:var(--gold); margin-bottom:9px}
header h1{margin:0 0 8px; font-size:27px; font-weight:700; letter-spacing:-.4px}
header .src{font-size:13px; color:var(--dim)}
header .rule{width:66px; height:2px; background:var(--gold); opacity:.75; margin:15px auto 0}
.tabs{display:flex; gap:8px; justify-content:center; margin:24px 0 16px; flex-wrap:wrap}
.tabs button{
  background:transparent; border:1px solid var(--line); color:var(--dim);
  border-radius:19px; padding:7px 17px; font-size:13.5px; font-family:inherit; cursor:pointer;
  transition:.15s;
}
.tabs button:hover{color:var(--ink); border-color:var(--gold)}
.tabs button.on{background:var(--gold); border-color:var(--gold); color:#1a1408; font-weight:700}
.panel{
  background:var(--panel); border:1px solid var(--line); border-radius:14px;
  padding:26px 24px; backdrop-filter:blur(2px); min-height:230px;
}
.panel .cite{font-size:12.5px; color:var(--gold); letter-spacing:.06em; margin-bottom:13px}
.panel p{margin:0 0 15px; font-size:16.5px}
.panel p:last-child{margin-bottom:0}
.panel .lyr{white-space:pre-wrap; font-size:16px}
.panel .tag{color:var(--gold); font-size:13.5px; letter-spacing:.08em}
.panel .pray{white-space:pre-wrap; font-size:16.5px; text-align:center; line-height:2.05}
.bar{margin-top:20px; display:flex; align-items:center; gap:11px; flex-wrap:wrap}
.bar button{
  background:rgba(255,255,255,.07); border:1px solid var(--line); color:var(--ink);
  border-radius:17px; padding:7px 15px; font-size:13px; font-family:inherit; cursor:pointer;
}
.bar button:hover{background:rgba(232,196,121,.16)}
.prog{flex:1; min-width:150px; height:5px; background:rgba(255,255,255,.13); border-radius:3px; cursor:pointer}
.prog i{display:block; height:100%; width:0; background:var(--gold); border-radius:3px}
.time{font-size:12px; color:var(--dim); font-variant-numeric:tabular-nums; white-space:nowrap}
.hint{margin-top:15px; font-size:12.5px; color:var(--dim); text-align:center; line-height:1.9}
#overlay{
  position:fixed; inset:0; z-index:9; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:17px; text-align:center; padding:26px;
  background:rgba(8,12,26,.90); backdrop-filter:blur(3px);
}
#overlay h2{margin:0; font-size:22px; font-weight:700}
#overlay p{margin:0; font-size:14px; color:var(--dim)}
#overlay button{
  margin-top:9px; background:var(--gold); border:0; color:#1a1408; font-weight:700;
  border-radius:24px; padding:13px 34px; font-size:15.5px; font-family:inherit; cursor:pointer;
}
@media(max-width:600px){
  .moon{width:62px; height:62px; top:44px; right:26px}
  header h1{font-size:23px}
  .wrap{padding:26px 15px 56px}
  .panel{padding:20px 16px}
  .panel p,.panel .pray{font-size:15.5px}
}
</style>
</head>
<body>
<div class="moon"></div>
<div id="stars"></div>

<div class="wrap">
  <header>
    <div class="k">오늘의 __KIND__ 묵상 · __DATE__</div>
    <h1 id="ttl"></h1>
    <div class="src" id="src"></div>
    <div class="rule"></div>
  </header>

  <div class="tabs" id="tabs"></div>

  <div class="panel" id="panel"></div>

  <div class="bar">
    <button id="play">❚❚ 멈춤</button>
    <button id="prev">◀ 이전</button>
    <button id="next">다음 ▶</button>
    <div class="prog" id="prog"><i id="fill"></i></div>
    <span class="time" id="time">0:00 / 0:00</span>
    <button id="rep">반복: 전체</button>
    <button id="mute">🔊</button>
  </div>

  <div class="hint">
    낭독 → 강론 → 노래 → 기도 순으로 저절로 이어집니다.<br>
    스페이스바는 멈춤과 재생, 좌우 화살표는 앞뒤 이동입니다.
  </div>
</div>

<div id="overlay">
  <h2>오늘의 __KIND__ 묵상</h2>
  <p>__DATE__ · __TITLE__</p>
  <button id="start">묵상 시작하기</button>
</div>

<audio id="au"></audio>

<script>
var DATA = __DATA__;

/* 별 */
(function(){
  var box = document.getElementById('stars'), html = '';
  for (var i = 0; i < 150; i++) {
    var x = Math.random() * 100, y = Math.random() * 100,
        s = Math.random() * 1.9 + 0.6, d = (Math.random() * 4).toFixed(2);
    html += '<span class="star" style="left:' + x.toFixed(2) + '%;top:' + y.toFixed(2) +
            '%;width:' + s.toFixed(2) + 'px;height:' + s.toFixed(2) +
            'px;animation-delay:' + d + 's"></span>';
  }
  box.innerHTML = html;
})();

var SEGS = [
  { key:'reading', name:'낭독', file:'audio/01_reading.mp3' },
  { key:'sermon',  name:'강론', file:'audio/02_sermon.mp3'  },
  { key:'song',    name:'노래', file:'audio/03_song.mp3'    },
  { key:'prayer',  name:'기도', file:'audio/04_prayer.mp3'  }
];

var au = document.getElementById('au'),
    panel = document.getElementById('panel'),
    tabs = document.getElementById('tabs'),
    fill = document.getElementById('fill'),
    timeEl = document.getElementById('time'),
    playBtn = document.getElementById('play'),
    repBtn = document.getElementById('rep'),
    muteBtn = document.getElementById('mute'),
    cur = 0, repMode = 0, started = false;   /* 0 전체반복 1 한메뉴반복 2 안함 */

document.getElementById('ttl').textContent = DATA.title;
document.getElementById('src').textContent = DATA.source + ' · ' + DATA.citation;

SEGS.forEach(function(s, i){
  var b = document.createElement('button');
  b.textContent = s.name;
  b.onclick = function(){ go(i, true); };
  tabs.appendChild(b);
});

function paras(t){
  return t.split(/\\n\\s*\\n/).map(function(p){
    return '<p>' + p.replace(/\\n/g, '<br>') + '</p>';
  }).join('');
}

function lyricsHtml(t){
  return '<div class="lyr">' + t.split('\\n').map(function(l){
    return /^\\s*\\[.*\\]\\s*$/.test(l) ? '<span class="tag">' + l + '</span>' : l;
  }).join('\\n') + '</div>';
}

function render(){
  var s = SEGS[cur], h = '';
  if (s.key === 'reading') {
    h = '<div class="cite">' + DATA.citation + '</div>' + paras(DATA.reading);
  } else if (s.key === 'sermon') {
    h = paras(DATA.sermon);
  } else if (s.key === 'song') {
    h = '<div class="cite">' + DATA.songTitle + '</div>' + lyricsHtml(DATA.songLyrics);
  } else {
    h = '<div class="pray">' + DATA.prayer + '</div>';
  }
  panel.innerHTML = h;
  [].forEach.call(tabs.children, function(b, i){ b.className = (i === cur ? 'on' : ''); });
}

function load(i, play, depth){
  depth = depth || 0;
  cur = (i + SEGS.length) % SEGS.length;
  render();
  au.src = SEGS[cur].file;
  au.onerror = function(){
    if (depth >= 3) { playBtn.textContent = '▶ 재생'; return; }
    load(cur + 1, play, depth + 1);
  };
  if (play) {
    var p = au.play();
    if (p && p.catch) p.catch(function(){ playBtn.textContent = '▶ 재생'; });
    playBtn.textContent = '❚❚ 멈춤';
  }
}

function go(i, play){ load(i, play === undefined ? started : play, 0); }

au.addEventListener('ended', function(){
  if (repMode === 1) { load(cur, true, 0); return; }
  if (cur === SEGS.length - 1 && repMode === 2) { playBtn.textContent = '▶ 재생'; return; }
  load(cur + 1, true, 0);
});

au.addEventListener('timeupdate', function(){
  var d = au.duration || 0, t = au.currentTime || 0;
  fill.style.width = (d ? (t / d * 100) : 0) + '%';
  timeEl.textContent = fmt(t) + ' / ' + fmt(d);
});

function fmt(s){
  if (!isFinite(s)) return '0:00';
  var m = Math.floor(s / 60), x = Math.floor(s % 60);
  return m + ':' + (x < 10 ? '0' : '') + x;
}

playBtn.onclick = function(){
  if (au.paused) { au.play(); playBtn.textContent = '❚❚ 멈춤'; }
  else { au.pause(); playBtn.textContent = '▶ 재생'; }
};
document.getElementById('prev').onclick = function(){ load(cur - 1, true, 0); };
document.getElementById('next').onclick = function(){ load(cur + 1, true, 0); };
document.getElementById('prog').onclick = function(e){
  var r = this.getBoundingClientRect();
  if (au.duration) au.currentTime = (e.clientX - r.left) / r.width * au.duration;
};
repBtn.onclick = function(){
  repMode = (repMode + 1) % 3;
  repBtn.textContent = '반복: ' + ['전체', '한 메뉴', '안 함'][repMode];
};
muteBtn.onclick = function(){
  au.muted = !au.muted;
  muteBtn.textContent = au.muted ? '🔇' : '🔊';
};
document.addEventListener('keydown', function(e){
  if (e.key === ' ') { e.preventDefault(); playBtn.click(); }
  if (e.key === 'ArrowLeft') load(cur - 1, true, 0);
  if (e.key === 'ArrowRight') load(cur + 1, true, 0);
});

document.getElementById('start').onclick = function(){
  started = true;
  document.getElementById('overlay').style.display = 'none';
  load(0, true, 0);
};

render();
</script>
</body>
</html>
"""


def main():
    html = (HTML
            .replace("__DATA__", json.dumps(DATA, ensure_ascii=False, indent=2))
            .replace("__KIND__", C.KIND)
            .replace("__DATE__", C.DATE)
            .replace("__TITLE__", C.TITLE))
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html 만들었습니다. (%d자)" % len(html))


if __name__ == "__main__":
    main()

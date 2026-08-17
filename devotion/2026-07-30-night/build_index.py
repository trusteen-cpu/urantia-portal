# -*- coding: utf-8 -*-
"""content.py 의 원고로 index.html 을 만든다.

실행:  python build_index.py
원고를 고쳤으면 이 파일을 다시 실행하면 재생기 화면도 함께 바뀝니다.
"""

import json
import content as C

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>오늘의 __KIND__ 묵상 __DATE__ · __TITLE__</title>
<style>
:root{
  --gold:#e8c479;
  --gold-dim:#b99a5c;
  --ink:#eef2ff;
  --sub:#a9b4d0;
  --panel:rgba(255,255,255,.055);
  --line:rgba(232,196,121,.28);
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0;height:100%}
body{
  font-family:'Noto Serif KR','Nanum Myeongjo',serif;
  color:var(--ink);
  background:linear-gradient(180deg,#0b1020 0%,#121a33 55%,#1c2647 100%);
  min-height:100%;
}
#sky{position:fixed;inset:0;z-index:0}
.moon{
  position:fixed;top:38px;right:42px;width:86px;height:86px;border-radius:50%;
  background:radial-gradient(circle at 35% 35%,#fff7e0,#f0d79b 60%,#d9bb78);
  box-shadow:0 0 60px 18px rgba(240,215,155,.20),0 0 140px 60px rgba(240,215,155,.10);
  z-index:0;
}
.wrap{position:relative;z-index:2;max-width:760px;margin:0 auto;padding:28px 20px 60px}
header{text-align:center;padding:18px 0 6px}
.kicker{color:var(--gold);letter-spacing:.32em;font-size:12px;margin-bottom:10px}
h1{margin:0;font-size:30px;letter-spacing:-.01em}
.cite{margin-top:10px;color:var(--sub);font-size:14px}
.cite b{color:var(--gold-dim);font-weight:600}
.rule{height:1px;background:linear-gradient(90deg,transparent,var(--line),transparent);margin:20px 0 24px}

.tabs{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:18px}
.tab{
  border:1px solid var(--line);background:transparent;color:var(--sub);
  padding:8px 16px;border-radius:999px;font-size:14px;cursor:pointer;
  font-family:inherit;transition:.2s;
}
.tab:hover{color:var(--ink)}
.tab.on{background:rgba(232,196,121,.14);color:var(--gold);border-color:var(--gold-dim)}

.card{background:var(--panel);border:1px solid rgba(255,255,255,.07);border-radius:18px;padding:26px 24px}
.label{color:var(--gold);font-size:13px;letter-spacing:.2em;margin-bottom:14px}
.text{white-space:pre-wrap;line-height:2.0;font-size:17.5px;color:#e9edfb}
.text.song{line-height:1.95}
.text .tag{color:var(--gold);display:block;margin-top:14px}

.player{
  position:sticky;bottom:0;margin-top:22px;
  background:rgba(11,16,32,.82);backdrop-filter:blur(10px);
  border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:16px 18px;
}
.bar{height:6px;border-radius:6px;background:rgba(255,255,255,.12);cursor:pointer;overflow:hidden}
.bar > i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--gold-dim),var(--gold))}
.times{display:flex;justify-content:space-between;color:var(--sub);font-size:12px;margin-top:8px}
.ctrls{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:12px;flex-wrap:wrap}
.btn{
  border:1px solid var(--line);background:transparent;color:var(--ink);
  width:46px;height:46px;border-radius:50%;cursor:pointer;font-size:16px;font-family:inherit;
  display:flex;align-items:center;justify-content:center;transition:.2s;
}
.btn:hover{background:rgba(232,196,121,.12)}
.btn.play{width:58px;height:58px;background:rgba(232,196,121,.16);border-color:var(--gold-dim);color:var(--gold);font-size:20px}
.btn.on{background:rgba(232,196,121,.2);color:var(--gold);border-color:var(--gold)}
.btn .badge{position:absolute;font-size:9px;transform:translate(16px,-14px);color:var(--gold)}
.btn{position:relative}
.hint{text-align:center;color:var(--sub);font-size:12px;margin-top:10px;line-height:1.7}
.miss{color:#f0b96b;font-size:13px;margin-top:10px;text-align:center;display:none}

#overlay{
  position:fixed;inset:0;z-index:20;background:rgba(6,9,20,.90);
  display:flex;align-items:center;justify-content:center;flex-direction:column;gap:18px;cursor:pointer;
  text-align:center;padding:24px;
}
#overlay .o-title{color:var(--gold);font-size:22px;letter-spacing:.08em}
#overlay .o-sub{color:var(--sub);font-size:14px;line-height:1.9}
#overlay .o-btn{
  margin-top:6px;border:1px solid var(--gold-dim);color:var(--gold);
  background:rgba(232,196,121,.12);padding:14px 34px;border-radius:999px;font-size:16px;
  font-family:inherit;cursor:pointer;
}
footer{text-align:center;color:var(--sub);font-size:12px;margin-top:26px;line-height:1.9}
@media (max-width:520px){
  h1{font-size:24px}
  .text{font-size:16.5px;line-height:1.95}
  .moon{width:64px;height:64px;top:22px;right:22px}
  .card{padding:20px 16px}
}
</style>
</head>
<body>
<canvas id="sky"></canvas>
<div class="moon"></div>

<div class="wrap">
  <header>
    <div class="kicker">오늘의 __KIND__ 묵상</div>
    <h1>__TITLE__</h1>
    <div class="cite">__DATE__ · 유란시아서 <b>__CITATION__</b><br>__SOURCE__</div>
  </header>
  <div class="rule"></div>

  <div class="tabs" id="tabs"></div>

  <div class="card">
    <div class="label" id="label">낭독</div>
    <div class="text" id="text"></div>
  </div>

  <div class="player">
    <div class="bar" id="bar"><i id="fill"></i></div>
    <div class="times"><span id="cur">0:00</span><span id="dur">0:00</span></div>
    <div class="ctrls">
      <button class="btn" id="prev" title="이전 (←)">⏮</button>
      <button class="btn play" id="play" title="재생/일시정지 (space)">▶</button>
      <button class="btn" id="next" title="다음 (→)">⏭</button>
      <button class="btn" id="rep" title="반복 없음 → 전체 무한 → 한 메뉴 무한">↻</button>
      <button class="btn" id="mute" title="음소거">🔊</button>
    </div>
    <div class="miss" id="miss">노래 파일(audio/03_song.mp3)이 아직 없습니다 — 잠시 뒤 다음으로 넘어갑니다.</div>
    <div class="hint" id="hint">반복: 전체 무한 연속 · 스페이스 재생/정지 · ← → 건너뛰기</div>
  </div>

  <footer>유란시아 핵심 진리 · 오늘의 __KIND__ 묵상<br>낭독 → 강론 → 노래 → 기도</footer>
</div>

<div id="overlay">
  <div class="o-title">오늘의 __KIND__ 묵상</div>
  <div class="o-sub">__TITLE__ · 유란시아서 __CITATION__<br>화면을 누르면 낭독부터 자동으로 이어집니다.</div>
  <button class="o-btn" id="start">묵상 시작하기</button>
</div>

<script>
const DATA = __DATA__;

/* ── 밤하늘 별 ────────────────────────────── */
(function(){
  const cv = document.getElementById('sky'), ctx = cv.getContext('2d');
  let stars = [];
  function init(){
    cv.width = innerWidth; cv.height = innerHeight;
    stars = [];
    for(let i=0;i<150;i++){
      stars.push({
        x: Math.random()*cv.width,
        y: Math.random()*cv.height,
        r: Math.random()*1.3+0.3,
        a: Math.random(),
        s: Math.random()*0.012+0.003
      });
    }
  }
  function draw(){
    ctx.clearRect(0,0,cv.width,cv.height);
    for(const st of stars){
      st.a += st.s;
      const alpha = 0.35 + Math.abs(Math.sin(st.a))*0.55;
      ctx.beginPath();
      ctx.arc(st.x, st.y, st.r, 0, Math.PI*2);
      ctx.fillStyle = 'rgba(255,247,225,'+alpha.toFixed(3)+')';
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  init(); draw();
  addEventListener('resize', init);
})();

/* ── 재생기 ──────────────────────────────── */
const tabsEl = document.getElementById('tabs');
const labelEl = document.getElementById('label');
const textEl = document.getElementById('text');
const barEl = document.getElementById('bar');
const fillEl = document.getElementById('fill');
const curEl = document.getElementById('cur');
const durEl = document.getElementById('dur');
const playBtn = document.getElementById('play');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');
const repBtn = document.getElementById('rep');
const muteBtn = document.getElementById('mute');
const missEl = document.getElementById('miss');
const hintEl = document.getElementById('hint');

let idx = 0;
let repeat = 0;              // 0 없음 · 1 전체 무한 · 2 한 메뉴 무한
let skipTimer = null;
const audio = new Audio();
audio.preload = 'auto';

DATA.forEach((d,i)=>{
  const b = document.createElement('button');
  b.className = 'tab'; b.textContent = d.label;
  b.onclick = ()=>{ go(i, true); };
  tabsEl.appendChild(b);
});

function renderText(d){
  if(d.key === 'song'){
    textEl.className = 'text song';
    textEl.innerHTML = d.text.split('\n').map(l=>{
      const t = l.trim();
      if(t.startsWith('[')) return '<span class="tag">'+t+'</span>';
      return l.replace(/&/g,'&amp;').replace(/</g,'&lt;');
    }).join('\n');
  }else{
    textEl.className = 'text';
    textEl.textContent = d.text;
  }
}

function paint(){
  const d = DATA[idx];
  labelEl.textContent = d.label + (d.key==='song' ? ' — ' + d.songTitle : '');
  renderText(d);
  [...tabsEl.children].forEach((b,i)=> b.classList.toggle('on', i===idx));
  missEl.style.display = 'none';
  window.scrollTo({top:0, behavior:'smooth'});
}

function go(i, autoplay){
  if(skipTimer){ clearTimeout(skipTimer); skipTimer = null; }
  idx = (i + DATA.length) % DATA.length;
  paint();
  audio.src = DATA[idx].file;
  if(autoplay !== false){ audio.play().catch(()=>{}); }
}

function fmt(s){
  if(!isFinite(s)) return '0:00';
  s = Math.max(0, Math.floor(s));
  return Math.floor(s/60) + ':' + String(s%60).padStart(2,'0');
}

audio.addEventListener('timeupdate', ()=>{
  const p = audio.duration ? audio.currentTime/audio.duration*100 : 0;
  fillEl.style.width = p + '%';
  curEl.textContent = fmt(audio.currentTime);
  durEl.textContent = fmt(audio.duration);
});
audio.addEventListener('play', ()=> playBtn.textContent = '⏸');
audio.addEventListener('pause', ()=> playBtn.textContent = '▶');

audio.addEventListener('ended', ()=>{
  if(repeat === 2){ audio.currentTime = 0; audio.play().catch(()=>{}); return; }
  if(idx === DATA.length-1 && repeat === 0){
    fillEl.style.width = '100%';
    return;
  }
  go(idx+1, true);
});

/* 노래 파일이 없으면 안내 후 자동으로 넘어감 */
audio.addEventListener('error', ()=>{
  if(DATA[idx].key !== 'song') return;
  missEl.style.display = 'block';
  if(repeat === 2) return;
  skipTimer = setTimeout(()=> go(idx+1, true), 2600);
});

playBtn.onclick = ()=>{ audio.paused ? audio.play().catch(()=>{}) : audio.pause(); };
nextBtn.onclick = ()=> go(idx+1, true);
prevBtn.onclick = ()=>{
  if(audio.currentTime > 3){ audio.currentTime = 0; return; }
  go(idx-1, true);
};
repBtn.onclick = ()=>{
  repeat = (repeat+1) % 3;
  repBtn.classList.toggle('on', repeat !== 0);
  repBtn.innerHTML = '↻' + (repeat===2 ? '<span class="badge">1</span>' : '');
  hintEl.textContent = repeat===0 ? '반복: 없음 (한 번 재생하고 끝)'
                    : repeat===1 ? '반복: 전체 무한 연속 · 스페이스 재생/정지 · ← → 건너뛰기'
                                 : '반복: 지금 메뉴만 무한 반복';
};
muteBtn.onclick = ()=>{
  audio.muted = !audio.muted;
  muteBtn.textContent = audio.muted ? '🔇' : '🔊';
  muteBtn.classList.toggle('on', audio.muted);
};
barEl.onclick = (e)=>{
  if(!audio.duration) return;
  const r = barEl.getBoundingClientRect();
  audio.currentTime = (e.clientX - r.left) / r.width * audio.duration;
};
addEventListener('keydown', (e)=>{
  if(e.code === 'Space'){ e.preventDefault(); playBtn.click(); }
  if(e.code === 'ArrowRight') nextBtn.click();
  if(e.code === 'ArrowLeft') prevBtn.click();
});

/* 시작 오버레이 — 누르면 '전체 무한 연속'이 켜진 채로 시작 */
const overlay = document.getElementById('overlay');
function start(){
  overlay.style.display = 'none';
  repeat = 1;
  repBtn.classList.add('on');
  go(0, true);
}
document.getElementById('start').onclick = start;
overlay.onclick = start;

go(0, false);
</script>
</body>
</html>
"""


def build() -> str:
    data = [
        {"key": "reading", "label": "낭독", "file": "audio/01_reading.mp3", "text": C.READING_TEXT},
        {"key": "sermon", "label": "강론", "file": "audio/02_sermon.mp3", "text": C.SERMON_TEXT},
        {"key": "song", "label": "노래", "file": "audio/03_song.mp3", "text": C.SONG_LYRICS,
         "songTitle": C.SONG_TITLE},
        {"key": "prayer", "label": "기도", "file": "audio/04_prayer.mp3", "text": C.PRAYER_TEXT},
    ]
    html = TEMPLATE
    html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False, indent=2))
    html = html.replace("__KIND__", C.KIND)
    html = html.replace("__TITLE__", C.TITLE)
    html = html.replace("__DATE__", C.DATE)
    html = html.replace("__CITATION__", C.CITATION)
    html = html.replace("__SOURCE__", C.SOURCE)
    return html


if __name__ == "__main__":
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(build())
    print("index.html 생성 완료")

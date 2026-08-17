# -*- coding: utf-8 -*-
"""content.py 의 원고를 그대로 넣어 index.html 을 생성합니다.
   원고를 고쳤으면  python build_index.py  를 다시 실행하십시오."""

import content as C
from generate_audio_daily import read_citation


def js(s):
    """자바스크립트 템플릿 리터럴 안전 이스케이프"""
    return s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>오늘의 __KIND__ 묵상 __DATE__ · __TITLE__</title>
<style>
  :root{
    --bg1:#0b1226; --bg2:#141c36; --bg3:#1e2746;
    --gold:#e3b662; --gold-soft:#c99a45;
    --ink:#eef2fb; --ink-dim:#b9c3dd; --ink-mute:#8492b4;
    --line:rgba(227,182,98,.28);
    --card:rgba(20,28,54,.72);
  }
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html,body{margin:0;padding:0;height:100%}
  body{
    background:linear-gradient(180deg,var(--bg1) 0%,var(--bg2) 55%,var(--bg3) 100%);
    color:var(--ink);
    font-family:"Noto Serif KR","Nanum Myeongjo",-apple-system,BlinkMacSystemFont,
                "Malgun Gothic","Apple SD Gothic Neo",serif;
    min-height:100%;
    overflow-x:hidden;
  }
  #sky{position:fixed;inset:0;z-index:0;pointer-events:none}
  .moon{
    position:fixed;top:34px;right:38px;width:74px;height:74px;border-radius:50%;
    background:radial-gradient(circle at 34% 34%,#fff6dd 0%,#f3dfa8 42%,#d8b978 72%,#b8974f 100%);
    box-shadow:0 0 44px 16px rgba(227,182,98,.20),0 0 110px 46px rgba(227,182,98,.10);
    z-index:0;pointer-events:none;
  }
  .wrap{position:relative;z-index:2;max-width:760px;margin:0 auto;padding:34px 20px 130px}

  header{text-align:center;margin-bottom:22px}
  .eyebrow{letter-spacing:.32em;font-size:12px;color:var(--gold);opacity:.9}
  h1{font-size:30px;margin:12px 0 6px;color:#fff;font-weight:700;letter-spacing:-.01em}
  .subtitle{color:var(--gold);font-size:15px;letter-spacing:.04em}
  .cite{color:var(--ink-mute);font-size:13px;margin-top:8px;line-height:1.7}
  .rule{width:88px;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);margin:18px auto}

  .menu{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:20px 0 26px}
  .menu button{
    background:rgba(255,255,255,.04);border:1px solid var(--line);color:var(--ink-dim);
    padding:9px 18px;border-radius:999px;font-size:14px;cursor:pointer;
    font-family:inherit;transition:.18s;
  }
  .menu button:hover{color:var(--ink);border-color:var(--gold)}
  .menu button.on{background:var(--gold);border-color:var(--gold);color:#16203a;font-weight:700}
  .menu button.missing{opacity:.42}

  .panel{
    background:var(--card);border:1px solid rgba(227,182,98,.16);border-radius:18px;
    padding:30px 26px;backdrop-filter:blur(3px);
    box-shadow:0 18px 50px rgba(0,0,0,.34);
  }
  .panel .label{
    display:inline-block;border:1px solid var(--line);color:var(--gold);
    font-size:12px;letter-spacing:.22em;padding:5px 14px;border-radius:999px;margin-bottom:18px;
  }
  .body{font-size:18px;line-height:2.05;color:var(--ink);white-space:pre-wrap;word-break:keep-all}
  .body.verse{font-size:18.5px;line-height:2.15}
  .body.song{text-align:center;line-height:2.3}
  .body.prayer{text-align:center;line-height:2.25}
  .tag{color:var(--gold);font-size:14px;letter-spacing:.18em}
  .songtitle{text-align:center;color:var(--gold);font-size:17px;margin-bottom:16px;letter-spacing:.06em}
  .note{margin-top:20px;color:var(--ink-mute);font-size:13px;text-align:center;line-height:1.9}

  .player{
    position:fixed;left:0;right:0;bottom:0;z-index:5;
    background:linear-gradient(180deg,rgba(11,18,38,.10),rgba(11,18,38,.94) 34%);
    border-top:1px solid rgba(227,182,98,.18);
    padding:12px 16px calc(14px + env(safe-area-inset-bottom));
  }
  .pbar{
    max-width:760px;margin:0 auto 10px;height:5px;border-radius:99px;
    background:rgba(255,255,255,.12);cursor:pointer;overflow:hidden;
  }
  .pfill{height:100%;width:0;background:linear-gradient(90deg,var(--gold-soft),var(--gold));border-radius:99px}
  .ctrls{max-width:760px;margin:0 auto;display:flex;align-items:center;justify-content:center;gap:10px}
  .ctrls button{
    background:rgba(255,255,255,.05);border:1px solid var(--line);color:var(--ink);
    width:44px;height:44px;border-radius:50%;font-size:15px;cursor:pointer;
    display:flex;align-items:center;justify-content:center;font-family:inherit;transition:.18s;
    position:relative;
  }
  .ctrls button:hover{border-color:var(--gold);color:var(--gold)}
  .ctrls .play{width:56px;height:56px;background:var(--gold);border-color:var(--gold);color:#16203a;font-size:19px}
  .ctrls .play:hover{color:#16203a}
  .ctrls button.act{border-color:var(--gold);color:var(--gold);background:rgba(227,182,98,.12)}
  .badge{
    position:absolute;top:-3px;right:-3px;background:var(--gold);color:#16203a;
    font-size:10px;font-weight:700;width:16px;height:16px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
  }
  .status{max-width:760px;margin:9px auto 0;text-align:center;color:var(--ink-mute);font-size:12px;letter-spacing:.06em}

  #overlay{
    position:fixed;inset:0;z-index:20;background:rgba(8,13,28,.93);
    display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:26px;
  }
  #overlay h2{color:#fff;font-size:25px;margin:0 0 10px;font-weight:700}
  #overlay p{color:var(--ink-dim);font-size:15px;margin:0 0 6px;line-height:1.9}
  #overlay .startbtn{
    margin-top:26px;background:var(--gold);color:#16203a;border:none;border-radius:999px;
    padding:15px 44px;font-size:17px;font-weight:700;cursor:pointer;font-family:inherit;
    box-shadow:0 12px 34px rgba(227,182,98,.26);
  }
  @media(max-width:520px){
    h1{font-size:25px}
    .panel{padding:24px 18px}
    .body{font-size:17px;line-height:1.98}
    .moon{width:56px;height:56px;top:22px;right:22px}
  }
</style>
</head>
<body>
<canvas id="sky"></canvas>
<div class="moon"></div>

<div class="wrap">
  <header>
    <div class="eyebrow">URANTIA CORE TRUTH</div>
    <h1>오늘의 __KIND__ 묵상</h1>
    <div class="subtitle">__TITLE__</div>
    <div class="cite">__DATE__ · 유란시아서 __CITATION__<br>__SOURCE__</div>
    <div class="rule"></div>
  </header>

  <nav class="menu" id="menu"></nav>

  <section class="panel">
    <span class="label" id="secLabel">낭독</span>
    <div class="body" id="secBody"></div>
    <div class="note" id="secNote"></div>
  </section>
</div>

<div class="player">
  <div class="pbar" id="pbar"><div class="pfill" id="pfill"></div></div>
  <div class="ctrls">
    <button id="btnRepeat" title="반복">↻</button>
    <button id="btnPrev" title="이전">⏮</button>
    <button class="play" id="btnPlay" title="재생/일시정지">▶</button>
    <button id="btnNext" title="다음">⏭</button>
    <button id="btnMute" title="음소거">🔊</button>
  </div>
  <div class="status" id="status">시작을 누르면 낭독부터 이어집니다</div>
</div>

<div id="overlay">
  <h2>오늘의 __KIND__ 묵상</h2>
  <p>__DATE__ · 「__TITLE__」</p>
  <p>유란시아서 __CITATION__</p>
  <p style="color:var(--ink-mute);font-size:13px;margin-top:14px">
     낭독 → 강론 → 노래 → 기도 순서로 이어서 재생됩니다
  </p>
  <button class="startbtn" id="startBtn">묵상 시작</button>
</div>

<audio id="au" preload="none"></audio>

<script>
const DATA = [
  {key:"reading", label:"낭독", file:"audio/01_reading.mp3", cls:"verse",
   text:`__READING__`},
  {key:"sermon",  label:"강론", file:"audio/02_sermon.mp3",  cls:"",
   text:`__SERMON__`},
  {key:"song",    label:"노래", file:"audio/03_song.mp3",    cls:"song",
   title:`__SONG_TITLE__`,
   text:`__SONG__`},
  {key:"prayer",  label:"기도", file:"audio/04_prayer.mp3",  cls:"prayer",
   text:`__PRAYER__`}
];
const CITATION = "__CITATION__";
const CITATION_KO = "__CITATION_KO__";

/* ── 밤하늘 별 ───────────────────────────── */
(function(){
  const cv = document.getElementById('sky');
  const ctx = cv.getContext('2d');
  let stars = [];
  function init(){
    cv.width = innerWidth; cv.height = innerHeight;
    stars = [];
    for(let i=0;i<150;i++){
      stars.push({
        x: Math.random()*cv.width,
        y: Math.random()*cv.height*0.92,
        r: Math.random()*1.35+0.35,
        a: Math.random()*0.6+0.25,
        s: Math.random()*0.011+0.003
      });
    }
  }
  function draw(){
    ctx.clearRect(0,0,cv.width,cv.height);
    for(const st of stars){
      st.a += st.s;
      if(st.a>0.92 || st.a<0.16) st.s *= -1;
      ctx.beginPath();
      ctx.arc(st.x,st.y,st.r,0,Math.PI*2);
      ctx.fillStyle = 'rgba(255,248,225,'+st.a.toFixed(3)+')';
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }
  init(); draw();
  addEventListener('resize', init);
})();

/* ── 재생기 ─────────────────────────────── */
const au      = document.getElementById('au');
const menuEl  = document.getElementById('menu');
const labelEl = document.getElementById('secLabel');
const bodyEl  = document.getElementById('secBody');
const noteEl  = document.getElementById('secNote');
const pbar    = document.getElementById('pbar');
const pfill   = document.getElementById('pfill');
const btnPlay = document.getElementById('btnPlay');
const btnPrev = document.getElementById('btnPrev');
const btnNext = document.getElementById('btnNext');
const btnRep  = document.getElementById('btnRepeat');
const btnMute = document.getElementById('btnMute');
const statusEl= document.getElementById('status');
const overlay = document.getElementById('overlay');

let idx = 0;
let repeatMode = 1;               /* 0 없음 · 1 전체 반복 · 2 한 메뉴 반복 */
let started = false;
const missing = {};                /* 파일이 없는 구간 */

const REPEAT_TEXT = ['반복 없음','전체 무한 반복','한 메뉴 무한 반복'];

function buildMenu(){
  menuEl.innerHTML = '';
  DATA.forEach((d,i)=>{
    const b = document.createElement('button');
    b.textContent = d.label;
    b.dataset.i = i;
    b.onclick = ()=>{ go(i,true); };
    menuEl.appendChild(b);
  });
}

function paintMenu(){
  [...menuEl.children].forEach((b,i)=>{
    b.classList.toggle('on', i===idx);
    b.classList.toggle('missing', !!missing[DATA[i].key]);
  });
}

function renderSection(){
  const d = DATA[idx];
  labelEl.textContent = d.label;
  let html = '';
  if(d.key === 'song' && d.title){
    html += '<div class="songtitle">「'+d.title+'」</div>';
  }
  let t = d.text;
  if(d.key === 'song'){
    t = t.replace(/^\\[(.+?)\\]$/gm, '<span class="tag">[$1]</span>');
  }
  html += t;
  bodyEl.className = 'body ' + (d.cls||'');
  bodyEl.innerHTML = html;

  if(d.key === 'reading'){
    noteEl.textContent = '유란시아서 ' + CITATION + '  ( ' + CITATION_KO + ' )';
  }else if(d.key === 'song'){
    noteEl.textContent = missing.song
      ? 'audio/03_song.mp3 이 없어 자동으로 다음으로 넘어갑니다'
      : '';
  }else{
    noteEl.textContent = '';
  }
  paintMenu();
}

function setStatus(extra){
  const d = DATA[idx];
  statusEl.textContent = (extra || (d.label + ' 재생 중')) + ' · ' + REPEAT_TEXT[repeatMode];
}

function go(i, autoplay){
  idx = (i + DATA.length) % DATA.length;
  renderSection();
  pfill.style.width = '0%';
  const d = DATA[idx];
  au.src = d.file;
  if(autoplay && started){
    au.play().catch(()=>{ setStatus('재생을 누르세요'); });
  }
  setStatus();
}

function next(auto){
  if(repeatMode === 2 && auto){
    au.currentTime = 0;
    au.play().catch(()=>{});
    return;
  }
  if(idx === DATA.length-1){
    if(repeatMode === 1 || !auto){ go(0,true); }
    else { btnPlay.textContent='▶'; setStatus('묵상을 마쳤습니다'); }
    return;
  }
  go(idx+1, true);
}

function prev(){
  if(au.currentTime > 3){ au.currentTime = 0; return; }
  go(idx-1, true);
}

btnPlay.onclick = ()=>{
  if(au.paused){ au.play().catch(()=>{}); } else { au.pause(); }
};
btnNext.onclick = ()=> next(false);
btnPrev.onclick = prev;

btnRep.onclick = ()=>{
  repeatMode = (repeatMode+1) % 3;
  btnRep.classList.toggle('act', repeatMode !== 0);
  btnRep.innerHTML = '↻' + (repeatMode===2 ? '<span class="badge">1</span>' : '');
  setStatus();
};

btnMute.onclick = ()=>{
  au.muted = !au.muted;
  btnMute.textContent = au.muted ? '🔇' : '🔊';
  btnMute.classList.toggle('act', au.muted);
};

pbar.onclick = (e)=>{
  if(!au.duration) return;
  const r = pbar.getBoundingClientRect();
  au.currentTime = ((e.clientX - r.left)/r.width) * au.duration;
};

au.addEventListener('timeupdate', ()=>{
  if(au.duration) pfill.style.width = (au.currentTime/au.duration*100) + '%';
});
au.addEventListener('play',  ()=>{ btnPlay.textContent='⏸'; setStatus(); });
au.addEventListener('pause', ()=>{ btnPlay.textContent='▶'; });
au.addEventListener('ended', ()=> next(true));
au.addEventListener('error', ()=>{
  const d = DATA[idx];
  missing[d.key] = true;
  paintMenu();
  if(d.key === 'song'){
    noteEl.textContent = 'audio/03_song.mp3 이 없어 자동으로 다음으로 넘어갑니다';
    setStatus('노래 파일이 없어 건너뜁니다');
    setTimeout(()=> next(true), 900);
  }else{
    setStatus(d.label + ' 음성 파일이 없습니다');
  }
});

addEventListener('keydown', (e)=>{
  if(e.code === 'Space'){ e.preventDefault(); btnPlay.click(); }
  else if(e.code === 'ArrowRight'){ next(false); }
  else if(e.code === 'ArrowLeft'){ prev(); }
});

document.getElementById('startBtn').onclick = ()=>{
  started = true;
  overlay.style.display = 'none';
  go(0, true);
};

buildMenu();
btnRep.classList.add('act');
renderSection();
au.src = DATA[0].file;
setStatus('시작을 누르면 낭독부터 이어집니다');
</script>
</body>
</html>
"""


def main():
    out = HTML
    repl = {
        "__KIND__": C.KIND,
        "__DATE__": C.DATE,
        "__TITLE__": C.TITLE,
        "__CITATION__": C.CITATION,
        "__CITATION_KO__": read_citation(C.CITATION),
        "__SOURCE__": C.SOURCE,
        "__READING__": js(C.READING),
        "__SERMON__": js(C.SERMON),
        "__SONG_TITLE__": js(C.SONG_TITLE),
        "__SONG__": js(C.SONG),
        "__PRAYER__": js(C.PRAYER),
    }
    for k, v in repl.items():
        out = out.replace(k, v)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(out)
    print("index.html 생성 완료 (%d 바이트)" % len(out.encode("utf-8")))


if __name__ == "__main__":
    main()

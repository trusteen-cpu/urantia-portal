# -*- coding: utf-8 -*-
"""content.py 의 원고를 그대로 index.html 에 심어 줍니다.

    python build_index.py

원고를 고쳤으면 이 스크립트를 다시 돌리세요. (index.html 이 새로 만들어집니다)
"""

import io
import os
import content

HERE = os.path.dirname(os.path.abspath(__file__))


def js(s: str) -> str:
    """자바스크립트 백틱 문자열 안에 안전하게 넣기."""
    return (s.replace("\\", "\\\\")
             .replace("`", "\\`")
             .replace("${", "\\${")
             .replace("</", "<\\/"))


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>오늘의 __KIND__ 묵상 __DATE__ · __TITLE__</title>
<style>
  :root{
    --ink:#f4ecdd;
    --dim:#c6b9a4;
    --gold:#e8c479;
    --gold-soft:rgba(232,196,121,.28);
    --panel:rgba(20,26,52,.55);
    --panel-2:rgba(20,26,52,.78);
    --line:rgba(232,196,121,.22);
    --amber:#f0b96b;
  }
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html,body{margin:0;padding:0;height:100%}
  body{
    font-family:"Noto Serif KR","Nanum Myeongjo",'Apple SD Gothic Neo',
                'Malgun Gothic',serif;
    color:var(--ink);
    background:linear-gradient(180deg,
        #161d3a 0%, #262b52 26%, #4a3f63 52%, #9a6a56 78%, #e8a860 100%);
    background-attachment:fixed;
    min-height:100%;
    overflow-x:hidden;
  }
  #sky{position:fixed;inset:0;z-index:0;pointer-events:none}
  #sun{
    position:fixed;right:-90px;bottom:-140px;width:420px;height:420px;
    border-radius:50%;z-index:0;pointer-events:none;
    background:radial-gradient(circle,
        rgba(255,226,170,.85) 0%, rgba(246,190,116,.45) 38%,
        rgba(233,150,86,.18) 62%, rgba(233,150,86,0) 78%);
    filter:blur(2px);
  }
  .wrap{position:relative;z-index:1;max-width:820px;margin:0 auto;
        padding:26px 18px 54px}

  header{text-align:center;padding:14px 0 8px}
  .date{font-size:13px;letter-spacing:.22em;color:var(--gold);opacity:.9}
  h1{margin:.42em 0 .18em;font-size:26px;font-weight:700;letter-spacing:.01em}
  .sub{font-size:14px;color:var(--dim);line-height:1.6}
  .rule{width:112px;height:1px;margin:16px auto 0;
        background:linear-gradient(90deg,transparent,var(--gold),transparent)}

  .tabs{display:flex;gap:8px;justify-content:center;margin:22px 0 16px;
        flex-wrap:wrap}
  .tab{border:1px solid var(--line);background:var(--panel);color:var(--dim);
       padding:9px 17px;border-radius:999px;font-size:14px;cursor:pointer;
       transition:.18s;font-family:inherit}
  .tab:hover{border-color:var(--gold-soft);color:var(--ink)}
  .tab.on{background:rgba(232,196,121,.16);border-color:var(--gold);
          color:var(--gold);font-weight:700}
  .tab .n{opacity:.6;margin-right:6px;font-size:12px}

  .card{background:var(--panel-2);border:1px solid var(--line);
        border-radius:16px;padding:24px 22px;
        box-shadow:0 10px 34px rgba(8,12,28,.34)}
  .label{display:inline-block;border:1px solid var(--gold-soft);
         color:var(--gold);border-radius:999px;padding:4px 13px;
         font-size:12px;letter-spacing:.14em;margin-bottom:14px}
  .cite{color:var(--gold);font-size:13px;margin-bottom:10px;opacity:.95}
  .body{font-size:17px;line-height:2.0;white-space:pre-wrap;word-break:keep-all}
  .body.reading{font-size:17.5px}
  .body.song{text-align:center;line-height:2.15}
  .body.prayer{text-align:center;line-height:2.15}
  .tag{color:var(--amber);font-size:13px;letter-spacing:.1em}

  .player{position:sticky;bottom:0;margin-top:22px;
          background:rgba(14,19,40,.92);backdrop-filter:blur(8px);
          border:1px solid var(--line);border-radius:16px;padding:14px 16px 16px}
  .bar{height:6px;border-radius:999px;background:rgba(255,255,255,.14);
       cursor:pointer;overflow:hidden}
  .bar>i{display:block;height:100%;width:0;border-radius:999px;
         background:linear-gradient(90deg,var(--gold),var(--amber))}
  .times{display:flex;justify-content:space-between;font-size:11.5px;
         color:var(--dim);margin-top:6px;letter-spacing:.04em}
  .ctrls{display:flex;align-items:center;justify-content:center;gap:10px;
         margin-top:10px;flex-wrap:wrap}
  .btn{border:1px solid var(--line);background:rgba(255,255,255,.05);
       color:var(--ink);width:44px;height:44px;border-radius:50%;
       font-size:16px;cursor:pointer;display:flex;align-items:center;
       justify-content:center;transition:.16s;font-family:inherit}
  .btn:hover{border-color:var(--gold);color:var(--gold)}
  .btn.play{width:56px;height:56px;font-size:20px;
            background:rgba(232,196,121,.18);border-color:var(--gold);
            color:var(--gold)}
  .btn.on{background:rgba(232,196,121,.2);border-color:var(--gold);
          color:var(--gold)}
  .btn .badge{position:absolute;transform:translate(15px,-15px);
              font-size:10px;background:var(--gold);color:#1a1f38;
              border-radius:999px;padding:0 4px;font-weight:700}
  .now{text-align:center;font-size:12.5px;color:var(--dim);margin-top:9px;
       letter-spacing:.06em;min-height:17px}

  #gate{position:fixed;inset:0;z-index:9;display:flex;align-items:center;
        justify-content:center;background:rgba(10,14,32,.9);
        backdrop-filter:blur(3px);cursor:pointer}
  #gate .in{text-align:center;padding:30px}
  #gate .ring{width:96px;height:96px;border-radius:50%;margin:0 auto 20px;
              border:1px solid var(--gold);display:flex;align-items:center;
              justify-content:center;font-size:30px;color:var(--gold);
              background:rgba(232,196,121,.1)}
  #gate h2{margin:0 0 8px;font-size:20px;font-weight:700}
  #gate p{margin:0;font-size:13.5px;color:var(--dim);line-height:1.9}

  footer{text-align:center;margin-top:26px;font-size:12px;color:var(--dim);
         opacity:.75;line-height:1.9}
  @media(max-width:520px){
    h1{font-size:22px}
    .body{font-size:16px;line-height:1.95}
    .card{padding:20px 16px}
  }
</style>
</head>
<body>
<canvas id="sky"></canvas><div id="sun"></div>

<div class="wrap">
  <header>
    <div class="date">__DATE__</div>
    <h1>오늘의 __KIND__ 묵상 · __TITLE__</h1>
    <div class="sub">__SOURCE__</div>
    <div class="rule"></div>
  </header>

  <div class="tabs" id="tabs"></div>

  <div class="card">
    <span class="label" id="lab">낭독</span>
    <div class="cite" id="cite">유란시아서 __CITATION__</div>
    <div class="body reading" id="body"></div>
  </div>

  <div class="player">
    <div class="bar" id="bar"><i id="fill"></i></div>
    <div class="times"><span id="cur">0:00</span><span id="dur">0:00</span></div>
    <div class="ctrls">
      <button class="btn" id="prev" title="이전 (←)">⏮</button>
      <button class="btn play" id="play" title="재생/일시정지 (Space)">▶</button>
      <button class="btn" id="next" title="다음 (→)">⏭</button>
      <button class="btn" id="rep" title="반복: 없음 → 전체 → 한 메뉴">↻</button>
      <button class="btn" id="mute" title="음소거">🔊</button>
    </div>
    <div class="now" id="now"></div>
  </div>

  <footer>
    낭독 → 강론 → 노래 → 기도 자동 연속 재생<br>
    Urantia Core Truth · 오늘의 __KIND__ 묵상
  </footer>
</div>

<div id="gate"><div class="in">
  <div class="ring">▶</div>
  <h2>오늘의 __KIND__ 묵상 __DATE__</h2>
  <p>화면을 누르면 시작합니다<br>낭독 → 강론 → 노래 → 기도 · 무한 반복</p>
</div></div>

<audio id="au" preload="auto"></audio>

<script>
const DATA = [
  {key:"reading", n:"01", label:"낭독", file:"audio/01_reading.mp3",
   cite:"유란시아서 __CITATION__", cls:"reading",
   text:`__READING__`},
  {key:"sermon", n:"02", label:"강론", file:"audio/02_sermon.mp3",
   cite:"__TITLE__", cls:"",
   text:`__SERMON__`},
  {key:"song", n:"03", label:"노래", file:"audio/03_song.mp3",
   cite:"__SONG_TITLE__", cls:"song",
   text:`__SONG__`},
  {key:"prayer", n:"04", label:"기도", file:"audio/04_prayer.mp3",
   cite:"오늘의 기도", cls:"prayer",
   text:`__PRAYER__`}
];

const au=document.getElementById('au'), bodyEl=document.getElementById('body'),
      labEl=document.getElementById('lab'), citeEl=document.getElementById('cite'),
      tabsEl=document.getElementById('tabs'), fill=document.getElementById('fill'),
      barEl=document.getElementById('bar'), curEl=document.getElementById('cur'),
      durEl=document.getElementById('dur'), nowEl=document.getElementById('now'),
      playB=document.getElementById('play'), repB=document.getElementById('rep'),
      muteB=document.getElementById('mute');

let idx=0, repeat=0, missing=false, skipTimer=null;   // repeat 0없음 1전체 2한메뉴
const REP_TXT=['반복 없음','전체 무한 반복','한 메뉴 무한 반복'];

DATA.forEach((d,i)=>{
  const b=document.createElement('button');
  b.className='tab'; b.innerHTML='<span class="n">'+d.n+'</span>'+d.label;
  b.onclick=()=>{load(i,true)};
  tabsEl.appendChild(b);
});
const tabs=[...tabsEl.children];

function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function render(t){
  return esc(t).replace(/^\[([^\]]+)\]$/gm,'<span class="tag">[$1]</span>');
}
function fmt(s){
  if(!isFinite(s)||s<0)s=0;
  const m=Math.floor(s/60), x=Math.floor(s%60);
  return m+':'+String(x).padStart(2,'0');
}

function load(i,autoplay){
  clearTimeout(skipTimer); missing=false;
  idx=(i+DATA.length)%DATA.length;
  const d=DATA[idx];
  labEl.textContent=d.label;
  citeEl.textContent=d.cite;
  bodyEl.className='body '+d.cls;
  bodyEl.innerHTML=render(d.text);
  tabs.forEach((t,k)=>t.classList.toggle('on',k===idx));
  nowEl.textContent='';
  fill.style.width='0%'; curEl.textContent='0:00'; durEl.textContent='0:00';
  au.src=d.file;
  au.load();
  if(autoplay) au.play().catch(()=>{playB.textContent='▶'});
  window.scrollTo({top:0,behavior:'smooth'});
}

au.addEventListener('loadedmetadata',()=>{durEl.textContent=fmt(au.duration)});
au.addEventListener('timeupdate',()=>{
  if(au.duration){
    fill.style.width=(au.currentTime/au.duration*100)+'%';
    curEl.textContent=fmt(au.currentTime);
  }
});
au.addEventListener('play',()=>{playB.textContent='⏸'});
au.addEventListener('pause',()=>{playB.textContent='▶'});

au.addEventListener('error',()=>{
  if(DATA[idx].key==='song'){
    missing=true;
    nowEl.textContent='노래 파일(audio/03_song.mp3)이 아직 없습니다 · 잠시 후 넘어갑니다';
    skipTimer=setTimeout(()=>{advance()},2600);
  }else{
    nowEl.textContent='음성 파일이 없습니다 · '+DATA[idx].file;
  }
});

function advance(){
  if(repeat===2){ load(idx,true); return; }
  if(idx===DATA.length-1){
    if(repeat===1){ load(0,true); }
    else{ nowEl.textContent='오늘의 묵상을 마쳤습니다'; }
    return;
  }
  load(idx+1,true);
}
au.addEventListener('ended',advance);

playB.onclick=()=>{ if(au.paused){au.play().catch(()=>{})}else{au.pause()} };
document.getElementById('next').onclick=()=>{ load(idx+1,true) };
document.getElementById('prev').onclick=()=>{
  if(au.currentTime>3 && !missing){ au.currentTime=0; }
  else{ load(idx-1,true); }
};
repB.onclick=()=>{
  repeat=(repeat+1)%3;
  repB.classList.toggle('on',repeat>0);
  repB.innerHTML = repeat===2 ? '↻<span class="badge">1</span>' : '↻';
  nowEl.textContent=REP_TXT[repeat];
};
muteB.onclick=()=>{
  au.muted=!au.muted;
  muteB.textContent=au.muted?'🔇':'🔊';
  muteB.classList.toggle('on',au.muted);
};
barEl.onclick=e=>{
  if(!au.duration)return;
  const r=barEl.getBoundingClientRect();
  au.currentTime=(e.clientX-r.left)/r.width*au.duration;
};
document.addEventListener('keydown',e=>{
  if(e.code==='Space'){e.preventDefault();playB.click()}
  if(e.code==='ArrowRight'){document.getElementById('next').click()}
  if(e.code==='ArrowLeft'){document.getElementById('prev').click()}
});

document.getElementById('gate').onclick=function(){
  this.style.display='none';
  repeat=1; repB.classList.add('on'); nowEl.textContent=REP_TXT[1];
  load(0,true);
};

/* 새벽 하늘의 별 — 화면 위쪽에만, 아래로 갈수록 사라짐 */
(function(){
  const c=document.getElementById('sky'), x=c.getContext('2d');
  let W,H,stars=[];
  function init(){
    W=c.width=innerWidth; H=c.height=innerHeight;
    stars=[];
    for(let i=0;i<70;i++){
      const y=Math.random()*H*0.58;
      stars.push({x:Math.random()*W,y:y,r:Math.random()*1.25+.35,
                  a:Math.random(),s:Math.random()*.016+.004,
                  f:Math.max(0,1-y/(H*0.58))});
    }
  }
  function draw(){
    x.clearRect(0,0,W,H);
    for(const s of stars){
      s.a+=s.s; const t=(Math.sin(s.a)+1)/2;
      x.globalAlpha=(0.18+t*0.5)*s.f;
      x.fillStyle='#fff5e0';
      x.beginPath(); x.arc(s.x,s.y,s.r,0,6.2832); x.fill();
    }
    x.globalAlpha=1;
    requestAnimationFrame(draw);
  }
  addEventListener('resize',init);
  init(); draw();
})();

load(0,false);
</script>
</body>
</html>
"""


def main():
    html = TEMPLATE
    repl = {
        "__KIND__": content.KIND,
        "__DATE__": content.DATE,
        "__TITLE__": content.TITLE,
        "__SOURCE__": content.SOURCE,
        "__CITATION__": content.CITATION,
        "__SONG_TITLE__": content.SONG_TITLE,
        "__READING__": js(content.READING),
        "__SERMON__": js(content.SERMON),
        "__SONG__": js(content.SONG_LYRICS),
        "__PRAYER__": js(content.PRAYER),
    }
    for k, v in repl.items():
        html = html.replace(k, v)

    out = os.path.join(HERE, "index.html")
    with io.open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html 을 새로 만들었습니다.  (" + str(len(html)) + " 바이트)")


if __name__ == "__main__":
    main()

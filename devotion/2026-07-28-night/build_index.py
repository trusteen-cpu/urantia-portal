# -*- coding: utf-8 -*-
"""content.py 의 네 가지 원고로 index.html 을 생성합니다.
   원고를 고치면 이 스크립트를 다시 돌리세요.  python build_index.py
"""
import os
import json
import content

HERE = os.path.dirname(os.path.abspath(__file__))


def js(s):
    """자바스크립트 문자열 리터럴로 안전하게 변환"""
    return json.dumps(s, ensure_ascii=False)


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>오늘의 __KIND__ 묵상 __DATE__ · __TITLE__</title>
<style>
  :root{
    --bg0:#0b1020; --bg1:#121a33; --bg2:#1c2647;
    --gold:#e8c479; --gold-dim:#a98a4e;
    --ink:#eaf0ff; --ink-dim:#9fb0d6;
    --card:rgba(255,255,255,.045);
    --line:rgba(232,196,121,.28);
  }
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html,body{height:100%}
  body{
    margin:0; color:var(--ink);
    font-family:"Noto Serif KR","Nanum Myeongjo",serif;
    background:linear-gradient(180deg,var(--bg0) 0%,var(--bg1) 55%,var(--bg2) 100%);
    overflow-x:hidden;
  }
  #sky{position:fixed;inset:0;z-index:0;pointer-events:none}
  .moon{
    position:fixed; right:8vw; top:7vh; width:86px; height:86px; border-radius:50%;
    background:radial-gradient(circle at 36% 34%,#fff8e6 0%,#f3e2b4 55%,#e2c98d 100%);
    box-shadow:0 0 34px 12px rgba(240,224,170,.20),0 0 90px 40px rgba(240,224,170,.10);
    z-index:0;
  }
  .wrap{position:relative;z-index:1;max-width:820px;margin:0 auto;padding:26px 20px 46px}
  header{text-align:center;padding:16px 0 6px}
  .eyebrow{color:var(--gold);letter-spacing:.32em;font-size:12px}
  h1{font-size:27px;margin:12px 0 6px;font-weight:700;letter-spacing:-.01em}
  .sub{color:var(--ink-dim);font-size:14px}
  .cite{color:var(--gold);font-size:13px;margin-top:8px}
  .rule{height:1px;background:linear-gradient(90deg,transparent,var(--line),transparent);margin:20px 0 4px}

  nav{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:20px 0 16px}
  nav button{
    background:var(--card);border:1px solid rgba(255,255,255,.10);color:var(--ink-dim);
    border-radius:12px;padding:11px 4px;font-size:14px;font-family:inherit;cursor:pointer;
    transition:.18s;
  }
  nav button .n{display:block;font-size:10px;letter-spacing:.16em;color:var(--gold-dim);margin-bottom:3px}
  nav button.on{background:rgba(232,196,121,.13);border-color:var(--line);color:var(--gold)}

  .panel{
    background:var(--card);border:1px solid rgba(255,255,255,.08);border-radius:18px;
    padding:24px 22px;min-height:220px;
  }
  .label{color:var(--gold);font-size:12px;letter-spacing:.26em;margin-bottom:14px}
  .body{font-size:17px;line-height:2.05;white-space:pre-wrap;word-break:keep-all}
  .body.song{text-align:center;line-height:2.25}
  .body .tag{color:var(--gold);font-size:14px;letter-spacing:.12em;display:block;margin:14px 0 4px}
  .miss{color:var(--ink-dim);font-size:14px;line-height:1.9;text-align:center;padding:22px 0}

  .bar{margin-top:20px}
  .track{height:5px;background:rgba(255,255,255,.10);border-radius:99px;cursor:pointer;overflow:hidden}
  .fill{height:100%;width:0;background:linear-gradient(90deg,var(--gold-dim),var(--gold));border-radius:99px}
  .time{display:flex;justify-content:space-between;color:var(--ink-dim);font-size:12px;margin-top:7px}

  .ctrls{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:16px;flex-wrap:wrap}
  .ctrls button{
    background:var(--card);border:1px solid rgba(255,255,255,.12);color:var(--ink);
    width:48px;height:48px;border-radius:50%;font-size:16px;cursor:pointer;font-family:inherit;
    display:flex;align-items:center;justify-content:center;transition:.18s;position:relative;
  }
  .ctrls button.play{width:62px;height:62px;font-size:21px;border-color:var(--line);color:var(--gold)}
  .ctrls button.on{background:rgba(232,196,121,.15);border-color:var(--line);color:var(--gold)}
  .badge{
    position:absolute;top:-3px;right:-3px;background:var(--gold);color:#1a1608;
    font-size:10px;line-height:1;padding:3px 4px;border-radius:8px;font-weight:700;
  }
  .hint{color:var(--ink-dim);font-size:12px;text-align:center;margin-top:16px;line-height:1.8}

  #overlay{
    position:fixed;inset:0;z-index:9;background:rgba(8,12,26,.90);
    display:flex;align-items:center;justify-content:center;flex-direction:column;gap:20px;
    backdrop-filter:blur(3px);cursor:pointer;text-align:center;padding:24px;
  }
  #overlay h2{font-size:22px;margin:0;font-weight:700}
  #overlay p{color:var(--ink-dim);font-size:14px;margin:0;line-height:1.9}
  #overlay .go{
    border:1px solid var(--line);color:var(--gold);background:rgba(232,196,121,.10);
    padding:14px 34px;border-radius:99px;font-size:16px;font-family:inherit;
  }
  @media(max-width:520px){
    h1{font-size:23px}.body{font-size:16px;line-height:1.95}
    .panel{padding:20px 16px}.moon{width:66px;height:66px;right:7vw;top:5vh}
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
    <div class="sub">__DATE__ · 「__TITLE__」</div>
    <div class="cite">유란시아서 __CITATION__ — __SOURCE__</div>
    <div class="rule"></div>
  </header>

  <nav id="nav"></nav>

  <section class="panel">
    <div class="label" id="label">낭독</div>
    <div class="body" id="text"></div>
  </section>

  <div class="bar">
    <div class="track" id="track"><div class="fill" id="fill"></div></div>
    <div class="time"><span id="cur">0:00</span><span id="dur">0:00</span></div>
  </div>

  <div class="ctrls">
    <button id="repeat" title="반복">↻</button>
    <button id="prev" title="이전">⏮</button>
    <button id="play" class="play" title="재생/일시정지">▶</button>
    <button id="next" title="다음">⏭</button>
    <button id="mute" title="음소거">🔊</button>
  </div>

  <div class="hint">
    낭독 → 강론 → 노래 → 기도 순으로 자동 재생됩니다.<br>
    ↻ 반복: 없음 → 전체 무한 반복 → 한 메뉴 무한 반복<br>
    스페이스 재생·정지 / ← → 이전·다음
  </div>
</div>

<div id="overlay">
  <h2>오늘의 __KIND__ 묵상</h2>
  <p>__DATE__ · 「__TITLE__」<br>화면을 누르면 시작합니다</p>
  <div class="go">▶ 시작하기</div>
</div>

<audio id="au" preload="none"></audio>

<script>
const DATA = [
  {id:"01_reading", label:"낭독", short:"낭독", song:false, text: __READING__},
  {id:"02_sermon",  label:"강론", short:"강론", song:false, text: __SERMON__},
  {id:"03_song",    label:"노래", short:"노래", song:true,  text: __SONG__},
  {id:"04_prayer",  label:"기도", short:"기도", song:false, text: __PRAYER__}
];

const au=document.getElementById('au');
const elText=document.getElementById('text'), elLabel=document.getElementById('label');
const elNav=document.getElementById('nav'), elFill=document.getElementById('fill');
const elCur=document.getElementById('cur'), elDur=document.getElementById('dur');
const bPlay=document.getElementById('play'), bPrev=document.getElementById('prev');
const bNext=document.getElementById('next'), bRep=document.getElementById('repeat');
const bMute=document.getElementById('mute'), track=document.getElementById('track');
const overlay=document.getElementById('overlay');

let idx=0, repeat=0, started=false;   // repeat 0 없음 1 전체 2 한 메뉴

DATA.forEach((d,i)=>{
  const b=document.createElement('button');
  b.innerHTML='<span class="n">'+String(i+1).padStart(2,'0')+'</span>'+d.short;
  b.onclick=()=>{ go(i,true); };
  elNav.appendChild(b);
});

function render(){
  const d=DATA[idx];
  elLabel.textContent=d.label;
  elText.className='body'+(d.song?' song':'');
  if(d.song){
    elText.innerHTML=d.text.split('\n').map(function(ln){
      const t=ln.trim();
      if(/^\[.+\]$/.test(t)) return '<span class="tag">'+t+'</span>';
      return escapeHtml(ln);
    }).join('\n');
  }else{
    elText.textContent=d.text;
  }
  [...elNav.children].forEach((b,i)=>b.classList.toggle('on',i===idx));
}
function escapeHtml(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}

function go(i,autoplay){
  idx=(i+DATA.length)%DATA.length;
  render();
  au.src='audio/'+DATA[idx].id+'.mp3';
  elFill.style.width='0%'; elCur.textContent='0:00'; elDur.textContent='0:00';
  if(autoplay!==false && started){ au.play().catch(()=>{}); }
}

function nextSeg(auto){
  if(repeat===2 && auto){ au.currentTime=0; au.play().catch(()=>{}); return; }
  if(idx===DATA.length-1 && auto && repeat===0){
    au.pause(); bPlay.textContent='▶'; return;
  }
  go(idx+1,true);
}

au.addEventListener('ended',()=>nextSeg(true));
au.addEventListener('error',()=>{
  if(DATA[idx].id==='03_song'){
    elText.innerHTML='<div class="miss">audio/03_song.mp3 파일이 아직 없습니다.<br>'
      +'Mureka 에서 「__SONGTITLE__」 곡을 만들어 audio 폴더에 넣어 주세요.<br>'
      +'잠시 후 다음 순서로 넘어갑니다.</div>';
    if(started) setTimeout(()=>{ if(DATA[idx].id==='03_song') nextSeg(true); },2600);
  }
});
au.addEventListener('timeupdate',()=>{
  if(!au.duration||!isFinite(au.duration))return;
  elFill.style.width=(au.currentTime/au.duration*100)+'%';
  elCur.textContent=fmt(au.currentTime); elDur.textContent=fmt(au.duration);
});
au.addEventListener('play',()=>bPlay.textContent='⏸');
au.addEventListener('pause',()=>bPlay.textContent='▶');

function fmt(s){s=Math.floor(s||0);return Math.floor(s/60)+':'+String(s%60).padStart(2,'0');}

bPlay.onclick=()=>{ started=true; au.paused?au.play().catch(()=>{}):au.pause(); };
bNext.onclick=()=>{ started=true; go(idx+1,true); };
bPrev.onclick=()=>{ started=true; if(au.currentTime>3){au.currentTime=0;} else {go(idx-1,true);} };
bMute.onclick=()=>{ au.muted=!au.muted; bMute.textContent=au.muted?'🔇':'🔊'; bMute.classList.toggle('on',au.muted); };
bRep.onclick=()=>{
  repeat=(repeat+1)%3;
  bRep.classList.toggle('on',repeat>0);
  bRep.innerHTML='↻'+(repeat===2?'<span class="badge">1</span>':'');
  bRep.title=['반복 없음','전체 무한 반복','한 메뉴 무한 반복'][repeat];
};
track.onclick=(e)=>{
  if(!au.duration||!isFinite(au.duration))return;
  const r=track.getBoundingClientRect();
  au.currentTime=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width))*au.duration;
};
document.addEventListener('keydown',(e)=>{
  if(e.code==='Space'){e.preventDefault();bPlay.click();}
  else if(e.code==='ArrowRight'){bNext.click();}
  else if(e.code==='ArrowLeft'){bPrev.click();}
});
overlay.onclick=()=>{
  overlay.style.display='none';
  started=true; repeat=1;
  bRep.classList.add('on'); bRep.title='전체 무한 반복';
  go(0,true);
};

/* 별 */
(function(){
  const c=document.getElementById('sky'), x=c.getContext('2d');
  let st=[];
  function init(){
    c.width=innerWidth; c.height=innerHeight; st=[];
    for(let i=0;i<150;i++) st.push({
      x:Math.random()*c.width, y:Math.random()*c.height,
      r:Math.random()*1.35+.25, a:Math.random(), s:Math.random()*.012+.003
    });
  }
  function loop(){
    x.clearRect(0,0,c.width,c.height);
    st.forEach(p=>{
      p.a+=p.s; const o=.28+Math.abs(Math.sin(p.a))*.62;
      x.beginPath(); x.arc(p.x,p.y,p.r,0,7);
      x.fillStyle='rgba(232,240,255,'+o.toFixed(3)+')'; x.fill();
    });
    requestAnimationFrame(loop);
  }
  addEventListener('resize',init); init(); loop();
})();

render();
au.src='audio/'+DATA[0].id+'.mp3';
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
        "__CITATION__": content.CITATION,
        "__SOURCE__": content.SOURCE,
        "__SONGTITLE__": content.SONG_TITLE,
        "__READING__": js(content.READING),
        "__SERMON__": js(content.SERMON),
        "__SONG__": js(content.SONG),
        "__PRAYER__": js(content.PRAYER),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    import re as _re
    left = _re.findall(r"__[A-Z]+__", html)
    assert not left, "치환되지 않은 토큰: %s" % left
    path = os.path.join(HERE, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html 생성 완료 (%d바이트)" % len(html.encode("utf-8")))


if __name__ == "__main__":
    main()

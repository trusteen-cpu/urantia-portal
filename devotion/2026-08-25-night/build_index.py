# -*- coding: utf-8 -*-
"""content.py 를 읽어 index.html 을 만든다.  python build_index.py"""
import json, html, content

def esc(t):
    return html.escape(t, quote=False)

DATA = {
    "date": content.DATE,
    "kind": content.KIND,
    "title": content.TITLE,
    "source": content.SOURCE,
    "citation": content.CITATION,
    "reading": [{"cit": c, "text": t} for c, t in content.READING],
    "sermon": [p.strip() for p in content.SERMON.split("\n\n") if p.strip()],
    "lyrics": content.LYRICS,
    "prayer": [p.strip() for p in content.PRAYER.split("\n\n") if p.strip()],
    "audioBase": (content.AUDIO_BASE.rstrip("/") + "/") if content.AUDIO_BASE else "audio/",
}

NIGHT = {
    "g1": "#0b1020", "g2": "#121a33", "g3": "#1c2647",
    "ink": "#e8ecf6", "dim": "#9fb0d0", "gold": "#c8b06a",
    "panel": "rgba(18,26,51,.42)", "orb": "#f2edd8", "stars": 150,
    "label": "오늘의 취침 묵상",
}
MORNING = {
    "g1": "#101a33", "g2": "#2c3358", "g3": "#7a6042",
    "ink": "#fdf6e8", "dim": "#e0cfae", "gold": "#e0a94b",
    "panel": "rgba(30,28,46,.38)", "orb": "#ffd98a", "stars": 60,
    "label": "오늘의 아침 묵상",
}

TPL = r"""<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__LABEL__ __DATE__ __TITLE__</title>
<style>
:root{--g1:__G1__;--g2:__G2__;--g3:__G3__;--ink:__INK__;--dim:__DIM__;--gold:__GOLD__;--panel:__PANEL__}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;color:var(--ink);
 font-family:"Noto Serif KR","Nanum Myeongjo",Georgia,serif;
 background:linear-gradient(180deg,var(--g1) 0%,var(--g2) 55%,var(--g3) 100%);}
canvas#sky{position:fixed;inset:0;z-index:0;pointer-events:none}
.wrap{position:relative;z-index:1;max-width:820px;margin:0 auto;padding:26px 18px 120px}
header{text-align:center;padding:14px 0 6px}
header .lb{color:var(--gold);letter-spacing:.22em;font-size:12px}
header h1{margin:10px 0 4px;font-size:27px;letter-spacing:-.01em}
header .src{color:var(--dim);font-size:13px}
.panel{background:var(--panel);border:1px solid rgba(200,176,106,.25);border-radius:16px;
 padding:20px 20px 22px;margin:18px 0}
.panel h2{margin:0 0 12px;font-size:15px;color:var(--gold);letter-spacing:.16em}
.v{margin:0 0 14px;line-height:1.95;font-size:17px;text-align:justify;word-break:keep-all}
.v .c{color:var(--gold);font-size:12.5px;margin-right:7px}
.ly{white-space:pre-wrap;line-height:1.9;font-size:16px}
.ly .tag{color:var(--gold)}
.pr{white-space:pre-wrap;line-height:2;font-size:17px;text-align:center}
.now{outline:1px solid rgba(200,176,106,.5);border-radius:12px;
 background:rgba(200,176,106,.10)}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:5;
 background:rgba(8,12,26,.86);border-top:1px solid rgba(200,176,106,.3);
 padding:9px 12px 12px}
.bar .in{max-width:820px;margin:0 auto}
.seg{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-bottom:8px}
.seg button{background:none;border:1px solid rgba(200,176,106,.35);color:var(--dim);
 border-radius:999px;padding:5px 13px;font-size:12.5px;cursor:pointer;font-family:inherit}
.seg button.on{background:var(--gold);color:#141625;border-color:var(--gold);font-weight:700}
.pg{height:5px;background:rgba(255,255,255,.14);border-radius:99px;cursor:pointer;margin:7px 0}
.pg i{display:block;height:100%;width:0;background:var(--gold);border-radius:99px}
.ctl{display:flex;gap:8px;justify-content:center;align-items:center;flex-wrap:wrap}
.ctl button{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);
 color:var(--ink);border-radius:999px;padding:7px 15px;font-size:13.5px;cursor:pointer;font-family:inherit}
.ctl button.main{background:var(--gold);color:#141625;border-color:var(--gold);font-weight:700}
.ov{position:fixed;inset:0;z-index:20;display:flex;align-items:center;justify-content:center;
 background:rgba(6,9,20,.9);text-align:center;padding:24px}
.ov div{max-width:420px}
.ov h2{color:var(--gold);font-size:20px;margin:0 0 10px}
.ov p{color:var(--dim);font-size:14px;line-height:1.8}
.ov button{margin-top:16px;background:var(--gold);color:#141625;border:0;border-radius:999px;
 padding:12px 30px;font-size:15px;cursor:pointer;font-family:inherit;font-weight:700}
footer{text-align:center;color:var(--dim);font-size:12px;padding:26px 0 0}
</style></head><body>
<canvas id="sky"></canvas>
<div class="wrap">
  <header>
    <div class="lb">__LABEL__</div>
    <h1 id="ttl"></h1>
    <div class="src" id="src"></div>
  </header>
  <section class="panel" id="p-reading"><h2>낭독</h2><div id="reading"></div></section>
  <section class="panel" id="p-sermon"><h2>강론</h2><div id="sermon"></div></section>
  <section class="panel" id="p-song"><h2>노래</h2><div class="ly" id="song"></div></section>
  <section class="panel" id="p-prayer"><h2>기도</h2><div class="pr" id="prayer"></div></section>
  <footer id="ft"></footer>
</div>
<div class="bar"><div class="in">
  <div class="seg">
    <button data-i="0">낭독</button><button data-i="1">강론</button>
    <button data-i="2">노래</button><button data-i="3">기도</button>
  </div>
  <div class="pg" id="pg"><i id="pgi"></i></div>
  <div class="ctl">
    <button id="prev">◀ 이전</button>
    <button id="play" class="main">▶ 재생</button>
    <button id="next">건너뛰기 ▶</button>
    <button id="rep">반복: 전체</button>
    <button id="mute">🔊</button>
  </div>
</div></div>
<div class="ov" id="ov"><div>
  <h2 id="ovt"></h2>
  <p>낭독 · 강론 · 노래 · 기도가 이어서 재생됩니다.</p>
  <button id="start">시작하기</button>
</div></div>
<script>
var DATA = __DATA__;
var $=function(s){return document.querySelector(s)};
function esc(t){return (t||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}

/* ---- 화면 ---- */
$('#ttl').textContent=DATA.title;
$('#src').textContent=DATA.source+'  ('+DATA.citation+')';
$('#ovt').textContent=DATA.title;
$('#ft').textContent=DATA.date+' · 유란시아서 '+DATA.citation;
$('#reading').innerHTML=DATA.reading.map(function(r){
  return '<p class="v"><span class="c">'+esc(r.cit)+'</span>'+esc(r.text)+'</p>'}).join('');
$('#sermon').innerHTML=DATA.sermon.map(function(p){
  return '<p class="v">'+esc(p)+'</p>'}).join('');
$('#song').innerHTML=esc(DATA.lyrics).replace(/\[([^\]]*)\]/g,'<span class="tag">[$1]</span>');
$('#prayer').innerHTML=DATA.prayer.map(function(p){
  return '<p class="v" style="text-align:center">'+esc(p)+'</p>'}).join('');

/* ---- 별 ---- */
(function(){
  var c=$('#sky'),x=c.getContext('2d');
  function draw(){
    var w=c.width=innerWidth,h=c.height=innerHeight;
    x.clearRect(0,0,w,h);
    var ox=w-90,oy=80;
    var g=x.createRadialGradient(ox,oy,0,ox,oy,160);
    g.addColorStop(0,'rgba(255,255,255,.20)');g.addColorStop(1,'rgba(255,255,255,0)');
    x.fillStyle=g;x.beginPath();x.arc(ox,oy,160,0,6.284);x.fill();
    x.fillStyle='__ORB__';x.beginPath();x.arc(ox,oy,43,0,6.284);x.fill();
    var s=12345;
    function rnd(){s=(s*1103515245+12345)%2147483648;return s/2147483648}
    for(var i=0;i<__STARS__;i++){
      var px=rnd()*w,py=rnd()*h*.8,r=rnd()*1.3+.3;
      if((px-ox)*(px-ox)+(py-oy)*(py-oy)<150*150)continue;
      x.fillStyle='rgba(255,255,255,'+(rnd()*.5+.25)+')';
      x.beginPath();x.arc(px,py,r,0,6.284);x.fill();
    }
  }
  draw();addEventListener('resize',draw);
})();

/* ---- 재생 ---- */
var FILES=['01_reading','02_sermon','03_song','04_prayer'];
var PANELS=['#p-reading','#p-sermon','#p-song','#p-prayer'];
var A=new Audio(),cur=0,playing=false,repMode=0,fails=0,retried={}; /* 0 전체 1 이 메뉴 2 없음 */
var REPL=['반복: 전체','반복: 이 메뉴','반복: 없음'];
function mark(){
  PANELS.forEach(function(p,i){$(p).classList.toggle('now',i===cur)});
  document.querySelectorAll('.seg button').forEach(function(b){
    b.classList.toggle('on',+b.dataset.i===cur)});
}
function load(i,go,bust){
  cur=i;mark();
  A.src=DATA.audioBase+FILES[i]+'.mp3'+(bust?('?r='+Date.now()):'');
  A.load();
  $(PANELS[i]).scrollIntoView({behavior:'smooth',block:'start'});
  if(go){var p=A.play();if(p&&p.catch)p.catch(function(){})}
}
function nextSeg(){
  if(repMode===1){load(cur,true);return}
  if(cur<3){load(cur+1,true);return}
  if(repMode===0){load(0,true);return}
  playing=false;$('#play').textContent='▶ 재생';
}
function noSound(){
  playing=false;fails=0;$('#play').textContent='▶ 재생';
  PANELS.forEach(function(p){$(p).classList.remove('now')});
  if(!$('#nosnd')){
    $('#reading').insertAdjacentHTML('beforebegin',
      '<div id="nosnd" style="background:rgba(200,80,80,.18);border:1px solid rgba(200,120,120,.5);'
     +'border-radius:10px;padding:11px 14px;font-size:13.5px;line-height:1.7;margin-bottom:14px">'
     +'소리 파일을 아직 찾지 못했습니다. 음성이 올라간 뒤에 다시 열어 주세요.<br>'
     +'<span style="opacity:.75;font-size:12.5px">'+DATA.audioBase+'01_reading.mp3</span></div>');
  }
}
A.addEventListener('ended',function(){fails=0;nextSeg()});
A.addEventListener('playing',function(){fails=0;retried={}});
A.addEventListener('error',function(){          /* 한 구간이 안 열리면 */
  if(!playing)return;
  if(!retried[cur]){                            /* 먼저 그 구간을 한 번 다시 시도 */
    retried[cur]=1;
    setTimeout(function(){load(cur,true,true)},600);
    return;
  }
  fails++;
  if(fails>=4){noSound();return}               /* 넷 다 없으면 멈추고 알린다 */
  setTimeout(nextSeg,400);
});
A.addEventListener('timeupdate',function(){
  if(A.duration)$('#pgi').style.width=(A.currentTime/A.duration*100)+'%';
});
$('#play').onclick=function(){
  if(playing){A.pause();playing=false;this.textContent='▶ 재생'}
  else{var p=A.play();if(p&&p.catch)p.catch(function(){});playing=true;this.textContent='⏸ 멈춤'}
};
$('#next').onclick=function(){playing=true;$('#play').textContent='⏸ 멈춤';
  if(cur<3)load(cur+1,true);else load(0,true)};
$('#prev').onclick=function(){playing=true;$('#play').textContent='⏸ 멈춤';
  load(cur>0?cur-1:3,true)};
$('#rep').onclick=function(){repMode=(repMode+1)%3;this.textContent=REPL[repMode]};
$('#mute').onclick=function(){A.muted=!A.muted;this.textContent=A.muted?'🔇':'🔊'};
$('#pg').onclick=function(e){
  if(!A.duration)return;
  var r=this.getBoundingClientRect();
  A.currentTime=(e.clientX-r.left)/r.width*A.duration;
};
document.querySelectorAll('.seg button').forEach(function(b){
  b.onclick=function(){playing=true;$('#play').textContent='⏸ 멈춤';load(+this.dataset.i,true)}});
document.addEventListener('keydown',function(e){
  if(e.code==='Space'){e.preventDefault();$('#play').click()}
  if(e.code==='ArrowRight')$('#next').click();
  if(e.code==='ArrowLeft')$('#prev').click();
});
$('#start').onclick=function(){
  $('#ov').style.display='none';playing=true;$('#play').textContent='⏸ 멈춤';load(0,true)};
mark();
</script></body></html>
"""

def main():
    th = NIGHT if content.KIND == "night" else MORNING
    out = TPL
    for k, v in [("__G1__", th["g1"]), ("__G2__", th["g2"]), ("__G3__", th["g3"]),
                 ("__INK__", th["ink"]), ("__DIM__", th["dim"]), ("__GOLD__", th["gold"]),
                 ("__PANEL__", th["panel"]), ("__ORB__", th["orb"]),
                 ("__STARS__", str(th["stars"])), ("__LABEL__", th["label"]),
                 ("__DATE__", content.DATE), ("__TITLE__", esc(content.TITLE))]:
        out = out.replace(k, v)
    out = out.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
    open("index.html", "w", encoding="utf-8").write(out)
    print("index.html 을 만들었습니다. (%s · %s)" % (content.DATE, content.TITLE))

if __name__ == "__main__":
    main()

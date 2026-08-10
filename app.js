/* 공통 도우미 — index.html · list.html · page.html 이 함께 씁니다
   2026-08-10 판: 주소 청소기(cleanUrl)와 맨주소 자동 링크(autoLink)가 들어 있습니다 */

const COLORS = {navy:'#17365D', teal:'#1F6D73', gold:'#B7791F', crimson:'#9E3D35', purple:'#60497A'};

function esc(s){return (s||'').replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));}
function colorOf(g){return COLORS[g && g.color] || COLORS.navy;}

function loadData(){
  return fetch('links.json?v='+Date.now()).then(r=>{ if(!r.ok) throw 0; return r.json(); });
}

/* ── 주소 청소기 ───────────────────────────────────────────
   주소 칸에 무엇이 딸려 들어와도 링크가 살아나게 합니다.
     <https://a.com/>   →  https://a.com/
     "https://a.com"    →  https://a.com
     앞뒤 공백·줄바꿈·보이지 않는 문자 제거
     주소 뒤에 이름이 붙어 있으면 주소 부분만 사용
     http:// 가 빠진  abc.netlify.app  은 https:// 를 붙여 줌          */
function cleanUrl(u){
  if(u===undefined || u===null) return '';
  let s=String(u).replace(/[\u200b-\u200d\ufeff\u00a0]/g,' ').replace(/\s+/g,' ').trim();
  if(!s) return '';
  s=s.replace(/^[<(\[{"'\u2039\u00ab\u201c\u2018]+/,'').replace(/[>)\]}"'\u203a\u00bb\u201d\u2019]+$/,'');
  s=s.split(' ')[0].replace(/[.,;:]+$/,'');
  if(!s) return '';
  if(/^(https?:|mailto:|tel:|#|\/)/i.test(s)) return s;
  if(/^[\w.-]+\.[a-z]{2,}([\/?#]|$)/i.test(s)) return 'https://'+s;
  return s;
}

/* 주소 만들기 —  list.html?g=그룹&i=항목&k=하위  */
function href(gid, i, k){
  let u='list.html?g='+encodeURIComponent(gid);
  if(i!==undefined && i!==null) u+='&i='+i;
  if(k!==undefined && k!==null) u+='&k='+k;
  return u;
}

/* 항목 하나가 어디로 가는지 정한다
   ① 하위가 있으면 → 하위 목록 페이지
   ② 글이 있으면   → 글 페이지
   ③ 그 밖에는     → 주소(없으면 카페 대문)                     */
function hasPage(o){
  return !!((o.text||'').trim() || o.image
         || (o.gallery||[]).length || (o.files||[]).length);
}
function targetOf(o, cafe, gid, i, k){
  if((o.children||[]).length) return {href: href(gid,i,k), ext:false, kind:'list'};
  if(hasPage(o))              return {href: page(gid,i,k),  ext:false, kind:'text'};
  const u=cleanUrl(o.url);
  return {href: u||cafe, ext:true, kind:'url', empty:!u};
}

function page(gid, i, k, j){
  let u='page.html?g='+encodeURIComponent(gid);
  if(i!==undefined && i!==null) u+='&i='+i;
  if(k!==undefined && k!==null) u+='&k='+k;
  if(j!==undefined && j!==null) u+='&j='+j;
  return u;
}

/* 검색용 평면화 — 세 층 전부 */
function flatten(D){
  const out=[], cafe=(D.site||{}).cafeUrl||'#';
  (D.groups||[]).forEach(g=>{
    (g.items||[]).forEach((it,ii)=>{
      let t=targetOf(it,cafe,g.id,ii);
      out.push({n:it.name, path:g.title, href:t.href, ext:t.ext});
      (it.children||[]).forEach((k,ki)=>{
        t=targetOf(k,cafe,g.id,ii,ki);
        out.push({n:k.name, path:g.title+' › '+it.name, href:t.href, ext:t.ext});
        (k.children||[]).forEach((j,ji)=>{
          const has=hasPage(j);
          out.push({n:j.name, path:g.title+' › '+it.name+' › '+k.name,
            href: has? page(g.id,ii,ki,ji) : (cleanUrl(j.url)||cafe), ext: !has});
        });
      });
    });
  });
  return out;
}

/* 사이사이에 끼우는 장식 판 — 코드로 그리는 SVG 라서 이미지 파일이 없습니다 */
const ORN = [
  /* 별자리 */
  c=>'<svg viewBox="0 0 200 120" preserveAspectRatio="xMidYMid slice">'
    +'<line x1="28" y1="86" x2="70" y2="52" stroke="'+c+'" stroke-width="1" opacity=".45"/>'
    +'<line x1="70" y1="52" x2="118" y2="70" stroke="'+c+'" stroke-width="1" opacity=".45"/>'
    +'<line x1="118" y1="70" x2="158" y2="32" stroke="'+c+'" stroke-width="1" opacity=".45"/>'
    +'<line x1="70" y1="52" x2="96" y2="22" stroke="'+c+'" stroke-width="1" opacity=".28"/>'
    +[[28,86,3.2],[70,52,4.6],[118,70,3],[158,32,4],[96,22,2.6],[44,34,1.8],[176,84,2],[136,102,1.6]]
      .map(p=>'<circle cx="'+p[0]+'" cy="'+p[1]+'" r="'+p[2]+'" fill="'+c+'" opacity=".8"/>').join('')
    +'</svg>',
  /* 동심원 — 파라다이스와 하보나 */
  c=>'<svg viewBox="0 0 200 120" preserveAspectRatio="xMidYMid slice">'
    +[52,40,28,17].map((r,i)=>'<circle cx="100" cy="60" r="'+r+'" fill="none" stroke="'+c
      +'" stroke-width="'+(i===3?0:1)+'" opacity="'+(.18+i*.12)+'" '+(i===1?'stroke-dasharray="3 5"':'')+'/>').join('')
    +'<circle cx="100" cy="60" r="8" fill="'+c+'" opacity=".85"/>'
    +'<circle cx="152" cy="60" r="2.6" fill="'+c+'" opacity=".6"/>'
    +'<circle cx="100" cy="20" r="2" fill="'+c+'" opacity=".5"/>'
    +'</svg>',
  /* 동트는 지평선 */
  c=>'<svg viewBox="0 0 200 120" preserveAspectRatio="xMidYMid slice">'
    +'<circle cx="100" cy="78" r="26" fill="'+c+'" opacity=".18"/>'
    +'<circle cx="100" cy="78" r="14" fill="'+c+'" opacity=".55"/>'
    +[0,1,2,3,4,5,6].map(i=>{const a=Math.PI*(1+ i/6);
      return '<line x1="'+(100+Math.cos(a)*32)+'" y1="'+(78+Math.sin(a)*32)
        +'" x2="'+(100+Math.cos(a)*46)+'" y2="'+(78+Math.sin(a)*46)
        +'" stroke="'+c+'" stroke-width="1.4" opacity=".38"/>';}).join('')
    +'<line x1="14" y1="78" x2="186" y2="78" stroke="'+c+'" stroke-width="1.2" opacity=".5"/>'
    +'</svg>',
  /* 펼친 책 */
  c=>'<svg viewBox="0 0 200 120" preserveAspectRatio="xMidYMid slice">'
    +'<path d="M100 38 C84 28 62 26 44 30 L44 88 C62 84 84 86 100 96 Z" fill="none" stroke="'+c+'" stroke-width="1.4" opacity=".6"/>'
    +'<path d="M100 38 C116 28 138 26 156 30 L156 88 C138 84 116 86 100 96 Z" fill="none" stroke="'+c+'" stroke-width="1.4" opacity=".6"/>'
    +'<line x1="100" y1="38" x2="100" y2="96" stroke="'+c+'" stroke-width="1.2" opacity=".45"/>'
    +[46,54,62].map(y=>'<line x1="56" y1="'+y+'" x2="88" y2="'+(y-2)+'" stroke="'+c+'" stroke-width="1" opacity=".22"/>'
      +'<line x1="112" y1="'+(y-2)+'" x2="144" y2="'+y+'" stroke="'+c+'" stroke-width="1" opacity=".22"/>').join('')
    +'<circle cx="100" cy="26" r="3.4" fill="'+c+'" opacity=".7"/>'
    +'</svg>'
];

function ornamentTile(n, color, quote){
  const svg = ORN[n % ORN.length](color);
  return '<div class="orn" style="--oc:'+color+'">'
    + '<div class="art">'+svg+'</div>'
    + (quote ? '<div class="oq">“'+esc(quote.t)+'”<span>'+esc(quote.r)+'</span></div>' : '')
    + '</div>';
}
/* ── 아주 작은 마크다운 변환기 ──────────────────────────
   # 제목 / ## 작은제목 / - 목록 / > 인용 / --- 줄 /
   **굵게** / *기울임* / [글자](주소) / 빈 줄로 문단 나눔
   맨 끝에서 autoLink 를 거치므로 주소를 그냥 붙여넣어도 눌립니다   */
function mdToHtml(src){
  const lines=(src||'').replace(/\r/g,'').split('\n');
  let html='', mode=null;
  const close=()=>{ if(mode==='ul'){html+='</ul>';} if(mode==='p'){html+='</p>';} mode=null; };
  const inline=t=>esc(t)
    .replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>')
    .replace(/(^|[^*])\*([^*]+)\*/g,'$1<i>$2</i>')
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,(m,txt,u)=>{
      const h=cleanUrl(u); if(!h) return m;
      return '<a href="'+h+'" target="_blank" rel="noopener">'+txt+'</a>';
    });
  lines.forEach(raw=>{
    const t=raw.trim();
    if(!t){ close(); return; }
    if(/^---+$/.test(t)){ close(); html+='<hr>'; return; }
    if(/^#\s+/.test(t)){ close(); html+='<h2>'+inline(t.replace(/^#\s+/,''))+'</h2>'; return; }
    if(/^##\s+/.test(t)){ close(); html+='<h3>'+inline(t.replace(/^##\s+/,''))+'</h3>'; return; }
    if(/^>\s?/.test(t)){ close(); html+='<blockquote>'+inline(t.replace(/^>\s?/,''))+'</blockquote>'; return; }
    if(/^[-*]\s+/.test(t)){
      if(mode!=='ul'){ close(); html+='<ul>'; mode='ul'; }
      html+='<li>'+inline(t.replace(/^[-*]\s+/,''))+'</li>'; return;
    }
    if(mode!=='p'){ close(); html+='<p>'; mode='p'; } else { html+='<br>'; }
    html+=inline(t);
  });
  close();
  return autoLink(html);
}

/* ── 맨주소 자동 링크 ───────────────────────────────────
   글 칸에 http… 나 www… 를 그냥 붙여넣어도 눌리게 만듭니다.
   [글자](주소) 로 이미 링크가 된 것은 건드리지 않습니다.       */
function autoLink(html){
  const keep=[];
  html = html.replace(/<a\b[^>]*>[\s\S]*?<\/a>/gi, m=>{
    keep.push(m); return '\u0000'+(keep.length-1)+'\u0000';
  });
  /* 글에  <https://…>  처럼 꺾쇠를 씌워 붙여넣은 경우 꺾쇠를 벗긴다 */
  html = html.replace(/&lt;((?:https?:\/\/|www\.)[^\s<>"']+?)&gt;/gi, '$1');
  html = html.replace(/(^|[\s(>])((?:https?:\/\/|www\.)[^\s<>"'()]+)/gi, function(all, pre, u){
    let tail='';
    u = u.replace(/[.,;:!?]+$/, m=>{ tail=m; return ''; });
    const h = /^www\./i.test(u) ? 'https://'+u : u;
    return pre + '<a href="'+h+'" target="_blank" rel="noopener">'+u+'</a>' + tail;
  });
  return html.replace(/\u0000(\d+)\u0000/g, (m,i)=>keep[+i]);
}

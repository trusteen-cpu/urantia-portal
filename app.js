/* 공통 도우미 — index.html 과 list.html 이 함께 씁니다 */

const COLORS = {navy:'#17365D', teal:'#1F6D73', gold:'#B7791F', crimson:'#9E3D35', purple:'#60497A'};

function esc(s){return (s||'').replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));}
function colorOf(g){return COLORS[g && g.color] || COLORS.navy;}

function loadData(){
  return fetch('links.json?v='+Date.now()).then(r=>{ if(!r.ok) throw 0; return r.json(); });
}

/* 주소 만들기 —  list.html?g=그룹&i=항목&k=하위  */
function href(gid, i, k){
  let u='list.html?g='+encodeURIComponent(gid);
  if(i!==undefined && i!==null) u+='&i='+i;
  if(k!==undefined && k!==null) u+='&k='+k;
  return u;
}

/* 검색용 평면화 — 세 층 전부 */
function flatten(D){
  const out=[], cafe=(D.site||{}).cafeUrl||'#';
  (D.groups||[]).forEach(g=>{
    (g.items||[]).forEach((it,ii)=>{
      const kids=it.children||[];
      out.push({n:it.name, path:g.title,
        href: kids.length? href(g.id,ii) : (it.url||cafe), ext: !kids.length});
      kids.forEach((k,ki)=>{
        const gks=k.children||[];
        out.push({n:k.name, path:g.title+' › '+it.name,
          href: gks.length? href(g.id,ii,ki) : (k.url||cafe), ext: !gks.length});
        gks.forEach(j=>{
          out.push({n:j.name, path:g.title+' › '+it.name+' › '+k.name,
            href: j.url||cafe, ext:true});
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

/* 유란시아서 절 번호(편:장.절)를 누르면 그 절 본문을 띄우는 공용 창.
   쓰는 법: <script src="/bible/ubref.js" data-src="ub.js"></script>
   - UBLINK(html) : 이미 esc된 HTML 안의 74:8.1 · 74:8.1-3 꼴 번호를 누를 수 있는 단추로 바꾼다.
   - 본문은 data-src(UBREF({...}) 꼴)를 처음 누를 때 한 번만 불러온다. */
(function () {
  var me = document.currentScript, SRC = (me && me.dataset.src) || 'ub.js', DATA = null, WAIT = [];
  var PAT = /(^|[^\d:.])(\d{1,3}):(\d{1,2})\.(\d{1,3})(?:-(\d{1,3}))?(?![\d:])/g;
  window.UBLINK = function (h) {
    return (h || '').replace(PAT, function (m, pre, p, c, a, b) {
      var k = p + ':' + c + '.' + a + (b ? '-' + b : '');
      return pre + '<button type="button" class="ubk" data-k="' + k + '" title="유란시아서 ' + k + ' 보기">' + k + '</button>';
    });
  };
  window.UBREF = function (d) { DATA = d; var w = WAIT; WAIT = []; w.forEach(function (f) { f(); }); };
  var css = document.createElement('style');
  css.textContent =
    '.ubk{all:unset;cursor:pointer;color:#9a5a12;font-weight:700;border-bottom:1.5px dotted currentColor;font-family:"맑은 고딕",sans-serif;font-size:.92em;white-space:nowrap}' +
    '.ubk:hover,.ubk:focus-visible{color:#c0392b;border-bottom-style:solid}' +
    'html[data-dark="1"] .ubk{color:#e9c46a}' +
    '#ubPop{position:fixed;inset:0;z-index:2147482000;display:none;align-items:center;justify-content:center;background:rgba(10,16,30,.55);padding:16px}' +
    '#ubPop.on{display:flex}' +
    '#ubPop .bx{background:#fffdf7;color:#20242c;max-width:640px;width:100%;max-height:82vh;overflow:auto;border-radius:16px;box-shadow:0 12px 40px rgba(0,0,0,.35);border-top:5px solid #c9a227}' +
    'html[data-dark="1"] #ubPop .bx{background:#1b1f28;color:#dfe3ea}' +
    '#ubPop .hd{display:flex;align-items:center;gap:8px;padding:12px 16px 8px;position:sticky;top:0;background:inherit;border-bottom:1px solid rgba(0,0,0,.08)}' +
    '#ubPop .hd b{font-family:"맑은 고딕",sans-serif;font-size:15px;color:#7a2e1f}' +
    'html[data-dark="1"] #ubPop .hd b{color:#e9c46a}' +
    '#ubPop .hd span{flex:1;font-size:12px;color:#888;font-family:"맑은 고딕",sans-serif}' +
    '#ubPop .x{all:unset;cursor:pointer;font-size:22px;line-height:1;padding:2px 8px;color:#888}' +
    '#ubPop .vs{padding:12px 18px 6px}' +
    '#ubPop .v{margin:0 0 12px;font-size:16.5px;line-height:1.9;word-break:keep-all;font-family:"Noto Serif KR","Nanum Myeongjo",Georgia,serif}' +
    '#ubPop .v i{font-style:normal;font-family:"맑은 고딕",sans-serif;font-size:12px;font-weight:700;color:#9a743a;margin-right:6px}' +
    '#ubPop .ft{padding:4px 18px 16px;display:flex;gap:10px;flex-wrap:wrap}' +
    '#ubPop .ft a{font-family:"맑은 고딕",sans-serif;font-size:13px;font-weight:700;color:#fff;background:#24466b;padding:7px 14px;border-radius:999px;text-decoration:none}';
  document.head.appendChild(css);
  var pop = document.createElement('div');
  pop.id = 'ubPop';
  pop.innerHTML = '<div class="bx" role="dialog" aria-modal="true"><div class="hd"><b></b><span>유란시아서 새번역본</span><button class="x" type="button" aria-label="닫기">×</button></div><div class="vs"></div><div class="ft"></div></div>';
  function esc(t) { return (t || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function close() { pop.classList.remove('on'); }
  function keys(k) {
    var m = k.match(/^(\d+):(\d+)\.(\d+)(?:-(\d+))?$/), out = [];
    if (!m) return out;
    for (var v = +m[3]; v <= +(m[4] || m[3]) && out.length < 20; v++) out.push(m[1] + ':' + m[2] + '.' + v);
    return out;
  }
  function show(k) {
    var ks = keys(k), first = ks[0];
    pop.querySelector('.hd b').textContent = k;
    pop.querySelector('.vs').innerHTML = ks.map(function (x) {
      return '<p class="v"><i>' + x + '</i>' + esc(DATA[x] || '(본문을 찾지 못했습니다)') + '</p>';
    }).join('');
    pop.querySelector('.ft').innerHTML = '<a href="/bilingual/#' + first + '" target="_blank" rel="noopener">앞뒤 문맥 보기 (한영 대조) ↗</a>';
    pop.classList.add('on');
    pop.querySelector('.x').focus();
  }
  function open(k) {
    if (DATA) { show(k); return; }
    WAIT.push(function () { show(k); });
    if (WAIT.length > 1) return;
    var s = document.createElement('script'); s.src = SRC;
    s.onerror = function () { WAIT = []; alert('유란시아서 본문을 불러오지 못했습니다. 연결을 확인해 주세요.'); };
    document.head.appendChild(s);
  }
  function init() {
    document.body.appendChild(pop);
    pop.addEventListener('click', function (e) { if (e.target === pop || e.target.closest('.x')) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    document.addEventListener('click', function (e) {
      var b = e.target.closest('.ubk[data-k]'); if (!b) return;
      e.preventDefault(); e.stopPropagation(); open(b.dataset.k);
    }, true);
  }
  if (document.body) init(); else document.addEventListener('DOMContentLoaded', init);
})();

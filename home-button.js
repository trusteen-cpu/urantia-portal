/* 모든 하위 페이지 공용 「홈페이지로 가기」 단추.
   페이지 <head>에:  <script src="/home-button.js" defer></script>
   위치 바꾸기:      data-pos="left"(기본 right)   data-top="60"(위에서 px, 기본 10)
   머리 띠 안에 넣기: data-into="header"(그 요소의 맨 앞에 떠 있지 않은 단추로 넣는다) */
(function () {
  if (window.__urHomeBtn) return; window.__urHomeBtn = 1;
  var s = document.currentScript || document.querySelector('script[src*="home-button.js"]');
  var pos = (s && s.dataset.pos) === 'left' ? 'left' : 'right';
  var top = (s && s.dataset.top) || '10';
  var into = s && s.dataset.into;
  function add() {
    if (document.querySelector('.ur-home-btn')) return;
    var st = document.createElement('style');
    st.textContent =
      '.ur-home-btn{position:fixed;top:calc(env(safe-area-inset-top,0px) + ' + top + 'px);' + pos + ':10px;z-index:2147483000;' +
      'display:inline-flex;align-items:center;gap:4px;padding:6px 11px;border-radius:999px;' +
      'background:#ff5a1f;color:#fff!important;border:2px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,.28);' +
      'font:700 12.5px/1.1 "Malgun Gothic","Apple SD Gothic Neo",system-ui,sans-serif;text-decoration:none!important;letter-spacing:0}' +
      '.ur-home-btn.inline{position:static;flex:0 0 auto;margin-right:6px;box-shadow:0 2px 6px rgba(0,0,0,.25)}' +
      '.ur-home-btn:hover{background:#e64a10}' +
      '.ur-home-btn:focus-visible{outline:3px solid #ffd23f;outline-offset:2px}' +
      '@media print{.ur-home-btn{display:none}}';
    document.head.appendChild(st);
    var a = document.createElement('a');
    a.href = '/'; a.className = 'ur-home-btn'; a.title = '홈페이지로 가기';
    a.setAttribute('aria-label', '홈페이지로 가기');
    a.textContent = '🏠 홈페이지로 가기';
    var host = into && document.querySelector(into);
    if (host) { a.className += ' inline'; host.insertBefore(a, host.firstChild); }
    else document.body.appendChild(a);
  }
  if (document.body) add(); else document.addEventListener('DOMContentLoaded', add);
})();

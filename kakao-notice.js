/* 카카오톡 안(인앱 브라우저)에서 열렸을 때만 맨 위에 안내 띠를 보인다.
   페이지 <head>에:  <script src="/kakao-notice.js" defer></script>
   시험용: 주소 끝에 ?kakao=1 을 붙이면 카톡이 아니어도 보인다. */
(function () {
  var ua = navigator.userAgent || '';
  var test = /[?&]kakao=1\b/.test(location.search);
  if (!/KAKAOTALK/i.test(ua) && !test) return;
  function add() {
    if (document.querySelector('.ur-kakao')) return;
    var st = document.createElement('style');
    st.textContent =
      '.ur-kakao{position:relative;z-index:2147482000;background:#fee500;color:#191600;' +
      'font:14px/1.6 "Malgun Gothic","Apple SD Gothic Neo",system-ui,sans-serif;padding:12px 40px 12px 14px;border-bottom:2px solid #d9c400}' +
      '.ur-kakao b{font-weight:800}' +
      '.ur-kakao .go{display:inline-block;margin-top:8px;background:#191600;color:#fee500!important;text-decoration:none!important;' +
      'font-weight:800;font-size:14px;padding:8px 14px;border-radius:999px}' +
      '.ur-kakao .x{position:absolute;right:8px;bottom:8px;background:none;border:0;font-size:22px;line-height:1;color:#191600;cursor:pointer;padding:4px 8px}' +
      /* 떠 있는 홈 단추(오른쪽 위)와 겹치지 않게 첫 줄을 조금 내린다 */
      '.ur-kakao.hb{padding-top:48px}';
    document.head.appendChild(st);
    var d = document.createElement('div');
    d.className = 'ur-kakao'; d.setAttribute('role', 'note');
    var here = location.href.replace(/([?&])kakao=1(&|$)/, '$1').replace(/[?&]$/, '');
    d.innerHTML =
      '<b>카카오톡 안에서는 화면이 제대로 열리지 않거나 멈출 수 있습니다.</b><br>' +
      '아래 단추를 누르거나, 오른쪽 아래(기기에 따라 오른쪽 위) <b>점 세 개 → 「다른 브라우저로 열기」</b>를 눌러 주세요.<br>' +
      '<a class="go" href="kakaotalk://web/openExternal?url=' + encodeURIComponent(here) + '">크롬·사파리로 바로 열기</a>' +
      '<button class="x" type="button" aria-label="안내 닫기">×</button>';
    d.querySelector('.x').onclick = function () { d.remove(); window.dispatchEvent(new Event('resize')); };
    document.body.insertBefore(d, document.body.firstChild);
    window.dispatchEvent(new Event('resize'));
  }
  function fit() {   // 홈 단추가 머리 띠 안이 아니라 떠 있으면 자리를 비운다
    var d = document.querySelector('.ur-kakao'), h = document.querySelector('.ur-home-btn');
    if (d) d.classList.toggle('hb', !!h && !h.classList.contains('inline'));
  }
  if (document.body) add(); else document.addEventListener('DOMContentLoaded', add);
  document.addEventListener('DOMContentLoaded', function () { setTimeout(fit, 0); });
  window.addEventListener('load', fit);
})();

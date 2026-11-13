/* 회원 확인 (2026-11-13) — 모든 페이지 <head> 맨 앞에:  <script src="/auth.js"></script>
   - 첫 화면(/)·가입(/join/)·로그인(/login/)·관리자(/join/admin.html)는 누구나 본다.
   - 첫 화면에서는 메뉴가 다 보이지만, 회원이 아니면 메뉴를 누를 때 가입 안내가 뜬다.
   - 그 밖의 모든 화면은 회원이 아니면 내용 대신 가입 안내를 보인다.
   - 회원 정보는 urantia-members 워커(/api/me)로 확인하고, 30분 동안 이 창에 기억한다.
   이 확인은 브라우저 안에서 하는 것이라, 일부러 자바스크립트를 끄면 지나갈 수 있다(사용자에게 설명함). */
(function () {
  if (window.URAuth) return;
  var API = /^(localhost|127\.0\.0\.1)$/.test(location.hostname) ? '' : 'https://urantia-members.trusteen.workers.dev';
  var TK = 'urToken', NK = 'urName', OK = 'urOkAt';
  function get(s, k) { try { return s.getItem(k) || ''; } catch (e) { return ''; } }
  function set(s, k, v) { try { v == null ? s.removeItem(k) : s.setItem(k, v); } catch (e) {} }
  var A = window.URAuth = {
    api: API,
    token: function () { return get(localStorage, TK); },
    name: function () { return get(localStorage, NK); },
    save: function (t, n) { set(localStorage, TK, t); set(localStorage, NK, n); set(sessionStorage, OK, String(Date.now())); },
    clear: function () { set(localStorage, TK, null); set(localStorage, NK, null); set(sessionStorage, OK, null); },
    headers: function (h) { h = h || {}; var t = A.token(); if (t) h.Authorization = 'Bearer ' + t; return h; },
    logout: function () {
      var t = A.token(); A.clear();
      if (t) fetch(API + '/api/logout', { method: 'POST', headers: { Authorization: 'Bearer ' + t } }).catch(function () {});
      location.href = '/';
    },
    isMember: function () { return !!A.token(); }
  };

  var path = location.pathname.replace(/index\.html$/, '');
  var PUBLIC = ['/', '/join/', '/join/admin.html', '/login/'];
  var isHome = path === '/';
  var isPublic = PUBLIC.indexOf(path) >= 0;
  var root = document.documentElement;
  var next = location.pathname + location.search + location.hash;

  var css = '.ur-gate{position:fixed;inset:0;z-index:2147483600;display:flex;align-items:center;justify-content:center;padding:16px;' +
    'background:rgba(13,23,48,.62);font-family:"Noto Sans KR","Malgun Gothic",system-ui,sans-serif}' +
    'html.ur-wait body,html.ur-lock body{visibility:hidden}html.ur-lock .ur-gate{visibility:visible}' +
    '.ur-gate .bx{max-width:420px;width:100%;background:#fffdf8;border-radius:14px;padding:26px 24px 22px;text-align:center;box-shadow:0 14px 44px rgba(0,0,0,.35);color:#20242e}' +
    '.ur-gate *{text-indent:0;letter-spacing:normal;text-align:center;font-family:inherit;box-sizing:border-box}' +
    '.ur-gate .ic{font-size:34px}.ur-gate h2{margin:6px 0 8px;font-size:20px;color:#17365D}' +
    '.ur-gate p{margin:0 0 16px;font-size:14.5px;line-height:1.7;color:#3b3f4a}' +
    '.ur-gate a{display:block;margin-top:8px;padding:12px;border-radius:9px;font-weight:700;text-decoration:none;font-size:15px}' +
    '.ur-gate a.j{background:#1F6D73;color:#fff}.ur-gate a.l{border:1px solid #1F6D73;color:#1F6D73;background:#fff}' +
    '.ur-gate a.h{color:#6b6f7d;font-weight:400;font-size:13px;padding:6px}.ur-gate .x{float:right;border:0;background:none;font-size:20px;cursor:pointer;color:#6b6f7d;margin:-14px -8px 0 0}' +
    '.ur-who{position:fixed;top:calc(env(safe-area-inset-top,0px) + 10px);left:10px;z-index:2147483000;padding:5px 10px;border-radius:999px;background:rgba(255,255,255,.92);' +
    'border:1px solid #d9d3c4;font:600 12px/1.2 "Malgun Gothic",system-ui,sans-serif;color:#17365D;box-shadow:0 2px 6px rgba(0,0,0,.15)}' +
    '.ur-who a{color:#1F6D73;text-decoration:none;margin-left:6px}@media print{.ur-who,.ur-gate{display:none}}';
  var st = document.createElement('style'); st.textContent = css; (document.head || root).appendChild(st);

  function gate(closable) {
    if (document.querySelector('.ur-gate')) return;
    var top = window.self !== window.top;
    var g = document.createElement('div'); g.className = 'ur-gate';
    var tgt = top ? ' target="_top"' : '';
    var n = encodeURIComponent(top ? '/' : next);
    g.innerHTML = '<div class="bx">' + (closable ? '<button class="x" aria-label="닫기">×</button>' : '') +
      '<div class="ic">📖</div><h2>정회원 전용입니다</h2>' +
      '<p>한국 유란시아서 독자회의 모든 자료는 정회원께 열려 있습니다.<br>정회원으로 가입하시면 바로 보실 수 있습니다.</p>' +
      '<a class="j" href="/join/?next=' + n + '"' + tgt + '>정회원 가입하기</a>' +
      '<a class="l" href="/login/?next=' + n + '"' + tgt + '>이미 회원이에요 — 로그인</a>' +
      (closable ? '' : '<a class="h" href="/"' + tgt + '>홈페이지 첫 화면으로</a>') + '</div>';
    if (closable) {
      g.addEventListener('click', function (e) { if (e.target === g || e.target.className === 'x') g.remove(); });
    }
    root.appendChild(g);
  }

  function badge() {
    if (window.self !== window.top || document.querySelector('.ur-who')) return;
    if (!isHome && path !== '/board/') return;            // 첫 화면과 게시판에만 표시 (다른 화면은 홈 단추와 겹치지 않게)
    var b = document.createElement('div'); b.className = 'ur-who';
    if (A.isMember()) {
      b.innerHTML = '<span></span><a href="#">로그아웃</a>';
      b.firstChild.textContent = A.name() + ' 님';
      b.lastChild.addEventListener('click', function (e) { e.preventDefault(); if (confirm('로그아웃할까요?')) A.logout(); });
    } else if (isHome) {
      b.innerHTML = '<a href="/login/" style="margin:0">로그인</a><a href="/join/">정회원 가입</a>';
    } else return;
    document.body.appendChild(b);
  }
  function whenBody(f) { if (document.body) f(); else document.addEventListener('DOMContentLoaded', f); }

  // 회원 확인: 30분 안에 확인했으면 바로 통과, 아니면 서버에 묻는다.
  function verify(done) {
    var t = A.token();
    if (!t) return done(false);
    var at = Number(get(sessionStorage, OK)) || 0;
    if (Date.now() - at < 30 * 60 * 1000) return done(true);
    fetch(API + '/api/me', { headers: { Authorization: 'Bearer ' + t } })
      .then(function (r) {
        if (r.status === 401 || r.status === 403) { A.clear(); return done(false); }
        if (r.ok) return r.json().then(function (j) { set(localStorage, NK, j.name); set(sessionStorage, OK, String(Date.now())); done(true); });
        done(true);                                         // 서버 문제일 때는 회원을 막지 않는다
      })
      .catch(function () { done(true); });
  }

  if (isPublic) {
    whenBody(badge);
    if (isHome) {
      // 첫 화면: 회원이 아니면 메뉴(링크)를 누를 때 안내를 띄운다.
      document.addEventListener('click', function (e) {
        if (A.isMember()) return;
        var a = e.target.closest && e.target.closest('a[href]');
        if (!a) return;
        var h = a.getAttribute('href') || '';
        if (!h || h.charAt(0) === '#' || /^(mailto:|tel:|javascript:)/i.test(h)) return;
        if (a.closest('.share,.sharebox,#shareBox,#shareBg,.givebg,.ur-gate,.ur-who') || /^share/.test(a.id || '')) return;
        if (/(facebook\.com\/sharer|twitter\.com\/intent|band\.us\/plugin|line\.me\/lineit)/.test(h)) return;
        var u; try { u = new URL(h, location.href); } catch (x) { return; }
        if (u.origin === location.origin && PUBLIC.indexOf(u.pathname.replace(/index\.html$/, '')) >= 0) return;
        e.preventDefault(); e.stopPropagation(); gate(true);
      }, true);
      verify(function () {});                                // 정지된 회원이면 기억을 지운다
    }
    return;
  }

  // 회원 화면
  if (!A.isMember()) { root.classList.add('ur-lock'); whenBody(function () { gate(false); }); return; }
  var at0 = Number(get(sessionStorage, OK)) || 0;
  if (Date.now() - at0 >= 30 * 60 * 1000) root.classList.add('ur-wait');
  verify(function (ok) {
    root.classList.remove('ur-wait');
    if (!ok) { root.classList.add('ur-lock'); whenBody(function () { gate(false); }); }
    else whenBody(badge);
  });
})();

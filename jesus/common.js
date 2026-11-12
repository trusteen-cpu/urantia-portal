/* 예수 연구(3번 메뉴) 공용: 머리 띠 높이, 밝기, 글씨 크기, 목차 열기, 소리 내어 읽기 */
var $ = function (s, r) { return (r || document).querySelector(s) };
var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)) };
function esc(t) { return String(t == null ? '' : t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;') }
function save(k, v) { try { localStorage.setItem(k, v) } catch (e) {} }
function load(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v } catch (e) { return d } }
function flash(t) { var w = $('#warn'); if (!w) return; w.textContent = t; w.style.display = 'block'; clearTimeout(w._t); w._t = setTimeout(function () { w.style.display = 'none' }, 2600) }

(function () {
  function hh() { var h = document.querySelector('header'); if (h) document.documentElement.style.setProperty('--hh', Math.max(0, Math.round(h.getBoundingClientRect().bottom)) + 'px') }
  addEventListener('DOMContentLoaded', hh); addEventListener('load', hh); addEventListener('resize', hh);
  addEventListener('DOMContentLoaded', function () {
    if (window.ResizeObserver) { var h = document.querySelector('header'); if (h) new ResizeObserver(hh).observe(h) }
    function ad() { document.documentElement.setAttribute('data-dark', load('jz_dark', '0')) }
    ad();
    var d = $('#dark'); if (d) d.onclick = function () { save('jz_dark', load('jz_dark', '0') === '1' ? '0' : '1'); ad() };
    var F = ['15.5px', '17.5px', '19.5px', '22px'], fi = +load('jz_fs', '1');
    function af() { document.documentElement.style.setProperty('--fs', F[fi] || F[1]); save('jz_fs', fi) }
    af();
    var f = $('#fs'); if (f) f.onclick = function () { fi = (fi + 1) % F.length; af() };
    var b = $('#burger'); if (b) b.onclick = function () { $('#side').classList.toggle('open') };
    document.addEventListener('click', function (e) {
      var s = $('#side');
      if (s && s.classList.contains('open') && innerWidth <= 900 && !e.target.closest('#side') && !e.target.closest('#burger')) s.classList.remove('open');
    });
  });
})();
function closeSide() { if (innerWidth <= 900) { var s = $('#side'); if (s) s.classList.remove('open') } }

/* ---------- 소리 내어 읽기 (본문 앱과 같은 방식: 구글 음성 → 막히면 브라우저 음성) ---------- */
var TTS = (function () {
  var SPK = window.speechSynthesis, VOICES = [], AUD = new Audio(), GEN = 0, GFAIL = false;
  var SPEEDS = [0.8, 1.0, 1.2, 1.5], si = +load('jz_spd', '1');
  function rate() { return SPEEDS[si] || 1 }
  function clean(t) { return (t || '').replace(/[「」『』\[\]—―·]/g, ' ').replace(/\s+/g, ' ') }
  function sentences(t) {
    var out = [], cur = '', E = '.!?。”"';
    for (var i = 0; i < t.length; i++) { cur += t.charAt(i); if (E.indexOf(t.charAt(i)) >= 0 && (i + 1 >= t.length || t.charAt(i + 1) === ' ')) { out.push(cur); cur = '' } }
    if (cur) out.push(cur); return out
  }
  function chunks(t) {
    var out = [], buf = '';
    sentences(t).forEach(function (s) {
      while (s.length > 190) { out.push(s.slice(0, 190)); s = s.slice(190) }
      if ((buf + ' ' + s).trim().length > 190) { if (buf) out.push(buf.trim()); buf = s } else { buf = (buf + ' ' + s).trim() }
    });
    if (buf) out.push(buf); return out.length ? out : [t]
  }
  function gurl(t) { return 'https://translate.googleapis.com/translate_tts?ie=UTF-8&client=gtx&tl=ko&ttsspeed=1&q=' + encodeURIComponent(t) }
  var FEM = /sunhi|heami|female|google 한국|google korean/i, MAL = /injoon|hyunsu|male/i;
  function vscore(v) { var n = (v.name || ''); return /natural|online/i.test(n) ? 3 : (/google/i.test(n) ? 2 : (v.localService ? 0 : 1)) }
  function fill() {
    if (!SPK) return;
    VOICES = (SPK.getVoices() || []).filter(function (v) { return /^ko/i.test(v.lang) });
    VOICES.sort(function (a, b) { return vscore(b) - vscore(a) });
    var sel = $('#voice'); if (!sel) return; sel.innerHTML = '';
    var o = document.createElement('option'); o.value = 'g'; o.textContent = '기본 음성'; sel.appendChild(o);
    VOICES.forEach(function (v, i) {
      var e = document.createElement('option'); e.value = i;
      e.textContent = (vscore(v) >= 2 ? '★ ' : '') + (v.name || '').replace(/^Microsoft\s+/, '').replace(/\s*-\s*Korean.*$/i, '') + (FEM.test(v.name) ? ' · 여' : (MAL.test(v.name) ? ' · 남' : ''));
      sel.appendChild(e)
    });
    var w = load('jz_voice', 'g'); if (w !== 'g') VOICES.forEach(function (v, i) { if (v.name === w) w = String(i) });
    sel.value = /^\d+$/.test(w) ? w : 'g';
  }
  addEventListener('DOMContentLoaded', function () {
    if (SPK) { SPK.onvoiceschanged = fill; fill() }
    var sel = $('#voice'); if (sel) sel.onchange = function () { save('jz_voice', this.value === 'g' ? 'g' : (VOICES[+this.value] || {}).name || 'g'); stop() };
    var sp = $('#spd'); if (sp) { sp.textContent = rate().toFixed(1) + '×'; sp.onclick = function () { si = (si + 1) % SPEEDS.length; save('jz_spd', si); sp.textContent = rate().toFixed(1) + '×'; try { AUD.playbackRate = rate() } catch (e) {} } }
  });
  AUD.addEventListener('loadedmetadata', function () { AUD.playbackRate = rate() });
  /* cb(끝남 신호)는 한 문단에 꼭 한 번만 — 두 번 불리면 노란 표시가 읽는 곳보다 앞서 나간다 */
  function speak(txt, cb0) {
    var g = GEN, t = clean(txt), sel = $('#voice'), fired = false;
    var cb = function () { if (fired || g !== GEN) return; fired = true; cb0 && cb0() };
    if ((!sel || sel.value === 'g') && !GFAIL) {
      var ps = chunks(t), i = 0, fell = false;
      var fallback = function () {            /* 구글 음성이 막히면 이 문단을 브라우저 음성으로 한 번만 다시 */
        if (fell || g !== GEN) return; fell = true; GFAIL = true;
        AUD.onended = null; AUD.onerror = null; try { AUD.pause() } catch (e) {}
        if (VOICES.length && sel) sel.value = '0';
        speak(t, cb);
      };
      var nx = function () {
        if (g !== GEN || fell) return;
        if (i >= ps.length) { cb(); return }
        AUD.onended = function () { if (g !== GEN || fell) return; i++; nx() };
        AUD.onerror = fallback;
        AUD.src = gurl(ps[i]); AUD.playbackRate = rate();
        var p = AUD.play(); if (p && p.catch) p.catch(fallback);
      };
      nx(); return;
    }
    if (!SPK) { cb(); return }
    var u = new SpeechSynthesisUtterance(t); var v = sel ? VOICES[+sel.value] : null; if (v) u.voice = v;
    u.lang = 'ko-KR'; u.rate = rate();
    u.onend = cb; u.onerror = cb;
    SPK.speak(u);
  }
  var Q = [], QI = -1, ON = null, DONE = null, playing = false;
  function stop() {
    GEN++; playing = false; Q = []; QI = -1;
    try { SPK && SPK.cancel() } catch (e) {}
    try { AUD.pause(); AUD.onended = null; AUD.onerror = null } catch (e) {}
    $$('.now').forEach(function (e) { e.classList.remove('now') });
    var d = DONE; DONE = null; d && d();
  }
  function step() {
    if (!playing) return; QI++;
    $$('.now').forEach(function (e) { e.classList.remove('now') });
    if (QI >= Q.length) { playing = false; var d = DONE; DONE = null; d && d(true); return }
    var it = Q[QI];
    if (it.el) { it.el.classList.add('now'); it.el.scrollIntoView({ block: 'center', behavior: 'smooth' }) }
    ON && ON(it, QI);
    speak(it.t, step);
  }
  /* items: [{t:'읽을 글', el:요소}] , onDone(finished) */
  function play(items, onItem, onDone) { stop(); Q = items; QI = -1; ON = onItem; DONE = onDone; playing = true; step() }
  return { play: play, stop: stop, isPlaying: function () { return playing } };
})();

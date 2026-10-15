(function () {
  /* ---------------------------------------------------------
     1. ヘッダー：KVを過ぎたら白い帯にする
     --------------------------------------------------------- */
  var hd = document.getElementById('hd');
  var kv = document.querySelector('.kv');
  function onScroll() { hd.classList.toggle('is-solid', scrollY > kv.offsetHeight - 60); }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------------------------------------------------------
     2. 予定に入れる：Googleカレンダー／iPhone・Mac（.ics）
        TODO：開場時間が決まったら、終日ではなく時間つきにする
     --------------------------------------------------------- */
  var title = 'THE SNOW CHRISTMAS 2026（MEGURO MARC）', loc = 'MEGURO MARC 東京都品川区西五反田3-3-2', url = 'https://thesnowchristmas.com/';
  var g = document.getElementById('calGoogle');
  g.href = 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + encodeURIComponent(title) +
    '&dates=20261219/20261221&location=' + encodeURIComponent(loc) + '&details=' + encodeURIComponent(url);
  document.getElementById('calApple').href = 'data:text/calendar;charset=utf-8,' + encodeURIComponent(['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//TSC2026//JA', 'BEGIN:VEVENT',
    'UID:tsc2026@thesnowchristmas.com', 'DTSTAMP:20261015T000000Z', 'DTSTART;VALUE=DATE:20261219', 'DTEND;VALUE=DATE:20261221',
    'SUMMARY:' + title, 'LOCATION:' + loc, 'URL:' + url, 'END:VEVENT', 'END:VCALENDAR'].join('\r\n'));

  /* ---------------------------------------------------------
     3. 日時・場所・URL をコピー
     --------------------------------------------------------- */
  function copy(text, btn) {
    function done() { var t = btn.textContent; btn.textContent = 'コピーしました'; btn.classList.add('is-done'); setTimeout(function () { btn.textContent = t; btn.classList.remove('is-done'); }, 1600); }
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
    else { var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); done(); } catch (e) {} ta.remove(); }
  }
  Array.prototype.forEach.call(document.querySelectorAll('[data-copy]'), function (b) {
    b.addEventListener('click', function () { copy(document.getElementById(b.dataset.copy).textContent, b); });
  });

  /* ---------------------------------------------------------
     4. 家族や友だちに送る（スマホは共有シート、PCはまとめてコピー）
     --------------------------------------------------------- */
  var share = document.getElementById('share');
  share.addEventListener('click', function (e) {
    e.preventDefault();
    var text = 'THE SNOW CHRISTMAS 2026\n2026年12月19日（土）・20日（日）\nMEGURO MARC（品川区西五反田3-3-2）入場無料\n';
    if (navigator.share) navigator.share({ title: 'THE SNOW CHRISTMAS 2026', text: text, url: url }).catch(function () {});
    else copy(text + url, share);
  });
})();

/* ---------------------------------------------------------
   5. ボタンに細かい雪の粒子が降る：ふだんは少しずつ、マウスをのせると多く
   --------------------------------------------------------- */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var sel = '.btn:not(:disabled):not(.is-disabled), .hd__cta, .fundlink, .ask summary, .copylist button, .banners a';
  var els = Array.prototype.slice.call(document.querySelectorAll(sel));
  function spark(el, big) {   // 細かい粒子が、ボタンの上から下へゆっくり降る
    var s = document.createElement('i'), w = el.offsetWidth, h = el.offsetHeight;
    s.className = 'grain';
    var size = 1 + Math.random() * (big ? 2 : 1.4);
    s.style.left = (Math.random() * w) + 'px';
    s.style.setProperty('--s', size.toFixed(2) + 'px');
    s.style.setProperty('--d', ((big ? 1.6 : 2.6) + Math.random() * 1.6).toFixed(2) + 's');
    s.style.setProperty('--x', ((Math.random() - 0.5) * 18).toFixed(0) + 'px');
    s.style.setProperty('--h', (h + 8) + 'px');
    s.style.setProperty('--o', (0.55 + Math.random() * 0.45).toFixed(2));
    el.appendChild(s);
    s.addEventListener('animationend', function () { s.remove(); });
  }
  var visible = new Set();
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? visible.add(e.target) : visible.delete(e.target); }); });
    els.forEach(function (el) { io.observe(el); });
  } else els.forEach(function (el) { visible.add(el); });
  els.forEach(function (el) {
    if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
    el.style.overflow = 'hidden';
    el.classList.add('sparkly');
    var t = null;
    el.addEventListener('mouseenter', function () { for (var i = 0; i < 8; i++) spark(el, true); t = setInterval(function () { spark(el, true); spark(el, true); }, 70); });
    el.addEventListener('mouseleave', function () { clearInterval(t); });
  });
  // ふだん：見えているボタンのどれかが、ときどき光る
  setInterval(function () {
    visible.forEach(function (el) { if (Math.random() < 0.8) spark(el, false); });
  }, 260);
})();

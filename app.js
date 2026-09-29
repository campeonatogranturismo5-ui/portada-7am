(function () {
  'use strict';
  var TZ = 'Europe/Madrid';
  var SECTIONS = [
    { key: 'politica', name: 'Política' },
    { key: 'exterior', name: 'Exterior' },
    { key: 'tecnologia', name: 'Tecnología' },
    { key: 'economia', name: 'Economía' },
    { key: 'cultura', name: 'Cultura' }
  ];

  function parts(iso, opts) {
    var d = new Date(iso);
    if (!iso || isNaN(d)) return null;
    var o = { timeZone: TZ };
    for (var k in opts) o[k] = opts[k];
    var p = {};
    new Intl.DateTimeFormat('es-ES', o).formatToParts(d).forEach(function (x) { p[x.type] = x.value; });
    return p;
  }
  function longDate(iso) {
    var p = parts(iso, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
    return p ? p.weekday + ', ' + p.day + ' de ' + p.month + ' de ' + p.year : '';
  }
  function hhmm(iso) {
    var p = parts(iso, { hour: '2-digit', minute: '2-digit', hour12: false });
    return p ? p.hour + ':' + p.minute : '';
  }
  function shortStamp(iso) {
    var p = parts(iso, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit', hour12: false });
    return p ? p.day + ' ' + (p.month || '').replace('.', '').replace(/^sept$/, 'sep') + ' · ' + p.hour + ':' + p.minute : '';
  }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function detailUrl(item) { return 'noticia.html?id=' + encodeURIComponent(item.id || ''); }

  function story(item, cls) {
    var art = el('article', 'story ' + cls);
    var meta = el('div', 'meta');
    meta.appendChild(el('span', 'source', item.source || ''));
    if (item.lang === 'en') meta.appendChild(el('span', 'lang', 'Fuente en inglés'));
    var t = shortStamp(item.publishedAt);
    if (t) {
      var time = el('time', 'time', t);
      time.setAttribute('datetime', item.publishedAt);
      meta.appendChild(time);
    }
    art.appendChild(meta);
    var href = detailUrl(item);
    var h = el('h3');
    var a = el('a', null, item.title || '');
    a.href = href;
    h.appendChild(a);
    art.appendChild(h);
    if (item.summary) art.appendChild(el('p', null, item.summary));
    var r = el('a', 'read', 'Leer');
    r.href = href;
    r.setAttribute('aria-label', 'Leer: ' + (item.title || ''));
    art.appendChild(r);
    art.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.target.closest('a')) return;
      if (window.getSelection && String(window.getSelection())) return;
      location.href = href;
    });
    return art;
  }

  function render(data) {
    document.getElementById('fecha').textContent = longDate(data.updatedAt);
    var upd = document.getElementById('actualizado');
    upd.textContent = '';
    upd.appendChild(document.createTextNode('Actualizado a las '));
    upd.appendChild(el('strong', null, hhmm(data.updatedAt) || '--:--'));
    var main = document.getElementById('contenido');
    var n = 0;
    SECTIONS.forEach(function (s) {
      var sec = data.sections && data.sections[s.key];
      var items = sec && sec.published ? sec.published.slice(0, 5) : [];
      if (!items.length) return;
      n++;
      var box = el('section', 'section');
      box.id = s.key;
      var head = el('div', 'section-head');
      head.appendChild(el('span', 'num', ('0' + n).slice(-2)));
      head.appendChild(el('h2', null, s.name));
      box.appendChild(head);
      box.appendChild(story(items[0], 'featured'));
      var grid = el('div', 'grid');
      items.slice(1).forEach(function (it) { grid.appendChild(story(it, 'small')); });
      box.appendChild(grid);
      main.appendChild(box);
    });
    if (!n) fail(new Error('sin noticias'));
    spy();
  }

  function fail(err) {
    document.getElementById('actualizado').textContent = 'No se pudo cargar la portada';
    document.getElementById('estado').textContent =
      'No se han podido cargar las noticias (' + (err && err.message ? err.message : 'error') + '). Vuelve a intentarlo en unos minutos.';
  }

  function spy() {
    if (!('IntersectionObserver' in window)) return;
    var links = {};
    document.querySelectorAll('.sections-nav a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && links[e.target.id]) {
          Object.keys(links).forEach(function (k) { links[k].classList.remove('active'); });
          links[e.target.id].classList.add('active');
        }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    document.querySelectorAll('.section').forEach(function (s) { io.observe(s); });
  }

  fetch('news.json?t=' + Date.now(), { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(render)
    .catch(fail);
})();

(function () {
  'use strict';
  var TZ = 'Europe/Madrid';
  var NAMES = { politica: 'Política', exterior: 'Exterior', tecnologia: 'Tecnología', economia: 'Economía', cultura: 'Cultura' };
  var PARCIAL = 'Resumen parcial: el artículo original es de pago o tenía poco contexto.';

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
  function stamp(iso) {
    var p = parts(iso, { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false });
    return p ? p.day + ' de ' + p.month + ' de ' + p.year + ' · ' + p.hour + ':' + p.minute + ' (hora de Madrid)' : '';
  }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function safeUrl(u) { return /^https?:\/\//i.test(u || '') ? u : null; }
  function getId() {
    var m = /[?&]id=([^&#]*)/.exec(location.search);
    try { return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')).trim() : ''; } catch (e) { return ''; }
  }
  function find(data, id) {
    var secs = (data && data.sections) || {};
    var keys = Object.keys(secs), i, list, j;
    var lists = ['published', 'pool'];
    for (var l = 0; l < lists.length; l++) {
      for (i = 0; i < keys.length; i++) {
        list = (secs[keys[i]] && secs[keys[i]][lists[l]]) || [];
        for (j = 0; j < list.length; j++) {
          if (list[j] && list[j].id === id) return { item: list[j], section: list[j].section || keys[i] };
        }
      }
    }
    return null;
  }
  function markNav(sec) {
    document.querySelectorAll('.sections-nav a').forEach(function (a) {
      if (a.getAttribute('data-sec') === sec) a.classList.add('active');
    });
  }
  function backLink(sec) {
    var a = el('a', 'back', '← Volver a portada');
    a.href = 'index.html' + (sec ? '#' + sec : '');
    return a;
  }

  function notFound(msg) {
    document.title = 'Noticia no encontrada · Portada 7AM';
    var box = document.getElementById('ficha');
    box.innerHTML = '';
    box.appendChild(backLink());
    var h = el('h1', null, 'Noticia no encontrada');
    box.appendChild(h);
    box.appendChild(el('p', 'lede', msg));
  }

  function render(data) {
    document.getElementById('fecha').textContent = longDate(data.updatedAt);
    var id = getId();
    if (!id) return notFound('Falta el identificador de la noticia. Vuelve a la portada y elige una historia.');
    var hit = find(data, id);
    if (!hit) return notFound('No encontramos ninguna noticia con el identificador «' + id + '». Puede que ya no esté en la selección de hoy.');
    var it = hit.item, sec = hit.section;
    document.title = (it.title || 'Noticia') + ' · Portada 7AM';
    markNav(sec);

    var box = document.getElementById('ficha');
    box.innerHTML = '';
    var top = backLink(sec); top.classList.add('top');
    box.appendChild(top);

    var meta = el('div', 'meta');
    if (NAMES[sec]) meta.appendChild(el('span', 'section-tag', NAMES[sec]));
    meta.appendChild(el('span', 'source', it.source || ''));
    if (it.lang === 'en') meta.appendChild(el('span', 'lang', 'Fuente en inglés'));
    var t = stamp(it.publishedAt);
    if (t) {
      var time = el('time', 'time', t);
      time.setAttribute('datetime', it.publishedAt);
      meta.appendChild(time);
    }
    box.appendChild(meta);
    box.appendChild(el('h1', null, it.title || ''));
    if (it.summary) box.appendChild(el('p', 'lede', it.summary));
    if (it.longSummary) box.appendChild(el('p', 'long', it.longSummary));

    var bullets = Array.isArray(it.bullets) ? it.bullets.filter(Boolean) : [];
    if (bullets.length) {
      box.appendChild(el('h2', null, 'Puntos clave'));
      var ul = el('ul', 'puntos');
      bullets.forEach(function (b) { ul.appendChild(el('li', null, b)); });
      box.appendChild(ul);
    }
    if (it.partial === true) box.appendChild(el('p', 'parcial', PARCIAL));

    var acc = el('div', 'acciones');
    var url = safeUrl(it.url);
    if (url) {
      var a = el('a', 'btn-fuente', 'Abrir original');
      a.href = url; a.target = '_blank'; a.rel = 'noopener';
      a.setAttribute('aria-label', 'Abrir original en ' + (it.source || 'la fuente') + ' (pestaña nueva)');
      acc.appendChild(a);
    }
    acc.appendChild(backLink(sec));
    box.appendChild(acc);
  }

  function fail(err) {
    document.title = 'Portada 7AM';
    var e = document.getElementById('estado');
    if (e) e.textContent = 'No se ha podido cargar la noticia (' + (err && err.message ? err.message : 'error') + '). Vuelve a intentarlo en unos minutos.';
  }

  fetch('news.json?t=' + Date.now(), { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(render)
    .catch(fail);
})();

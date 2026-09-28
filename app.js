(function () {
  var TZ = 'Europe/Madrid';
  function fmt(iso, withWeekday) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d)) return '';
    var opts = { timeZone: TZ, day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false };
    if (withWeekday) opts.weekday = 'long';
    var parts = new Intl.DateTimeFormat('es-ES', opts).formatToParts(d);
    var p = {};
    parts.forEach(function (x) { p[x.type] = x.value; });
    var month = (p.month || '').replace('.', '');
    return (withWeekday ? p.weekday + ' ' : '') + p.day + ' ' + month + ' ' + p.year + ', ' + p.hour + ':' + p.minute;
  }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function render(data) {
    document.getElementById('updated').textContent = 'Actualizado: ' + (fmt(data.updated, true) || 'desconocido');
    var grid = document.getElementById('grid');
    grid.innerHTML = '';
    (data.items || []).forEach(function (it, i) {
      var li = el('li', 'card');
      var meta = el('div', 'meta');
      meta.appendChild(el('span', 'num', '#' + (i + 1)));
      meta.appendChild(el('span', 'medio', it.medio || ''));
      li.appendChild(meta);
      li.appendChild(el('h2', null, it.titular || ''));
      if (it.resumen) li.appendChild(el('p', null, it.resumen));
      var f = fmt(it.fecha, false);
      if (f) li.appendChild(el('span', 'fecha', f));
      if (it.enlace) {
        var a = el('a', null, 'Leer en ' + (it.medio || 'la fuente') + ' →');
        a.href = it.enlace; a.target = '_blank'; a.rel = 'noopener noreferrer';
        li.appendChild(a);
      }
      grid.appendChild(li);
    });
  }
  function fail(err) {
    document.getElementById('updated').textContent = 'No se pudo cargar la portada';
    var s = document.getElementById('status');
    s.className = 'msg';
    s.textContent = 'No se han podido cargar las noticias (' + (err && err.message ? err.message : 'error') + '). Inténtalo de nuevo en unos minutos.';
  }
  fetch('news.json?t=' + Date.now(), { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(render)
    .catch(fail);
})();

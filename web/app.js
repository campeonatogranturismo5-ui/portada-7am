(()=>{'use strict';
const $=s=>document.querySelector(s), all=s=>[...document.querySelectorAll(s)];
const store={get(k,f){try{return JSON.parse(localStorage.getItem(k))??f}catch{return f}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v));return true}catch{return false}}};
let saved=new Set(store.get('p7-saved',[]));
let theme=store.get('p7-theme',matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
document.documentElement.dataset.theme=theme;
function notice(t){$('#notice').textContent=t;setTimeout(()=>$('#notice').textContent='',3500)}
$('#theme')?.addEventListener('click',()=>{theme=theme==='dark'?'light':'dark';document.documentElement.dataset.theme=theme;store.set('p7-theme',theme)});
function refresh(){all('[data-save]').forEach(b=>{let on=saved.has(b.dataset.save);b.setAttribute('aria-pressed',String(on));b.textContent=on?'Guardada ✓':'Guardar'});if($('#saved-count'))$('#saved-count').textContent=saved.size?`(${saved.size})`:'';all('.saved-grid .story').forEach(el=>el.hidden=!saved.has(el.dataset.id));if($('#saved-empty'))$('#saved-empty').hidden=all('.saved-grid .story').some(el=>!el.hidden)}
all('[data-save]').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.save;saved.has(id)?saved.delete(id):saved.add(id);if(!store.set('p7-saved',[...saved]))notice('Este navegador no permite guardar la lista.');refresh()}));refresh();
all('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(b.dataset.copy);notice('Enlace copiado')}catch{notice('No se pudo copiar. Puedes copiar la dirección del navegador.')}}));
all('[data-edition]').forEach(el=>{const age=Date.now()-Date.parse(el.dataset.edition);if(age>36*3600000){el.textContent='Edición desactualizada · Se conserva la última publicación válida';el.classList.add('stale')}else el.textContent='Resúmenes automáticos · Fuentes enlazadas'});
if($('#search')){fetch('/search.json').then(r=>r.json()).then(data=>{const byId=new Map(data.map(x=>[x.id,x]));const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();function filter(){const q=norm($('#search').value.trim()),day=$('#date-filter').value;let count=0;all('.archive-grid .story').forEach(el=>{const d=byId.get(el.dataset.id);let visible=d&&norm(d.title+' '+d.summary+' '+d.source).includes(q)&&(!day||new Intl.DateTimeFormat('sv-SE',{timeZone:'Europe/Madrid'}).format(new Date(d.publishedAt))===day);el.hidden=!visible;if(visible)count++});$('#results-count').textContent=`${count} noticias encontradas`;}$('#search').addEventListener('input',filter);$('#date-filter').addEventListener('input',filter);filter()}).catch(()=>notice('No se pudo cargar el buscador. Las noticias siguen disponibles.'))}
})();

"""Generate crawlable HTML, permanent articles and dated editions without dependencies."""
import html
import json
import shutil
from pathlib import Path
from pipeline import ROOT, SECTIONS, read, write, date, validate_edition

def esc(value): return html.escape(str(value),quote=True)
def stamp(value): return date(value).astimezone(__import__('pipeline').TZ).strftime('%d/%m/%Y · %H:%M')

def build(root=ROOT):
    config=read(root/'data/config.json')
    base=config['siteUrl'].rstrip('/')
    out=root/'dist'
    out.mkdir(exist_ok=True)
    archive=read(root/'data/archive.json',{})
    legacy=read(root/'data/legacy-news.json',{})
    aliases={}
    for section,block in legacy.get('sections',{}).items():
        for old in block.get('pool',[]):
            from pipeline import digest
            key='legacy-'+digest(old['url'])
            aliases.setdefault(old['id'],key)
            archive.setdefault(key,{**old,'id':key,'section':{'politica':'espana','exterior':'internacional'}.get(section,section),'paragraphs':[old.get('longSummary','')], 'legacy':True})
    current=read(root/'data/current.json')
    if current: validate_edition(current)
    else:
        current={'updatedAt':legacy['updatedAt'],'date':legacy['updatedAt'][:10],'sections':{s:[] for s in SECTIONS},'legacy':True}
        for section,block in legacy.get('sections',{}).items():
            current['sections'][{'politica':'espana','exterior':'internacional'}.get(section,section)]=[archive[aliases[x['id']]] for x in block.get('published',[])]

    def page(title,description,body,path='/',updated=None):
        return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · Portada 7AM</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{base}{path}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{base}{path}"><meta property="og:type" content="{'article' if path.startswith('/noticias/') else 'website'}"><meta property="og:locale" content="es_ES"><meta name="twitter:card" content="summary"><meta name="color-scheme" content="light dark"><link rel="stylesheet" href="/styles.css"><script src="/app.js" defer></script></head><body><a class="skip" href="#contenido">Saltar al contenido</a><header><div class="wrap topbar"><a class="brand" href="/">PORTADA <span>7AM</span></a><div class="tools"><a href="/archivo/">Archivo</a><a href="/guardadas/">Guardadas <span id="saved-count"></span></a><button id="theme" aria-label="Cambiar modo claro u oscuro">◐</button></div></div><div class="wrap strap"><span>UNA MIRADA AL DÍA</span><span>Castellano · Fuentes diversas</span></div></header><nav aria-label="Secciones"><div class="wrap">{''.join(f'<a href="/#{s}">{n}</a>' for s,n in SECTIONS.items())}</div></nav><main class="wrap" id="contenido">{body}</main><footer class="wrap"><a class="brand" href="/">PORTADA <span>7AM</span></a><p>Selección y resúmenes automáticos. Pueden contener errores; contrasta los datos con las fuentes originales.</p><p>Un proyecto personal de lectura, sin cuentas. Las noticias y sus derechos pertenecen a sus medios. <a href="/acerca/">Cómo funciona</a></p></footer><div id="notice" role="status" aria-live="polite"></div></body></html>'''

    def save(path,text):
        dest=out/path
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(text,encoding='utf-8')

    def card(item):
        return f'''<article class="story" data-id="{esc(item['id'])}"><div class="meta">{esc(item['source'])} <span>· {stamp(item['publishedAt'])}</span></div><h3><a href="/noticias/{item['id']}/">{esc(item['title'])}</a></h3><p>{esc(item['summary'])}</p><div class="card-bottom"><a class="read" href="/noticias/{item['id']}/">Leer resumen <span>→</span></a><button class="save" data-save="{item['id']}" aria-label="Guardar: {esc(item['title'])}" aria-pressed="false">Guardar</button></div></article>'''

    def edition_body(edition,archived=False):
        highlights=[items[0] for items in edition['sections'].values() if items][:5]
        body=f'<div class="edition"><p>{"EDICIÓN ARCHIVADA" if archived else "LA EDICIÓN"} · <time datetime="{edition["updatedAt"]}">{stamp(edition["updatedAt"])}</time></p><p data-edition="{edition["updatedAt"]}" class="freshness">Fecha real de publicación</p></div>'
        if edition.get('legacy'): body+='<p class="alert">Edición heredada del proyecto original. La nueva actualización automática todavía no ha publicado su primera edición.</p>'
        body+='<section class="highlights"><div><p class="eyebrow">EL DÍA, EN PERSPECTIVA</p><h1>Lo importante<br>de hoy<span>.</span></h1><p>Las claves de distintas secciones, con sus fuentes a un clic.</p></div><ol>'+''.join(f'<li><span>{SECTIONS[x["section"]]}</span><a href="/noticias/{x["id"]}/">{esc(x["title"])}</a></li>' for x in highlights)+'</ol></section>'
        for section,items in edition['sections'].items():
            body+=f'<section class="news-section" id="{section}"><div class="section-title"><h2>{SECTIONS[section]}</h2><span>{len(items):02d}</span></div><div class="grid">'+(''.join(card(x) for x in items) if items else '<p class="empty">No hay noticias nuevas verificadas en esta edición.</p>')+'</div></section>'
        return body

    save('index.html',page('Las noticias, con contexto','Noticias en castellano de Euskadi, España, internacional, ciencia, tecnología, economía y cultura.',edition_body(current)))
    for item in archive.values():
        key=item['id']; path=f'/noticias/{key}/'
        lang={'es':'castellano','en':'inglés','eu':'euskera','fr':'francés'}.get(item['lang'],item['lang'])
        body=f'<article class="article" data-id="{key}"><a class="back" href="/">← Volver a portada</a><p class="eyebrow">{SECTIONS.get(item["section"],item["section"])}</p><h1>{esc(item["title"])}</h1><p class="article-meta">{esc(item["source"])} · Fuente en {esc(lang)} · <time datetime="{item["publishedAt"]}">{stamp(item["publishedAt"])}</time></p><p class="lede">{esc(item["summary"])}</p>'
        if item.get('legacy'): body+='<p class="alert">Noticia del archivo original. Se conserva para mantener los enlaces anteriores; no es una noticia recién publicada.</p>'
        body+='<div class="prose">'+''.join(f'<p>{esc(p)}</p>' for p in item['paragraphs'])+'</div><h2>Puntos clave</h2><ul class="points">'+''.join(f'<li>{esc(b)}</li>' for b in item['bullets'])+'</ul>'
        if item.get('partial') or item.get('parcial'): body+='<p class="partial"><strong>Resumen parcial.</strong> Elaborado con el material público disponible. El original puede aportar más detalles.</p>'
        body+=f'<a class="original" href="{esc(item["url"])}" rel="noopener noreferrer" target="_blank">Leer noticia original ↗<small>{esc(item["source"])} · {esc(lang)}</small></a><div class="actions"><button class="save" data-save="{key}" aria-pressed="false">Guardar para después</button><a href="https://wa.me/?text={__import__("urllib.parse",fromlist=["quote"]).quote(item["title"]+" "+base+path)}" target="_blank" rel="noopener noreferrer">Compartir por WhatsApp</a><button data-copy="{base}{path}">Copiar enlace</button></div><p class="disclosure">Resumen automático. Fecha de la fuente: {stamp(item["publishedAt"])}.</p></article>'
        structured={'@context':'https://schema.org','@type':'NewsArticle','headline':item['title'],'description':item['summary'],'datePublished':item['publishedAt'],'inLanguage':'es-ES','url':base+path,'isBasedOn':item['url'],'author':{'@type':'Organization','name':'Portada 7AM — resumen automático'}}
        body+='<script type="application/ld+json">'+json.dumps(structured,ensure_ascii=False).replace('<','\\u003c')+'</script>'
        save(f'noticias/{key}/index.html',page(item['title'],item['summary'],body,path))
    editions=sorted((root/'data/editions').glob('*.json'),reverse=True) if (root/'data/editions').exists() else []
    archive_body='<div class="page-heading"><p class="eyebrow">PARA VOLVER A LO IMPORTANTE</p><h1>Archivo y buscador</h1><label for="search">Buscar en titulares y resúmenes</label><input id="search" type="search" placeholder="Tema, lugar o medio…"><label for="date-filter">Fecha de la noticia</label><input id="date-filter" type="date"></div><div class="edition-links">'
    for f in editions:
        edition=read(f); path=f'/ediciones/{f.stem}/'
        save(f'ediciones/{f.stem}/index.html',page('Edición '+f.stem,'Edición archivada de Portada 7AM',edition_body(edition,True),path))
        archive_body+=f'<a href="{path}">{f.stem}</a> '
    archive_body+='</div><p id="results-count" role="status"></p><div class="grid archive-grid">'
    sorted_items=sorted(archive.values(),key=lambda x:x['publishedAt'],reverse=True)
    archive_body+=''.join(card(x) for x in sorted_items)+'</div>'
    save('archivo/index.html',page('Archivo','Busca noticias y consulta ediciones anteriores.',archive_body,'/archivo/'))
    save('guardadas/index.html',page('Guardadas','Tu lista de lectura, guardada solo en este navegador.','<div class="page-heading"><h1>Para leer después</h1><p>Guardadas en este navegador, sin crear una cuenta.</p></div><p id="saved-empty">Todavía no has guardado noticias.</p><div class="grid saved-grid">'+''.join(card(x) for x in sorted_items)+'</div>','/guardadas/'))
    save('acerca/index.html',page('Cómo funciona','Fuentes, resúmenes automáticos y límites.', '<article class="article"><h1>Una mirada al día</h1><p>Portada 7AM es un proyecto personal de lectura. Consulta fuentes RSS públicas, selecciona noticias recientes y genera resúmenes propios en castellano con Gemini. Cada ficha identifica el medio, el idioma y la fecha del original.</p><h2>Transparencia</h2><p>Los resúmenes se revisan automáticamente frente al material consultado, pero pueden contener errores. Los extractos se marcan como resúmenes parciales. No se sortean muros de pago y no se reproducen artículos completos.</p><h2>Actualización</h2><p>La edición se programa alrededor de las 07:00 de Europe/Madrid. Los servicios gratuitos pueden retrasar o suspender ejecuciones. Ante errores se mantiene la última edición válida con su fecha real. No se garantiza disponibilidad ilimitada.</p><h2>Privacidad</h2><p>El tema visual y la lista de lectura se guardan localmente en tu navegador. No necesitas cuenta. WhatsApp solo se abre si decides compartir. El alojamiento puede registrar datos técnicos de acceso.</p></article>','/acerca/'))
    save('noticia.html',page('Noticia del archivo','Enlace antiguo de Portada 7AM.','<article class="article"><h1>Abriendo noticia del archivo</h1><p id="legacy-status">Si no se abre automáticamente, busca la noticia en el <a href="/archivo/">archivo</a>.</p></article><script src="/legacy.js" defer></script>','/noticia.html'))
    write(out/'legacy-aliases.json',aliases)
    save('legacy.js',"fetch('/legacy-aliases.json').then(r=>r.json()).then(a=>{const id=new URLSearchParams(location.search).get('id');if(a[id])location.replace('/noticias/'+a[id]+'/');});")
    write(out/'news.json',current)
    write(out/'search.json',[{k:x[k] for k in ('id','title','summary','source','publishedAt')} for x in sorted_items])
    for name in ('styles.css','app.js'): shutil.copyfile(root/'web'/name,out/name)
    save('robots.txt',f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n')
    save('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{esc(base+path)}</loc></url>' for path in ['/', '/archivo/']+[f'/noticias/{k}/' for k in archive])+'</urlset>')
    print('HTML generado:',len(archive),'fichas permanentes')

if __name__=='__main__': build()

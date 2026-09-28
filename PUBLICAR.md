# Portada 7AM — Cómo actualizar y republicar (v2, portada por secciones)

## Datos fijos
- **URL pública:** https://portada-7am.vercel.app/ (200, sin protección de Vercel)
- **Repo GitHub (público):** https://github.com/campeonatogranturismo5-ui/portada-7am
  - owner `campeonatogranturismo5-ui` · repo `portada-7am` · rama `main`
- **Vercel:** proyecto `portada-7am` (id `prj_vARAnlnxjlEc4XjkH5SEmbCBzvNH`), team `enriquelebrijo-2398s-projects`
  (id `team_g3dcU0xCcjzgBwnhMbeDs1oW`). Enlazado por Git: **cada push a `main` despliega a producción solo** (~30 s).
- Copia de trabajo en la box: `/workspace/portada-7am` (capturas en `shots/`, NO se suben).
- Herramientas: conector MCP GitHub `user-GitHub-xai` (`push_files`) y conector Vercel `user-Vercel-xai`.
  `gh` NO está autenticado; `vercel` CLI no instalado. No iniciar logins.
- Ficheros del sitio: `index.html`, `styles.css`, `app.js` (lee `news.json?t=<timestamp>`), `news.json`, `Briefing/log.md`.

## Fuentes por sección (probadas el 28/09/2026)
| Sección | Fuentes pedidas | Estado | Fallback que funcionó |
|---|---|---|---|
| Política | El País, BBC Mundo, Reuters | El País ✅ BBC Mundo ✅ Reuters ❌ 401 | Europa Press ✅, elDiario.es ✅ |
| Tecnología | The Verge, TechCrunch, El País Tecnología | ✅ ✅ ✅ (El País Tec: poco volumen, 1 noticia/día) | Ars Technica ✅, Xataka ✅ |
| Economía | Expansión, Reuters Business, Cinco Días | ✅ ❌ 401 ✅ | El País Economía ✅, Financial Times RSS ✅ (artículos con muro de pago), BBC Business ✅. El Confidencial ❌ (reto JS 403 en artículos), El Economista ❌ 403 |
| Cultura | El País Cultura, BBC Culture, The Guardian Culture | ✅ BBC Culture ⚠️ (feed con 1 artículo) ✅ | BBC News Entertainment & Arts ✅ |

Feeds:
- El País España: `https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada`
- El País Internacional: `.../section/internacional/portada` · Tecnología: `.../section/tecnologia/portada` · Cultura: `.../section/cultura/portada`
- Cinco Días: `https://feeds.elpais.com/mrss-s/pages/ep/site/cincodias.elpais.com/portada`
- BBC Mundo: `https://feeds.bbci.co.uk/mundo/rss.xml`
- BBC Culture: `https://www.bbc.com/culture/feed.rss` · BBC Ent&Arts: `https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml` · BBC Business: `https://feeds.bbci.co.uk/news/business/rss.xml`
- The Verge: `https://www.theverge.com/rss/index.xml` · TechCrunch: `https://techcrunch.com/feed/`
- Ars Technica: `https://feeds.arstechnica.com/arstechnica/index` · Xataka: `https://www.xataka.com/feedburner.xml`
- Expansión: `https://e00-expansion.uecdn.es/rss/portada.xml` (codificación ISO-8859-1)
- Guardian Culture: `https://www.theguardian.com/culture/rss`
- Europa Press nacional: `https://www.europapress.es/rss/rss.aspx?ch=00066` · elDiario.es política: `https://www.eldiario.es/rss/politica/`
- FT: `https://www.ft.com/rss/home`

Consejos: usar User-Agent de navegador (Chrome Windows) + `Accept-Language: es-ES`. El País devuelve 403 si se piden
muchos artículos en paralelo: pedirlos de uno en uno con 2-4 s de pausa. La fecha sale de `"datePublished"` (convertir a +02:00 / +01:00).

## Reglas editoriales
- 10 candidatos por sección en `pool` (40 en total), frescos (24-48 h), mezclando medios; sin duplicar la misma historia entre secciones.
- `published` = copia de los 5 más relevantes del `pool` (el primero es la noticia destacada grande). Los otros 5 quedan de reserva.
- Títulos en español (traducción fiel si la fuente es inglesa). Resumen: 1 frase en español basada SOLO en el texto del artículo
  (og:description / entradilla / primeros párrafos). Nunca inventar. Verificar que cada URL responde 200 y es un artículo real.

## Forma exacta de news.json
```json
{
  "updatedAt": "2026-09-28T20:08:00+02:00",
  "timezone": "Europe/Madrid",
  "sections": {
    "politica":   {"published": [5 items], "pool": [10 items]},
    "tecnologia": {"published": [...], "pool": [...]},
    "economia":   {"published": [...], "pool": [...]},
    "cultura":    {"published": [...], "pool": [...]}
  }
}
```
Item: `{"id":"pol-01","title":"…","summary":"…","source":"El País","url":"https://…","section":"politica","publishedAt":"2026-09-28T14:19:06+02:00"}`
(ids: `pol-NN`, `tec-NN`, `eco-NN`, `cul-NN`). `updatedAt` con `date +%Y-%m-%dT%H:%M:00%:z` (la web muestra "Actualizado a las HH:MM").
Script de ayuda usado el 28/09: `/workspace/feeds2/build.py` (datos en línea → genera `news.json` y añade la entrada a `Briefing/log.md`).

## Publicar
1. Añadir al final de `Briefing/log.md`: `## <updatedAt>` + los 5 títulos publicados por sección (sin borrar entradas anteriores).
2. Un solo commit con el conector GitHub `user-GitHub-xai` → `push_files`:
   `{"owner":"campeonatogranturismo5-ui","repo":"portada-7am","branch":"main","message":"Portada 7AM: AAAA-MM-DD","files":[{"path":"news.json","content":"…"},{"path":"Briefing/log.md","content":"<fichero completo>"}]}`
3. Vercel despliega solo. Opcional: `user-Vercel-xai` → `get_project` (teamId arriba) → `latestDeployment.readyState == READY`.

## Verificar
```bash
for f in "" styles.css app.js; do curl -s -o /dev/null -w "%{http_code} /$f\n" "https://portada-7am.vercel.app/$f"; done
curl -s "https://portada-7am.vercel.app/news.json?t=$(date +%s)" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['updatedAt']);[print(k,len(v['published']),len(v['pool'])) for k,v in d['sections'].items()]"
```
Esperado: 200 ×3, el `updatedAt` nuevo y `5 10` en las 4 secciones.
Capturas (opcional): `google-chrome --headless=new --no-sandbox --hide-scrollbars --user-data-dir=/tmp/chr$RANDOM --virtual-time-budget=6000 --window-size=390,1000 --screenshot=shots/live-mobile.png https://portada-7am.vercel.app/` (y 1440,2200 para escritorio).

## Si algo falla
- Push sin despliegue: `user-Vercel-xai` → `create_deployment` con `deploymentId` del último, o revisar `get_project`.
- Las URLs de despliegue concretas (`portada-7am-xxxx-….vercel.app`) piden login de Vercel (SSO): usar siempre `portada-7am.vercel.app`.

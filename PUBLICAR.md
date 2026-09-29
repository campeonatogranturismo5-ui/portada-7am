# Portada 7AM — Cómo actualizar y republicar (v4: 5 secciones + ficha de noticia + idioma de la fuente)

## Datos fijos
- **URL pública:** https://portada-7am.vercel.app/ (200, sin protección de Vercel)
- **Repo GitHub (público):** https://github.com/campeonatogranturismo5-ui/portada-7am
  - owner `campeonatogranturismo5-ui` · repo `portada-7am` · rama `main`
- **Vercel:** proyecto `portada-7am` (id `prj_vARAnlnxjlEc4XjkH5SEmbCBzvNH`), team `enriquelebrijo-2398s-projects`
  (id `team_g3dcU0xCcjzgBwnhMbeDs1oW`). Enlazado por Git: **cada push a `main` despliega a producción solo** (~30 s).
- **Clon de trabajo en la box: `/workspace/portada-7am-repo`** (git + `gh` autenticado como `campeonatogranturismo5-ui`).
  Capturas en `/workspace/portada-7am/shots/` (fuera del repo, NO se suben). `/workspace/portada-7am` es una copia antigua: no publicar desde ahí.
- Herramientas: `git` + `gh` (vía principal); conector MCP GitHub `user-GitHub-xai` (`push_files`, solo como alternativa)
  y conector Vercel `user-Vercel-xai`. `vercel` CLI no instalado. No iniciar logins nuevos.
- Ficheros del sitio: `index.html` + `app.js` (portada; lee `news.json?t=<timestamp>`), `noticia.html` + `noticia.js` (ficha
  `noticia.html?id=<id>`: busca el id en `published` y luego en `pool`), `styles.css`, `news.json`, `Briefing/log.md`,
  `scripts/build_news.py` (genera y valida `news.json`).
- Secciones, en este orden (menú y portada): **Política · Exterior · Tecnología · Economía · Cultura**
  (`politica`, `exterior`, `tecnologia`, `economia`, `cultura`). Cada una: 1 destacada + 4 en rejilla.
- Las tarjetas de la portada (tarjeta entera y enlace "Leer") abren la ficha propia `noticia.html?id=…` en la misma pestaña;
  **ningún enlace de la portada apunta a un medio externo**. El enlace al original solo está en la ficha (botón "Abrir original",
  pestaña nueva). Si `lang` es `"en"`, la tarjeta y la ficha muestran la etiqueta pequeña "Fuente en inglés" junto al medio.
  **No tocar el diseño de la portada.**
- `.github/workflows/assemble-news.yml` y `.portada-news-parts/` son restos de un apaño anterior para subir `news.json` por trozos:
  **no usarlos** (el workflow solo se dispara si se tocan esos ficheros; con `git push` ya no hacen falta).

## Fuentes por sección (probadas el 29/09/2026)
| Sección | Fuentes | Estado |
|---|---|---|
| Política (España sobre todo) | El País España, elDiario.es, Europa Press | ✅ ✅ ✅ |
| Exterior (mundo) | El País Internacional, BBC Mundo, BBC World, The Guardian World, Politico Europe, AP | ✅ ✅ ✅ ✅ ✅ ✅ (AP: sin RSS, 401; se usa la portada `apnews.com/world-news`) |
| Tecnología (España + internacional) | El País Tecnología, Xataka, TechCrunch, The Verge, Ars Technica, BBC Tech, Guardian Tech | ✅ todas |
| Economía (España + internacional) | El País Economía, Cinco Días, Expansión, BBC Business, Guardian Business, FT | ✅ (FT: solo titular + entradilla, muro de pago → `partial`) |
| Cultura | El País Cultura, BBC Entertainment & Arts, Guardian Culture | ✅ ✅ ✅ |
| — | **Reuters** | ❌ RSS 404 y artículos 401 (anti-bot). Solo se ven titulares vía Google News → no usar salvo como parcial. |

Feeds:
- El País: `https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/<espana|internacional|tecnologia|economia|cultura>/portada`
- Cinco Días: `https://feeds.elpais.com/mrss-s/pages/ep/site/cincodias.elpais.com/portada`
- BBC Mundo: `https://feeds.bbci.co.uk/mundo/rss.xml` · BBC News: `https://feeds.bbci.co.uk/news/<world|business|technology|entertainment_and_arts>/rss.xml`
- The Guardian: `https://www.theguardian.com/<world|business|technology|culture>/rss`
- Politico Europe: `https://www.politico.eu/feed/` (hay piezas en francés: descartar o tratarlas como fuente no española)
- FT: `https://www.ft.com/rss/home` · `https://www.ft.com/world?format=rss`
- AP: enlaces `https://apnews.com/article/…` sacados de `https://apnews.com/world-news` (la página del artículo sí da 200)
- The Verge: `https://www.theverge.com/rss/index.xml` · TechCrunch: `https://techcrunch.com/feed/`
- Ars Technica: `https://feeds.arstechnica.com/arstechnica/index` · Xataka: `https://www.xataka.com/feedburner.xml`
- Expansión: `https://e00-expansion.uecdn.es/rss/portada.xml` (ISO-8859-1)
- Europa Press nacional: `https://www.europapress.es/rss/rss.aspx?ch=00066` · elDiario.es política: `https://www.eldiario.es/rss/politica/`

Consejos de descarga: User-Agent de navegador (Chrome Windows) + `Accept-Language: es-ES`. **De uno en uno con pausas.**
El País/Cinco Días dan 403 si se piden seguidos: 20–30 s de pausa entre artículos suyos (y reintentar los 403 al final) funcionó
con los 20 artículos de El País del 29/09. El texto sale de `articleBody` del JSON-LD (El País, Cinco Días, Europa Press) o de los
`<p>` del cuerpo (BBC, Guardian, Ars, TechCrunch, Xataka, elDiario.es, AP, Politico: quitar menús/promos del principio y final).
La fecha sale de `"datePublished"` (convertir a hora de Madrid, +02:00 / +01:00).

## Reglas editoriales
- **Todo el sitio en castellano**, siempre, sea cual sea el idioma de la fuente: `title`, `summary`, `longSummary` y `bullets`
  escritos con palabras propias. **Nunca traducir el artículo frase a frase ni publicarlo entero.**
- 10 candidatos por sección en `pool` (50 en total), frescos (24-48 h), mezclando medios; sin repetir la misma historia en dos
  secciones. Política = política española sobre todo; Exterior = mundo; Tecnología y Economía = mezcla España + internacional.
- `published` = copia de los 5 más relevantes del `pool` (el primero es la destacada grande). Los otros 5 quedan de reserva.
- Nunca inventar. Solo artículos reales verificados (URL 200 y texto leído). Sin opinión ni datos externos al artículo.
- **Leer el artículo completo** de las 50 noticias y escribir para cada una:
  - `summary`: 1 frase (tarjeta).
  - `longSummary`: **180–280 palabras** con palabras propias, solo con hechos del artículo.
  - `bullets`: **exactamente 4** puntos clave, frases cortas.
  - `partial`: `false` normalmente. Si el artículo es de pago o el texto útil es muy escaso, `partial: true` y un `longSummary`
    más corto (<180 palabras) solo con lo disponible (titular, entradilla, RSS). La ficha muestra la nota de resumen parcial.
    Para reducir parciales: preferir otra noticia equivalente con texto completo (p. ej. sustituir piezas de ~250 palabras).
  - `lang`: idioma de la fuente ORIGINAL (`"es"` o `"en"`). `region`: ámbito de la noticia (`"es"` España, `"int"` internacional).
- Si al releer un artículo se ha actualizado (cambia el titular), actualizar `title`/`summary`.

## Forma exacta de news.json
```json
{
  "updatedAt": "2026-09-29T22:01:00+02:00",
  "timezone": "Europe/Madrid",
  "sections": {
    "politica":   {"published": [5 items], "pool": [10 items]},
    "exterior":   {"published": [...], "pool": [...]},
    "tecnologia": {"published": [...], "pool": [...]},
    "economia":   {"published": [...], "pool": [...]},
    "cultura":    {"published": [...], "pool": [...]}
  }
}
```
Item (todos los campos obligatorios, en `published` y en `pool`):
```json
{"id":"exterior-02","title":"…","summary":"…","longSummary":"180–280 palabras…","bullets":["…","…","…","…"],
 "source":"BBC","url":"https://…","section":"exterior","publishedAt":"2026-09-29T19:14:10+02:00",
 "lang":"en","region":"int","partial":false}
```
- ids URL-safe y estables: `<seccion>-NN` (`politica-01`…`cultura-10`) por orden del `pool`; el item de `published` conserva el id.
- `updatedAt` con `date +%Y-%m-%dT%H:%M:00%:z` (la web muestra "Actualizado a las HH:MM").

### Script: `scripts/build_news.py`
1. Borrador `draft.json` fuera del repo (p. ej. `/workspace/feedsN/draft.json`):
   `{"updatedAt":"…","sections":{"politica":[10 items],"exterior":[…],"tecnologia":[…],"economia":[…],"cultura":[…]}}`,
   cada item con `title, summary, longSummary, bullets, source, url, publishedAt, lang, region, partial` y `"published": true`
   en los 5 de portada. Si falta `lang`, se deduce del medio (`LANG_BY_SOURCE`).
2. `cd /workspace/portada-7am-repo && python3 scripts/build_news.py /workspace/feedsN/draft.json --log`
   → asigna ids, escribe `news.json` (un item por línea), añade la entrada a `Briefing/log.md` y **valida**: 5 secciones con
   10/5 items, todos los campos, 4 bullets, `lang` es/en, `region` es/int, `partial` booleano, 180–280 palabras si no es parcial
   (<180 si lo es), fechas ISO. Si hay errores no escribe nada. Al final imprime
   `items: 50 · fuente en inglés: N · parciales: N · palabras (no parciales): min–max`.
3. `python3 scripts/build_news.py --check [fichero]` valida un `news.json` sin tocarlo.

## Publicar (vía principal: git + gh desde `/workspace/portada-7am-repo`)
```bash
cd /workspace/portada-7am-repo
git pull --ff-only origin main              # sincronizar antes de generar
python3 scripts/build_news.py /workspace/feedsN/draft.json --log
git add news.json Briefing/log.md           # (+ otros ficheros si cambian)
git commit -m "Portada 7AM: AAAA-MM-DD"     # un solo commit
git push origin main                        # sin límite de tamaño; Vercel despliega solo
```
`gh auth status` debe mostrar `campeonatogranturismo5-ui`. Si `gh`/git no están disponibles, **alternativa**: conector
`user-GitHub-xai` → `push_files` a `main` con los ficheros completos (news.json pesa ~180 KB: si la llamada es demasiado grande,
parar y avisar; no trocear en base64 ni usar workflows).
Opcional: `user-Vercel-xai` → `get_project` (teamId arriba) → `latestDeployment.readyState == READY`.

## Verificar
```bash
B=https://portada-7am.vercel.app
for f in "" noticia.html styles.css app.js noticia.js; do curl -s -o /dev/null -w "%{http_code} /$f\n" "$B/$f"; done
curl -s "$B/news.json?t=$(date +%s)" -o /tmp/live.json && python3 /workspace/portada-7am-repo/scripts/build_news.py --check /tmp/live.json
curl -s "$B/app.js" | grep -n "href" # la portada solo enlaza a noticia.html?id=… (nada de item.url)
```
Esperado: 200 ×5 y `items: 50 · … · parciales: N · palabras (no parciales): min–max` sin errores.
Capturas (`--user-data-dir` nuevo para no usar caché):
`google-chrome --headless=new --no-sandbox --hide-scrollbars --user-data-dir=/tmp/chr$RANDOM --virtual-time-budget=8000 --window-size=390,1000 --screenshot=/workspace/portada-7am/shots/live-mobile.png $B/`
(1440,2200 para escritorio; ficha de una fuente inglesa: `$B/noticia.html?id=exterior-02`).

## Si algo falla
- Push sin despliegue: `user-Vercel-xai` → `create_deployment` con `deploymentId` del último, o revisar `get_project`.
- Las URLs de despliegue concretas (`portada-7am-xxxx-….vercel.app`) piden login de Vercel (SSO): usar siempre `portada-7am.vercel.app`.

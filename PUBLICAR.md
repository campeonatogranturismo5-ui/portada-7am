# Portada 7AM — Cómo actualizar y republicar

## Datos fijos
- **URL pública:** https://portada-7am.vercel.app/ (verificada 200, sin protección de Vercel)
- **Repo GitHub (público):** https://github.com/campeonatogranturismo5-ui/portada-7am
  - owner: `campeonatogranturismo5-ui` · repo: `portada-7am` · rama: `main`
- **Vercel:** proyecto `portada-7am` (id `prj_vARAnlnxjlEc4XjkH5SEmbCBzvNH`),
  team `enriquelebrijo-2398s-projects` (id `team_g3dcU0xCcjzgBwnhMbeDs1oW`).
  Enlazado al repo por Git: **cada push a `main` despliega a producción automáticamente**. No hace falta redeploy manual.
- Copia local de trabajo: `/workspace/portada-7am` (en la box).
- CLIs: `gh` está instalado pero **no autenticado**; `vercel` CLI no está instalado. Se usan los conectores MCP.
- GitHub Pages **no** está activado (no hay gh autenticado ni herramienta MCP para Pages). Se sirve por Vercel.

## Rutina diaria (7:00 Europe/Madrid)
1. Recoger noticias de las fuentes (RSS/páginas que funcionaron el 28/09/2026):
   - BBC: https://feeds.bbci.co.uk/news/rss.xml y https://feeds.bbci.co.uk/news/world/rss.xml
   - El País: https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada (algún artículo da 403 con curl básico; reintentar con User-Agent de navegador Windows + `Accept-Language: es-ES`)
   - Cadena SER: https://cadenaser.com/arc/outboundfeeds/rss/?outputType=xml (mucho contenido local; filtrar `/nacional/`)
   - RTVE: portada https://www.rtve.es/noticias/ (extraer enlaces `/noticias/AAAAMMDD/...`). El RSS `api2.rtve.es/rss/temas_noticias.xml` está congelado en 2022; no usarlo.
   - AP: portada https://apnews.com/ (enlaces `/article/...`; fecha en `"datePublished"` en UTC → convertir a +02:00/+01:00)
   - Reuters: **bloqueado** (401) desde la box.
   Elegir 10 historias, máx. ~3 por medio, sin duplicados. Resumen de 1 frase en español basado solo en el texto de la fuente (og:description / primeros párrafos). Nunca inventar.
2. Escribir `news.json`:
   `{"updated": "<ISO8601 con +02:00 o +01:00>", "items": [{"titular","medio","resumen","enlace","fecha"} x10]}`
   (`date +%Y-%m-%dT%H:%M:%S%:z` en la box da la hora de Madrid con offset.)
3. Añadir al final de `Briefing/log.md`: `## <fecha ISO>` + lista numerada de los 10 titulares — medio.
4. Publicar con **un commit** vía conector GitHub (MCP `user-GitHub-xai`, herramienta `push_files`):
   ```json
   {"owner":"campeonatogranturismo5-ui","repo":"portada-7am","branch":"main",
    "message":"Portada 7AM: noticias AAAA-MM-DD",
    "files":[{"path":"news.json","content":"..."},{"path":"Briefing/log.md","content":"<log completo>"}]}
   ```
   (Para `log.md` hay que enviar el archivo completo, no solo la entrada nueva.)
5. Vercel despliega solo (~10-30 s). Comprobar (opcional) con MCP `user-Vercel-xai` → `list_deployments` / `get_project` (teamId arriba).
6. Verificar:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" https://portada-7am.vercel.app/
   curl -s "https://portada-7am.vercel.app/news.json?t=$(date +%s)" | head -3   # debe mostrar el nuevo "updated"
   ```

## Si algo falla
- Si el push no dispara despliegue: MCP `user-Vercel-xai` → `create_deployment` redeploy del último (`deploymentId`), o revisar `get_project` → `latestDeployment`.
- La protección SSO de Vercel está en modo "all_except_custom_domains" pero el dominio de producción `portada-7am.vercel.app` responde 200 público. Las URLs de preview/despliegue concretas (`portada-7am-xxxx-...vercel.app`) sí pueden pedir login: usar siempre la URL de producción.

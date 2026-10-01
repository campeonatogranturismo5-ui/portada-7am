# Estado verificable de Portada 7AM

Actualizado: 01/10/2026. Trabajo en la rama `codex/automatic-edition`.

## Completado

- Recuperación del ZIP y del repositorio actual, sin sobrescribir su rama principal.
- Copia Git recuperable desde `5dd8c1df5fdeb363e12e004acb6586f72055031b`.
- Sitio generado en HTML: siete secciones, archivo, buscador, guardadas, claro/oscuro, WhatsApp y copia de enlaces.
- 50 fichas del archivo original con identificadores congelados y compatibilidad con los enlaces antiguos.
- Recopilación real de RSS: la selección piloto incluye Durango y una fuente primaria de ciencia en inglés (NASA).
- Cuota observada en AI Studio del proyecto Asistente: nivel gratuito, Gemini 3.1 Flash Lite, 15 RPM / 250.000 TPM / 500 RPD. Modelo documentado como gratuito el 30/09/2026.
- Pruebas locales de caché, fechas, cambio horario, deduplicación y conservación de edición ante fallo simulado de Gemini.
- Verificación de HTML, metadatos, enlaces internos y ausencia de patrones de claves en la salida pública.
- Navegación local probada en escritorio, móvil y tableta: tema, ficha, guardadas, búsqueda y copiar enlace.
- GitHub Actions de validación ejecutado con éxito y despliegue Preview de Vercel completado y abierto en navegador.
- Vercel Hobby y repositorio público confirmados. No se ha activado facturación.

## Pendiente — no afirmar que ya está funcionando

- GEMINI_API_KEY está guardado desde el 30/09 y funciona. Las llamadas reales ya han validado una noticia de Euskadi; el piloto completo sigue pendiente.
- Ejecutar el piloto de cinco noticias, revisar fidelidad humana y enlaces de fuentes, y repetirlo para verificar la caché real.
- Publicar la nueva versión en producción y comprobar el resultado público.
- Activar AUTO_EDITION_ENABLED tras la prueba real; el workflow preparado aún no constituye una automatización activa.
- Hostalia autenticado y CNAME noticias.lebrijo.es añadido hacia 422a85f40776f04b.vercel-dns-017.com. Dominio añadido a producción en Vercel. Pendiente propagación DNS y verificar HTTPS; todavía no se ha sustituido la web anterior.
- Comprobar posteriormente la primera ejecución programada. Una prueba manual no la sustituye.

## Recuperación

Ver README.md. La edición actual solo cambia cuando el resultado pasa los controles. La caché y el consumo se conservan por separado después de un fallo. La rama principal mantiene la versión anterior mientras no se complete el piloto.

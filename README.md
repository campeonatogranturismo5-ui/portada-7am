# Portada 7AM

Web estática con siete secciones, fichas HTML permanentes, archivo, buscador, temas claro/oscuro y lectura guardada en el navegador.

## Operación

- python scripts/pipeline.py --collect-only --limit 5: comprueba RSS sin utilizar Gemini.
- python scripts/pipeline.py --limit 5: piloto real, requiere GEMINI_API_KEY en el entorno.
- python scripts/pipeline.py --limit 35: hasta cinco noticias por sección. No rellena secciones.
- python scripts/build.py: genera exclusivamente contenido público en dist/.
- python -m unittest discover -s tests -v y python scripts/check_site.py: controles.

Python 3.12 en Linux; en Windows se requiere la base de zonas tzdata si Python no dispone de ella. Sin paquetes de ejecución en GitHub Actions.

## Datos y seguridad

La clave va únicamente en el secreto de GitHub Actions GEMINI_API_KEY. Nunca en archivos, variables públicas o Vercel cliente. data/config.json selecciona un único modelo gratuito verificado, sin fallback de pago. Se conservan caché de resúmenes y contador diario, incluso después de fallos. Máximo local: 90 llamadas al día y una llamada cada 7 segundos, por debajo de las cuotas observadas.

El material RSS se considera datos, nunca instrucciones. Se valida la fecha, se comprueba el enlace público, se seleccionan medios y se deduplica antes de resumir. Una segunda llamada revisa fidelidad, castellano y duplicados semánticos. Los controles automáticos no garantizan ausencia de errores. Las fichas basadas en extractos se marcan como parciales. No se descargan cuerpos ocultos ni se sortean bloqueos.

El contador usa el día de America/Los_Angeles; los datos se archivan con Europe/Madrid. Los identificadores nuevos derivan de la URL canónica. Los identificadores reutilizados del proyecto antiguo quedan congelados mediante aliases hacia el archivo de la versión recuperada. No se puede reconstruir cuál de sus noticias anteriores pretendía abrir un enlace reutilizado antes de esta migración.

## Programación y despliegue

El workflow edition.yml programa las 07:07 Europe/Madrid y un segundo intento a las 08:37, con exclusión mutua y límite de 20 minutos. La programación queda desactivada hasta establecer AUTO_EDITION_ENABLED=true tras verificar el piloto. El segundo intento no publica otra edición si ya hay una del día. Las ejecuciones manuales pueden actualizarla. El HTML se construye y verifica antes de hacer commit.

Vercel debe estar conectado a main, en Hobby, usando vercel.json y el directorio dist. Solo se publica mediante commit validado. Verificar el estado READY del despliegue y la fecha pública: un commit no demuestra que se haya desplegado.

GitHub puede retrasar o descartar ejecuciones y desactivar schedules de repositorios públicos tras 60 días sin actividad. Si ocurre: revisar Actions, resolver el fallo, reactivar el workflow y ejecutarlo manualmente. El aviso de edición desactualizada aparece tras 36 horas. Los fallos de un workflow pueden notificarse según las preferencias de GitHub del propietario. No se asegura disponibilidad ilimitada.

## Recuperación

Ante fallo de Gemini, no se modifica data/current.json. Repetir manualmente reutiliza la caché. Para deshacer una publicación: revertir el commit de edición o restaurar data/current.json y reconstruir, conservando data/archive.json para no romper enlaces. En Vercel se puede promover el despliegue válido anterior. La copia inicial está en el commit 5dd8c1df5fdeb363e12e004acb6586f72055031b.

## Gratuidad comprobada el 30/09/2026

- Proyecto Asistente: AI Studio muestra Nivel gratuito; Gemini 3.1 Flash Lite: 15 RPM, 250.000 TPM, 500 RPD.
- Modelo y precios: https://ai.google.dev/gemini-api/docs/pricing#gemini-3.1-flash-lite
- GitHub Actions: runners estándar gratuitos en repositorios públicos. https://docs.github.com/en/actions/concepts/billing-and-usage
- Vercel Hobby: proyectos personales no comerciales; al agotar límites puede pausar. https://vercel.com/docs/plans/hobby
- Horarios y posibles desactivaciones: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule

No activar facturación, créditos, planes o trials para resolver un límite. Los proveedores pueden cambiar las condiciones; si el modelo deja de estar disponible se detiene la edición.

## Estado de entrega

Consultar ENTREGA.md: distingue pruebas locales, piloto real, instalación de automatización, publicación y DNS.

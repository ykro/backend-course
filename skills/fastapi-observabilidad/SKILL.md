---
name: fastapi-observabilidad
description: Usar cuando un API Python o FastAPI ya está en producción (Cloud Run u otro) y "no sé qué pasó cuando falla", faltan logs, no hay forma de seguir una petición, no hay alertas, o hay que agregar logging estructurado, request id, trazas o métricas de latencia y errores.
---

# Observabilidad de un API FastAPI

Saber qué pasó requiere tres cosas. Logs estructurados donde cada línea dice qué petición la produjo, métricas de latencia y errores, y una alerta que avisa antes que el cliente. En Cloud Run, todo lo que la app escribe en stdout como JSON con `severity` y `message` llega a Cloud Logging ya indexado.

1. Configura logging una sola vez al arrancar. JSON a stdout con `severity`, `message`, `logger` y los campos extra. Nada de `print`.
2. Agrega un middleware que por cada petición genere o propague un id (`X-Request-ID`), lo guarde en un `contextvars` para que todas las líneas lo lleven, lo devuelva en la respuesta y escriba una línea final con método, ruta (la plantilla, no el path con ids), código y duración en milisegundos.
3. Correlaciona con las trazas de Cloud Run. Lee `traceparent` o `X-Cloud-Trace-Context` y escribe `logging.googleapis.com/trace` como `projects/PROJECT_ID/traces/TRACE_ID`. Cloud Run no define `GOOGLE_CLOUD_PROJECT` por sí solo; pásalo con `--set-env-vars` o léelo del servidor de metadatos. Si falta, avisa en el arranque en vez de apagar la correlación en silencio.
4. Registra las excepciones no manejadas con su traceback en un handler de `Exception` que responde 500 genérico al cliente. Así Error Reporting las agrupa. Ese handler corre fuera de los middlewares, así que agrega ahí el `X-Request-ID` y la línea final leyendo el id del `contextvar`. Desactiva `uvicorn.access` (o déjalo en WARNING) para no duplicar líneas.
5. No registres secretos, tokens, contraseñas ni datos personales completos. Correos y teléfonos enmascarados, cuerpos de petición fuera por defecto.
6. Métricas. Lo mínimo es latencia por ruta y tasa de 5xx. En Cloud Run ya existen las de petición; para las propias, crea métricas basadas en logs sobre la línea final del paso 2 o usa OpenTelemetry con el exportador de Google Cloud.
7. Alertas en Cloud Monitoring. Tasa de 5xx mayor al 2 % en 5 minutos y latencia p95 sobre tu umbral, más un uptime check a `/health`. Pruébalas una vez provocando el error en un entorno de prueba.
8. Escribe tests del middleware. La respuesta trae `X-Request-ID`, un id recibido se respeta, y la línea de log es JSON válido con `severity` y duración (`caplog` o capturando stdout).
9. No cambies el comportamiento de las rutas al agregar observabilidad; si ves un bug, anótalo aparte.
10. Reporta qué se registra, cómo buscarlo (un filtro de ejemplo en Logs Explorer como `jsonPayload.request_id="..."`), las alertas creadas y lo que quedó pendiente.

```python
import json, logging, sys
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar("request_id")

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {"severity": record.levelname, "message": record.getMessage(), "logger": record.name}
        entry.update(getattr(record, "fields", {}))
        if rid := request_id.get(None):  # ContextVar que llena el middleware
            entry["request_id"] = rid
        if record.exc_info:
            entry["stack_trace"] = self.formatException(record.exc_info)
        return json.dumps(entry, ensure_ascii=False, default=str)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)
```

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

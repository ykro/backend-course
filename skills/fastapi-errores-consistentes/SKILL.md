---
name: fastapi-errores-consistentes
description: Usar cuando los errores de un API FastAPI vienen en formatos distintos (detail como texto, como objeto, listas de validación), el frontend o la app no sabe qué mostrar, aparecen 500 con trazas, o hay que definir códigos de error estables y documentarlos en OpenAPI.
---

# Errores consistentes en un API FastAPI

Todos los errores salen con la misma forma, un código estable que el cliente puede usar en un `switch` y un mensaje para personas. Los errores de dominio se lanzan como excepciones propias y se traducen en un solo lugar. Cambiar la forma de los errores rompe a los clientes que ya existen, así que se coordina antes de desplegar.

1. Inventaría los errores actuales. Busca `HTTPException`, `raise`, `return JSONResponse` y los 422 de validación, y anota código HTTP y forma de cada uno.
2. Pregunta quién consume el API hoy, aunque el pedido diga "hazlo"; mientras esperas, prepara el cambio en una rama. Si hay clientes que leen `detail`, el formato nuevo es un cambio que rompe; propón mantener `detail` en paralelo por un tiempo o publicarlo en una versión nueva (skill `fastapi-versionado-api`). Decide con el equipo antes de implementar.
3. Elige una forma y escríbela. Puede ser `application/problem+json` (RFC 9457, con `type`, `title`, `status`, `detail`) más un campo `code`, o un sobre propio `{"error": {"code", "message", "details"}}`. Una sola.
4. Define las excepciones de dominio con su código HTTP y su `code` (`TASK_NOT_FOUND`, `NOT_OWNER`). El dominio lanza esas excepciones y no importa FastAPI.
5. Registra handlers para tus excepciones de dominio, para `HTTPException` de Starlette (404 de ruta, 405), para `RequestValidationError` (422 con la lista de campos en `details`) y para `Exception` (500 genérico sin traza al cliente y con traza en el log).
6. No cambies de paso qué código HTTP devuelve una situación (un 404 que pasa a 401). Convertir un 500 accidental en el 404 o 409 que corresponde sí es parte del trabajo, y se lista. Si encuentras uno mal, anótalo y propónlo aparte.
7. Documenta la forma en OpenAPI con un modelo de error y `responses={404: {"model": ErrorOut}, ...}` en las rutas, para que los clientes generados la conozcan.
8. Escribe tests de la forma. Un 404 de dominio, un 404 de ruta inexistente, un 422 y un 500 forzado, todos con la misma estructura y el `code` esperado. Para el 500 usa `TestClient(app, raise_server_exceptions=False)`; el cliente por defecto vuelve a lanzar la excepción y nunca ves la respuesta. Un 401 debe seguir trayendo `WWW-Authenticate`.
9. Reporta la forma elegida, la tabla de códigos y el plan de transición para los clientes actuales.

```python
# from starlette.exceptions import HTTPException as StarletteHTTPException
# logger = logging.getLogger(__name__)

class DomainError(Exception):
    status_code = 400
    code = "BAD_REQUEST"
    def __init__(self, message: str, **details: object) -> None:
        self.message, self.details = message, details

class TaskNotFound(DomainError):
    status_code, code = 404, "TASK_NOT_FOUND"

def error_body(code: str, message: str, details: object = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or {}}}

@app.exception_handler(DomainError)
async def domain_error(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(error_body(exc.code, exc.message, exc.details), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    fields = [{"field": ".".join(map(str, e["loc"][1:])), "message": e["msg"]} for e in exc.errors()]
    return JSONResponse(error_body("VALIDATION_ERROR", "Datos inválidos", {"fields": fields}), status_code=422)

@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(error_body(f"HTTP_{exc.status_code}", str(exc.detail)),
                        status_code=exc.status_code, headers=exc.headers)  # conserva WWW-Authenticate

@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("error no manejado")
    return JSONResponse(error_body("INTERNAL_ERROR", "Ocurrió un error inesperado"), status_code=500)
```

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

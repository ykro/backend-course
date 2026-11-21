---
name: fastapi-rendimiento-async
description: Usar cuando un API FastAPI se congela o se pone lento con varias peticiones a la vez, hasta /health deja de responder, hay time.sleep, requests o una base de datos síncrona dentro de async def, o hay que decidir entre def y async def, timeouts y caché.
---

# Rendimiento async en FastAPI

FastAPI corre las rutas `async def` en el hilo del event loop y las `def` en un pool de hilos. Una llamada que bloquea (`time.sleep`, `requests`, un driver síncrono, cálculo pesado) dentro de `async def` detiene todo el servidor, incluido `/health`. Primero se mide, después se cambia una cosa y se vuelve a medir.

1. Reproduce y mide antes de tocar. Lanza N peticiones concurrentes a la ruta lenta y, a la vez, a `/health`, y anota tiempos. Un script corto con `httpx.AsyncClient` y `asyncio.gather` alcanza, o `hey -n 40 -c 20 URL`.
2. Busca bloqueos dentro de `async def`. `time.sleep`, `requests.`, `urllib`, sesiones de SQLAlchemy síncronas, lectura de archivos grandes, bucles de cálculo.
3. Elige el arreglo más pequeño que resuelve. Si todo lo que llama la ruta es síncrono, empieza por `def`; pasa a async solo si ya usas librerías async o necesitas muchas llamadas salientes simultáneas.

   | Situación | Arreglo |
   |---|---|
   | La ruta solo llama código síncrono | cambiar `async def` por `def`; corre en el pool de hilos |
   | Necesitas async y una librería síncrona puntual | `await run_in_threadpool(func, ...)` de `fastapi.concurrency` |
   | Llamadas HTTP salientes | `httpx.AsyncClient` compartido (creado en el lifespan) con `timeout` explícito |
   | Base de datos | driver async (`asyncpg`, `create_async_engine`) en todo el camino, o rutas `def` con sesión síncrona |
   | Trabajo largo (PDF, correo) | devolver 202 y hacerlo en una cola (Cloud Tasks) o `BackgroundTasks` si es corto y perderlo no importa |
   | Cálculo de CPU | proceso aparte o servicio de trabajos; los hilos no ayudan |

4. Toda llamada externa lleva timeout y manejo de error. Sin timeout, un servicio lento cuelga tus workers.
5. Si agregas caché (por ejemplo del tipo de cambio), define cuánto tiempo vale, qué pasa cuando expira y el externo falla, y si la respuesta debe decir la fecha del dato. Para dinero, un dato viejo sin aviso es un error, no una optimización. Evita que muchas peticiones refresquen la caché a la vez con un candado (`asyncio.Lock`).
6. Revisa también lo que no es async. Consultas N+1, falta de índices, respuestas enormes sin paginación y el número de workers de uvicorn o instancias.
7. Mide otra vez con la misma prueba y reporta antes y después (tiempo de la ruta y de `/health`).
8. Deja una prueba de regresión. Con el externo simulado lento (`MockTransport` que espera), N peticiones concurrentes terminan en menos de un umbral y `/health` responde mientras tanto.

Si el proyecto usa `httpx2` (lo trae Starlette reciente), la interfaz es la misma con `import httpx2 as httpx`. Al probar, `httpx.ASGITransport` no corre el lifespan; usa `with TestClient(app)` o inicializa el cliente en el fixture. Con muchas peticiones, el límite de conexiones del cliente de medición (100 en httpx) puede ser el cuello de botella; súbelo.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=httpx.Timeout(5.0))
    yield
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/tasks/{task_id}/report")
async def report(task_id: int, request: Request):
    r = await request.app.state.http.get(RATES_URL)
    r.raise_for_status()
    ...
```

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

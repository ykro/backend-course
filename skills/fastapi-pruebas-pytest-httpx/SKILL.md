---
name: fastapi-pruebas-pytest-httpx
description: Usar cuando hay que escribir o arreglar pruebas de un API FastAPI con pytest - base de datos de prueba, dependency_overrides, autenticación en tests, llamadas a APIs externos sin red, endpoints async, tests lentos o que dependen del orden, o "escríbeme pruebas para esta API".
---

# Pruebas de FastAPI con pytest y httpx

Cada test arma sus datos, no toca la red ni la base real y describe el comportamiento correcto. Las dependencias (sesión, usuario, cliente HTTP, reloj) se reemplazan con `app.dependency_overrides`, no editando la app. Si el código no se puede reemplazar así, eso es un hallazgo que se propone, no algo que se cambia sin permiso.

1. Lee cómo se crean la app, la sesión de base de datos y los clientes externos. Anota qué es una dependencia (`Depends`) y qué es global (sesión creada al importar, `requests.get` dentro de la ruta). Lo global no se puede aislar bien; propón convertirlo en dependencia y espera el sí antes de tocar `app/`. Mientras tanto escribe las pruebas que sí se pueden aislar hoy (las rutas que no usan lo global) y deja listas las demás.
2. En `tests/conftest.py` crea la base de prueba y el cliente. SQLite en memoria con `StaticPool` sirve para lógica; si el código usa funciones propias de Postgres, usa un Postgres de prueba. Cada test empieza con tablas vacías.
3. Reemplaza las dependencias con `app.dependency_overrides[get_session] = ...` y límpialas al final (`app.dependency_overrides.clear()`).
4. Para APIs externos, si el código usa httpx, inyecta un `httpx.Client` y en los tests pásale `httpx.MockTransport` o usa `respx`. Si usa `requests`, propón cambiar a httpx o usa `responses` (agrégala como dependencia de desarrollo). Prueba la respuesta buena, un error 500 del externo y un timeout.
5. Para autenticación, crea un fixture que registra un usuario y devuelve sus headers, o reemplaza `get_current_user`. Prueba siempre con dos usuarios para cubrir que uno no ve lo del otro.
6. Para endpoints o código async, usa `httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")` con `@pytest.mark.anyio` (el plugin de pytest que trae anyio) o `pytest-asyncio`. Para lo sync basta `TestClient`. Las versiones recientes de Starlette usan el paquete `httpx2` (misma interfaz) y avisan que `httpx` está deprecado; si el proyecto solo tiene `httpx2`, escribe `import httpx2 as httpx` en los ejemplos.
7. Escribe lo que debe pasar, no lo que pasa hoy. Si hoy responde 500 donde el contrato dice 404, el test espera 404 y se marca `@pytest.mark.xfail(strict=True, reason="...")` hasta arreglarlo. Un `pytest.raises` que acepta el 500 consagra el bug.
8. Prioriza lo que más daño hace si se rompe. Pertenencia entre usuarios, validación de entrada, errores del externo y el caso feliz de cada ruta. Para decidir qué casos atrapan errores reales y comprobarlo con mutantes, usa la skill `fastapi-tests-que-atrapan-errores`.
9. Corre `uv run pytest -q` dos veces y en orden aleatorio si tienes `pytest-randomly`. Muestra la salida y los xfail con su motivo.

```python
import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app, get_session, get_rates_client
from app.db import Base

@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    def fake_rates(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"rates": {"GTQ": "7.75"}})

    def session_override():
        with Session() as s:
            yield s

    app.dependency_overrides[get_session] = session_override
    app.dependency_overrides[get_rates_client] = lambda: httpx.Client(transport=httpx.MockTransport(fake_rates))
    yield TestClient(app)
    app.dependency_overrides.clear()
```

El ejemplo supone que `get_session` y `get_rates_client` ya son dependencias; si no existen, ese es el primer cambio que se propone.

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

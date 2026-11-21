---
name: fastapi-endpoint-con-contrato
description: Usar cuando hay que agregar o cambiar un endpoint o ruta en un proyecto FastAPI ("agrega una ruta que...", "necesito un endpoint para...", PATCH, acciones como cancelar, vender, aprobar), antes de escribir el código.
---

# Endpoint de FastAPI con contrato y pruebas

Primero el contrato, después un test que falla y después el código mínimo, capa por capa. El contrato es una decisión del producto; si el pedido no lo fija, se propone y se confirma antes de programar. El proyecto ya tiene capas, formato de errores y reglas (en `AGENTS.md` o en el código); se copian aunque otra forma también funcione.

1. Lee `AGENTS.md` si existe y una ruta parecida del proyecto. Anota cómo valida paths y cuerpos, qué `response_model` usa, dónde vive la lógica, cómo lanza errores y cómo se prueba.
2. Busca si ya existe otra forma de llegar al mismo estado. Si ya hay `PATCH /status` que acepta `sold`, un endpoint nuevo de venta crea dos caminos y datos inconsistentes; el contrato decide cuál queda y qué pasa con el otro.
3. Escribe el contrato en pocas líneas. Método y ruta, cuerpo de entrada, respuesta exitosa con su código, y la tabla de errores con código HTTP, código de error y orden de evaluación. El orden habitual es 401, 422 de validación, 404 del recurso, 403 de propiedad y después las reglas de dominio (409, 400). Si eliges algo que el pedido no dice (idempotencia, fechas futuras, zona horaria), márcalo `[CONFIRMAR]` y pregunta antes de seguir. Mientras esperas, deja escritos el contrato propuesto y los tests, sin tocar la app. Si cerrar el camino viejo obliga a cambiar tests existentes, eso también se confirma; los tests existentes no se editan sin aprobación.
4. Escribe los tests del contrato con los fixtures del proyecto. Un caso feliz y uno por fila de la tabla de errores. Corre `pytest` y confirma que fallan por la razón correcta (404 o 405 porque la ruta no existe), no por un error de importación.
5. Modelos en su archivo. La entrada es una clase distinta de la salida, con `extra="forbid"` y límites (`max_length`, `gt`, `le`) para que una entrada extrema sea 422 y nunca 500. Dinero en `Decimal` o en centavos enteros, nunca `float`.
6. Lógica en el dominio o repositorio, que lanza excepciones de dominio y no importa FastAPI. Valida todo antes de mutar. Toda ruta que use un recurso por id comprueba que pertenece a quien llama, y el dueño sale del token, nunca del cuerpo.
7. La ruta solo recibe, llama con `Depends(...)` y devuelve el modelo de salida.
8. Si el cambio agrega o cambia columnas, hace falta una migración; usa la skill `fastapi-migraciones-alembic`. Borrar la base no es un plan.
9. Corre la suite completa y el linter (`uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`). Si un test que ya pasaba falla, se arregla el código, no el test.
10. Reporta el contrato final, los archivos por capa, los tests (qué verifica cada uno), la salida de los comandos y lo que quedó `[CONFIRMAR]`. No cambies comportamiento de otras rutas sin decirlo y sin que se apruebe.

```python
def test_mark_sold_by_other_agent_is_403(client, login_as, create_property) -> None:
    prop = create_property(owner="ana@x.gt")
    r = client.post(f"/api/v1/properties/{prop['id']}/sale",
                    json={"sold_on": "2026-11-02"}, headers=login_as("beto@x.gt"))
    assert r.status_code == 403
    assert client.get(f"/api/v1/properties/{prop['id']}").json()["status"] != "sold"
```

## Errores comunes

| Error | Corrección |
|---|---|
| `KeyError` o `None.__dict__` que terminan en 500 al pedir un id inexistente | buscar y lanzar el 404 de dominio |
| Un hijo encontrado aunque pertenece a otro padre | filtrar por padre y por id |
| El mismo modelo para entrada y salida | clases distintas; la salida nunca expone hash, correo ajeno ni campos internos |
| `HTTPException` dentro del repositorio | excepción de dominio y handler en la app |
| Cambiar "de paso" otra ruta | proponerlo aparte |

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

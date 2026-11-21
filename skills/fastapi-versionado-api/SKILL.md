---
name: fastapi-versionado-api
description: Usar cuando hay que cambiar la forma de una respuesta o de un campo en un API que ya tiene clientes (app móvil, integraciones) - renombrar o cambiar el tipo de un campo, quitar una ruta, crear /api/v2, deprecar algo, o clientes viejos que no se actualizan.
---

# Versionar un API sin romper a los clientes

Un cambio que rompe a un cliente que no se puede actualizar a la fuerza (una app móvil vieja) se hace en pasos. Primero se agrega lo nuevo junto a lo viejo, luego se mide quién sigue usando lo viejo y al final se quita. Cuándo quitarlo lo deciden los datos de uso, no el calendario del equipo.

1. Clasifica el cambio. Agregar un campo opcional o una ruta nueva no rompe. Renombrar, quitar, cambiar el tipo o el significado de un campo, volver obligatorio algo de la entrada o cambiar códigos de error sí rompe.
2. Si no rompe, hazlo en la versión actual y documéntalo en el changelog.
3. Si rompe, elige la forma y confírmala con quien mantiene los clientes.

   | Forma | Cuándo |
   |---|---|
   | Campo nuevo en paralelo (`price_detail: {amount, currency}` junto a `price`) | un cambio puntual; los clientes nuevos leen el campo nuevo |
   | Versión en la ruta (`/api/v2/tasks`) con un `APIRouter` por versión | varios cambios juntos o un contrato distinto |
   | Versión por header | solo si ya es la convención del API |

4. Comparte la lógica entre versiones. El servicio devuelve un objeto de dominio y cada versión tiene su modelo de salida; no copies servicios.
5. Si el campo nuevo necesita un dato que no existe (la moneda), pregunta de dónde sale antes de diseñarlo. Si el campo viejo se calcula del nuevo, hazlo sin perder precisión. Dinero en `Decimal` o centavos, nunca `round(float * 100)`.
6. Marca lo viejo como deprecado. En OpenAPI con `deprecated=True` en la ruta o el campo, y en la respuesta con los headers `Deprecation` (RFC 9745, la fecha desde la que está deprecado como `@` más segundos Unix), `Sunset` (fecha HTTP en que se quitará) y un `Link` a la documentación.
7. Mide antes de quitar. Registra por petición la versión usada y el cliente (`User-Agent` o un header `X-App-Version`). Define con el equipo la regla para apagar (por ejemplo, menos del 1 % de las peticiones durante 30 días) y, si la app lo permite, un mínimo de versión que muestre "actualiza la app".
8. Escribe tests de contrato por versión. Un test por versión que valida la forma exacta de la respuesta, para que un cambio en v2 no rompa v1 sin que nadie lo note.
9. Entrega el plan en pasos con fechas o condiciones (agregar, publicar app nueva, medir, deprecar, quitar), qué cambia en cada uno y el test que lo protege.

```python
v1 = APIRouter(prefix="/api/v1")
v2 = APIRouter(prefix="/api/v2")

@v1.get("/tasks/{task_id}", response_model=TaskOutV1, deprecated=True)
def get_task_v1(task_id: int, response: Response, svc: TaskServiceDep) -> TaskOutV1:
    response.headers["Deprecation"] = "@1798761600"  # 2027-01-01 en segundos Unix
    response.headers["Sunset"] = SUNSET_V1  # "Wed, 30 Jun 2027 00:00:00 GMT", acordada después de medir el uso
    return TaskOutV1.from_domain(svc.get(task_id))

@v2.get("/tasks/{task_id}", response_model=TaskOutV2)
def get_task_v2(task_id: int, svc: TaskServiceDep) -> TaskOutV2:
    return TaskOutV2.from_domain(svc.get(task_id))
```

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

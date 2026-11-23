# Código del codelab, Unidad 2

Cada bloque de código del codelab, en el orden en que aparece, con la sangría exacta. El código del taller lo escribe tu agente con el pedido de cada paso del codelab: estos **fragmentos** son la referencia para revisar su diff (el cuerpo de una función, un método), no para pegarlos. No son archivos completos del proyecto, salvo que el paso diga lo contrario. Los `comandos.sh` se corren línea por línea en la terminal, en la raíz de tu repositorio.

| Paso | Archivo | Dónde va |
| :--- | :--- | :--- |
| 1. Entorno y estado inicial | `paso-01-entorno-y-estado-inicial/01-comandos.sh` | terminal, en la raíz de tu repositorio |
| 1. Entorno y estado inicial | `paso-01-entorno-y-estado-inicial/02-comandos.sh` | terminal, en la raíz de tu repositorio |
| 2. Tablas y DTO | `paso-02-tablas-y-dto/01-models.py` | `app/models.py` |
| 2. Tablas y DTO | `paso-02-tablas-y-dto/02-schemas.py` | `app/schemas.py` |
| 3. Sesiones, capas y tests herméticos | `paso-03-sesiones-capas-y-tests-hermeticos/01-fragmento.py` | ver el texto del paso en el codelab |
| 3. Sesiones, capas y tests herméticos | `paso-03-sesiones-capas-y-tests-hermeticos/02-conftest.py` | `tests/conftest.py` |
| 4. Taller 1: filtros, JOIN y paginación | `paso-04-taller-1-filtros-join-y-paginacion/01-repository.py` | `app/repository.py` |
| 4. Taller 1: filtros, JOIN y paginación | `paso-04-taller-1-filtros-join-y-paginacion/02-comandos.sh` | terminal, en la raíz de tu repositorio |
| 4. Taller 1: filtros, JOIN y paginación | `paso-04-taller-1-filtros-join-y-paginacion/03-repository.py` | `app/repository.py` (sigue en el mismo archivo) |
| 5. Taller 2: agendar sin colisiones | `paso-05-taller-2-agendar-sin-colisiones/01-fragmento.py` | ver el texto del paso en el codelab |
| 5. Taller 2: agendar sin colisiones | `paso-05-taller-2-agendar-sin-colisiones/02-fragmento.py` | ver el texto del paso en el codelab |
| 5. Taller 2: agendar sin colisiones | `paso-05-taller-2-agendar-sin-colisiones/03-comandos.sh` | terminal, en la raíz de tu repositorio |
| 6. Consola, ruff y seguridad | `paso-06-consola-ruff-y-seguridad/01-comandos.sh` | terminal, en la raíz de tu repositorio |

# Escríbelo tú

En este paso del codelab la pieza clave la escribes a mano, sin agente, antes de comparar con la referencia.

## Paso 5. Taller 2: agendar sin colisiones

**Escríbelo tú: la consulta de traslape.**

**Pedido.** Esta pieza va a mano, sin agente. En `schedule_visit` de `app/repository.py`, después de comprobar que la propiedad existe y no está vendida, escribe la consulta que busca una visita de la misma propiedad que se traslape con la nueva, y lanza `VisitSlotConflictError` si la encuentra. El resto puedes escribirlo tú o pedírselo al agente con el pedido de este paso. Si el agente reescribe tu consulta, compara su versión con la tuya.

**Pista.** Es un `select(Visit.id)` con tres condiciones en el `where`: la misma `property_id`, `scheduled_start` de la existente menor que el fin de la nueva y `scheduled_end` de la existente mayor que el inicio de la nueva. Con `.first()` te basta saber si hay una. Usa `<` y `>`, no `<=`: tocar el borde está permitido.

**Verifica.** Corre `uv run pytest tests/test_workshop.py -k schedule_visit -v`. Los cuatro tests de `schedule_visit` deben pasar, entre ellos `test_schedule_visit_rejects_overlap_and_allows_contiguous`, que prueba el traslape y el borde, y `test_schedule_visit_is_atomic_under_concurrency`, que lanza 10 reservas en hilos. Si el de los bordes falla, revisa si usaste `<=`.

---
name: fastapi-tests-que-atrapan-errores
description: Usar cuando hay que escribir tests para lógica de un proyecto Python o FastAPI y el objetivo es que atrapen errores reales ("tests que sirvan", "¿qué casos pruebo?", cobertura alta que no detecta bugs, tests que pasan con código roto), o al revisar si una suite existente protege algo.
---

# Tests que atrapan errores reales

Un test vale si pasa con la implementación correcta y falla con un error plausible que la suite actual no atrapa. Diez tests del mismo concepto valen como uno. La forma de comprobarlo es sembrar el error (un mutante) y ver que el test lo detecta. Para montar fixtures, base de prueba o dobles de APIs externos usa la skill `fastapi-pruebas-pytest-httpx`.

1. Lee el contrato (README, docstrings, tabla de errores) y los tests existentes. Anota lo que ya está cubierto.
2. Lista los conceptos sin test, buscando en estas familias.

   | Concepto | Error plausible |
   |---|---|
   | Borde exacto | `<` en lugar de `<=` en un límite de monto o de intentos |
   | Orden de errores | responde el 400 de validación de negocio antes que el 404 |
   | Atomicidad | una operación rechazada deja datos cambiados a medias |
   | Pertenencia | acepta el id de otro dueño o de otro padre |
   | Derivados | totales, saldos o `updated_at` quedan viejos |
   | `null` frente a ausente | acepta `null` donde el contrato lo prohíbe |
   | Normalización | mayúsculas, espacios o Unicode que deberían ser lo mismo |
   | Orden determinista | la lista cambia de orden o repite filas al paginar |
   | Tiempo | ventana que no se libera, reloj real en lugar del inyectado |
   | Concurrencia | dos peticiones simultáneas rompen una regla de unicidad |

3. Escribe un test por concepto, con un nombre que diga qué verifica y un docstring de una línea con el error que atrapa. Prueba por la interfaz pública (HTTP o la función pública), nunca por atributos privados como `guard._failures`, que se rompen al refactorizar sin que haya bug.
4. Afirma solo lo que fija el contrato. El texto exacto de un mensaje o el orden de campos de un JSON hacen frágil el test.
5. Hazlo determinista. Reloj inyectable o falso en lugar de `sleep`, semillas fijas y datos propios en cada test. Para concurrencia, lanza las peticiones con hilos y una `threading.Barrier` para que arranquen juntas, y vuelve lenta la parte crítica con un doble inyectado, no con `sleep` en el código.
6. Comprueba cada test con su mutante. Siembra a mano en el código el error que describe el docstring, confirma que ese test falla por una aserción (no por un error de importación o del fixture) y que la suite que ya existía sigue en verde con el mutante; si ella también lo atrapa, tu test no agrega nada. Deshaz restaurando el texto exacto o con `git stash push -- app/` (un `git stash` sin ruta guarda también tus tests nuevos); `git checkout -- RUTA` borra cambios sin commit que no son tuyos. Si no falla, el test no atrapa nada y se cambia. Para hacerlo repetible, deja la lista de mutantes en el PR o, si el proyecto lo acepta como dependencia de desarrollo, usa `mutmut`.
7. Reporta una tabla con test, concepto, mutante sembrado y si lo atrapó, y la salida de `pytest`. Si escribiste más de cinco, marca los esenciales (los que atrapan un mutante que ningún otro atrapa); una suite que nadie quiere mantener se borra.

```python
def test_rejected_patch_leaves_expense_unchanged(client, create_trip, add_expense) -> None:
    """Atrapa un PATCH no atómico que cambia campos y luego falla por la moneda."""
    trip = create_trip(currency="GTQ")
    exp = add_expense(trip)
    before = client.get(f"/api/v1/trips/{trip['id']}/expenses").json()
    # Moneda válida pero distinta de la del viaje: la rechaza el dominio (400), no el modelo (422).
    r = client.patch(f"/api/v1/trips/{trip['id']}/expenses/{exp['id']}",
                     json={"description": "Nueva", "currency": "EUR"})
    assert r.status_code == 400
    assert client.get(f"/api/v1/trips/{trip['id']}/expenses").json() == before
```

## Errores comunes

| Error | Corrección |
|---|---|
| Copiar un test existente con otros datos | buscar un concepto nuevo |
| `pytest.raises` o asserts que fijan un bug actual como esperado | el test describe lo correcto; si hoy falla, `pytest.mark.xfail(strict=True)` con el motivo |
| Cobertura del 100 % como meta | la meta es atrapar mutantes |

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

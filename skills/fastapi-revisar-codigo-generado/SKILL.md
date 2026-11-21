---
name: fastapi-revisar-codigo-generado
description: Usar cuando hay que revisar un pull request, un diff o código generado por IA en un proyecto Python o FastAPI antes de mergearlo o aceptarlo ("¿lo mergeo?", "revisa lo que hizo el asistente", code review, auditoría del PR).
---

# Revisar un PR de FastAPI

El código generado se ve bien y corre. Se revisa contra el contrato y las reglas del proyecto, buscando los defectos que la IA repite, y con evidencia de tests y linter corriendo sobre la rama, no solo leyendo.

1. Lee el contrato (README, issue o descripción del PR), `AGENTS.md` si existe, `git diff main...RAMA --stat` y el diff completo. Si solo tienes un diff suelto, aplícalo en una copia para poder correrlo, o dilo en la evidencia.
2. Revisa la integridad primero. Tests borrados o debilitados (`assert True`), cambios en `conftest.py`, workflows de CI, `pyproject.toml` o lockfile sin razón, y correcciones que cambian el test en lugar del código son bloqueantes.
3. Recorre la tabla y anota cada hallazgo con archivo y línea, qué pasa en producción y cómo se corrige.

   | Área | Qué buscar |
   |---|---|
   | Contrato | rutas, códigos y orden de errores; `response_model` declarado |
   | Modelos | `extra="forbid"`, entrada distinta de salida, límites, `.dict()` obsoleto en vez de `model_dump(exclude_unset=True)` |
   | Dinero | `float`, `round()` o tolerancias en lugar de `Decimal` o centavos |
   | Capas | `HTTPException` o imports de FastAPI en el dominio, consultas en la ruta |
   | Errores | `dict[...]`, `next(...)` o `None` que terminan en 500 |
   | Atomicidad | muta antes de validar; verificar y escribir sin transacción o candado |
   | Datos | sesión global, consultas dentro de un `for` (N+1), SQL concatenado, paginación sin orden estable |
   | Seguridad | ruta por id sin comprobar dueño (IDOR), dueño tomado del cuerpo, secretos en el código, CORS `*` con credenciales, mensajes que revelan si una cuenta existe |
   | Operación | `print` en lugar de logging, datos personales en logs |
   | Tests | ¿hay tests que fallarían sin el cambio? |

4. En la rama corre `uv run pytest`, `uv run ruff check .` y `uv run ruff format --check .`, y compara con `main`. Cuenta solo lo que el PR rompe o arregla.
5. Demuestra el hallazgo más grave con un test que falla en la rama (por ejemplo, otro usuario aplica un descuento a un inmueble ajeno y recibe 200). Ese test se entrega con el PR marcado `xfail(strict=True)` con el motivo, para que la CI no quede roja y el arreglo lo vuelva verde; si el proyecto prohíbe tocar tests, se entrega como archivo aparte.
Bloqueante es lo que pierde o expone datos, da resultados incorrectos, rompe el contrato o debilita tests. Importante es lo que fallará en producción pronto (500, rendimiento, logs). Menor es estilo.

6. Entrega el veredicto con esta forma y, aparte, el comentario listo para pegar en GitHub. Si el PR mezcla varias cosas, pide dividirlo.

```
Veredicto: no mergear | mergear con cambios | mergear
Bloqueantes (impiden el merge)
1. archivo:linea - que pasa en produccion - correccion
Importantes (antes del release)
Menores
Evidencia: pytest N passed, M failed en la rama (main: ...); ruff OK o falla
Test de regresion agregado: ruta::nombre
```

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

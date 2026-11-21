---
name: fastapi-migraciones-alembic
description: Usar cuando hay que cambiar el esquema de una base de datos con datos reales en un proyecto Python (agregar, renombrar o hacer obligatoria una columna, cambiar un tipo), el proyecto usa create_all o borra la base para aplicar cambios, o se va a introducir Alembic en un proyecto que ya está en producción.
---

# Migraciones con Alembic sin perder datos

Si la base vive en el disco del contenedor (SQLite en Cloud Run) y se pierde en cada despliegue, no hay datos que migrar; dilo y resuelve primero dónde viven los datos. `create_all` no altera tablas que ya existen, y borrar la base no es un plan cuando hay datos. Cada cambio de esquema es una migración versionada, probada en el mismo motor que producción y aplicada antes de que el código nuevo la necesite. Los valores para rellenar datos viejos son decisiones del negocio, no del agente.

1. Si el proyecto no tiene Alembic, instálalo (`uv add alembic`), corre `alembic init migrations`, apunta `env.py` a la URL de configuración y a `Base.metadata` (o `SQLModel.metadata`).
2. Crea la línea base desde el esquema real. Genera la primera migración con `alembic revision --autogenerate` contra una base vacía, compárala con el esquema de producción (pide a quien tenga acceso un `pg_dump --schema-only`) y, si coinciden, marca producción con `alembic stamp head` sin ejecutarla. Si no coinciden, primero se corrige la diferencia.
3. Escribe la migración del cambio con `alembic revision --autogenerate -m "..."` y léela línea por línea. Autogenerate ve un renombre como borrar y crear (pierde datos); cámbialo a `op.alter_column(..., new_column_name=...)` o al patrón de abajo.
4. Para cambios que rompen, usa expandir y contraer en despliegues separados.

   | Cambio | Paso 1 (expandir) | Paso 2 | Paso 3 (contraer) |
   |---|---|---|---|
   | Columna obligatoria nueva | agregarla `nullable=True` | rellenar con el valor que decidió el negocio | `nullable=False` |
   | Renombrar columna | agregar la nueva y escribir en ambas | copiar datos y leer de la nueva | borrar la vieja cuando ningún código la use |
   | Cambiar tipo (`Float` a `Numeric`) | columna nueva con el tipo correcto | copiar con conversión explícita y revisar redondeos | borrar la vieja |

5. Pregunta el valor de relleno (`due_date` de las tareas viejas) y escríbelo en la migración con un comentario de quién lo decidió.
6. Escribe `downgrade()` y pruébalo. Si un paso no se puede deshacer sin perder datos, dilo en la migración.
7. Prueba en el mismo motor que producción, nunca solo en SQLite. Por ejemplo `docker run -d --name pg -e POSTGRES_PASSWORD=dev -p 5433:5432 postgres:17`, carga datos parecidos a los reales, corre `alembic upgrade head`, `alembic downgrade -1` y otra vez `upgrade head`, y revisa los datos. Mira también el SQL con `alembic upgrade head --sql`. Si no hay Docker ni Postgres disponible, usa uno local (Homebrew, Postgres.app) o una base de staging; si no se puede ninguno, entrega la migración marcada como no probada en el motor real y dilo como bloqueante.
8. Quita `create_all` del arranque de la app y deja que las migraciones creen el esquema, también en los tests (o crea las tablas desde `metadata` solo en la base de prueba).
9. En el despliegue, la migración corre antes que el código nuevo y una sola vez (un job o un paso del pipeline, no en el arranque de cada instancia). Haz respaldo antes en producción.
10. Reporta las migraciones, el resultado de upgrade y downgrade en el motor real y los pasos de contraer que quedan pendientes.

```python
def upgrade() -> None:
    op.add_column("tasks", sa.Column("due_date", sa.Date(), nullable=True))
    # Valor decidido por el negocio (2026-11-05): fecha de creacion + 7 dias (supone una columna created_at).
    op.execute("UPDATE tasks SET due_date = created_at::date + 7 WHERE due_date IS NULL")
    op.alter_column("tasks", "due_date", nullable=False)
```

Este ejemplo hace los tres pasos juntos y solo es seguro si ningún código viejo inserta tareas mientras corre; si lo hace, separa el último paso en otro despliegue.

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

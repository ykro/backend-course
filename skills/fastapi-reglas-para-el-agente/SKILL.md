---
name: fastapi-reglas-para-el-agente
description: Usar cuando un asistente de código repite errores en un proyecto Python o FastAPI (lógica en las rutas, float para dinero, datetime.now() suelto, tests modificados), hay que escribir o ampliar AGENTS.md, CLAUDE.md o GEMINI.md, o el asistente ignora las reglas del proyecto.
---

# Reglas para el asistente en AGENTS.md

Una regla sirve si se puede comprobar en el código, con un test o con un comando, y nace de algo que el asistente hizo mal o podría hacer mal en este proyecto. Pocas reglas que se cumplen valen más que un archivo largo que nadie lee. Una regla que deja la decisión abierta ("usa Decimal o centavos") no es regla.

1. Lee el `AGENTS.md` actual si existe y el código. Ubica dónde están rutas, dominio, modelos, configuración y tests, y cómo se corren (`uv run pytest`, `uv run ruff check .`).
2. Contrasta lo que dice la persona con el código (`grep`) y reporta si no coincide; un `grep` no ve alias ni imports indirectos, así que dilo. Lista los errores que el asistente cometió o cometería aquí. Dónde pone la lógica, con qué tipo maneja dinero, de dónde saca la hora, qué archivos no se tocan, qué no debe revelar una respuesta, qué comandos deben pasar.
3. Cierra cada decisión antes de escribir la regla. Si el proyecto aún no decidió (Decimal o centavos), pregúntalo; la regla dice una sola cosa.
4. Escribe cada regla en una línea con qué se cumple, dónde y cómo se comprueba.
   - "El código debe ser limpio" no sirve.
   - "Toda hora sale de `app/clock.py` (`get_clock()`); `datetime.now(` solo aparece en ese archivo. Lo comprueba `grep -rn 'datetime.now(' app/ | grep -v clock.py` vacío" sí sirve.
5. Si una regla necesita algo que no existe (el módulo `clock.py`, la regla de Ruff, el job de CI), créalo en el mismo cambio o márcalo como pendiente con su tarea. Una regla que falla desde el primer día enseña al asistente a ignorarlas. Si el proyecto está desordenado (todo en `main.py`, sin tests), escribe las reglas para el estado al que se quiere llegar y una lista corta de tareas para llegar, en vez de refactorizar todo en el mismo cambio.
6. Mantén el archivo corto. Entre cinco y quince reglas en secciones (cómo trabajar, arquitectura, datos, seguridad, comandos). Lo que se puede automatizar va al linter o a un test y la regla solo lo menciona.
7. Haz que la herramienta lo lea. Antigravity y Codex leen `AGENTS.md` solos. Claude Code necesita `CLAUDE.md` con la línea `@AGENTS.md` y Gemini CLI, `GEMINI.md` con la misma línea.
8. Comprueba el efecto. Pide al asistente, en una conversación nueva, el mismo cambio que antes salió mal y compara. Si sigue igual, la regla no se está leyendo o está mal redactada.

Ejemplos con la forma correcta.

```
- La logica vive en app/services/; las rutas en app/api/ solo validan, llaman al servicio con Depends y devuelven el modelo de salida. Un test de arquitectura falla si app/api importa sqlalchemy.
- El dinero es Decimal de punta a punta (columna Numeric(12, 2), modelos con Decimal). Un test falla si app/schemas.py o app/models.py contienen float.
- Ningun test existente se edita para que pase; si un test parece incorrecto, se explica y se espera aprobacion.
- Antes de decir "listo" corren uv run pytest y uv run ruff check . y se muestra la salida.
```

Mientras esperas una respuesta, adelanta lo que no depende de ella y entrega tu propuesta por defecto para que la persona solo tenga que aprobarla.

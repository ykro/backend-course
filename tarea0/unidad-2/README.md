# Tarea 0 (warmup): paginación, intervalos y capas en Python puro

Seis funciones y diez tests para practicar, sin base de datos, las ideas que usaremos con SQLModel. Duración estimada: 45 minutos.

| Koan | Función en `koans.py` | Concepto |
| ---: | :--- | :--- |
| 1 | `compute_pagination(total, page, size)` | `offset = (page - 1) * size` y `pages = ceil(total / size)`, con 0 páginas si no hay resultados |
| 2 | `normalize_city_filter(city)` | Filtro opcional: minúsculas, sin espacios extremos, `None` si viene vacío |
| 3 | `intervals_overlap(start_a, end_a, start_b, end_b)` | Traslape de intervalos semiabiertos: `[10:00, 11:00)` y `[11:00, 12:00)` no chocan |
| 4 | `filter_properties_in_memory(rows, ...)` | Predicados opcionales combinados con AND, como un `WHERE` dinámico |
| 5 | `join_properties_with_agencies(properties, agencies)` | `JOIN` en memoria en O(N + M) con un diccionario, sin búsquedas dentro del ciclo |
| 6 | `managed_session_lifecycle(events)` | Generador con `yield` y `finally`: el cierre ocurre incluso si hay una excepción |

## Ejecución

```bash
uv run pytest -v       # al inicio: 10 en rojo
```

Implementa cada función en `koans.py` hasta tener los 10 tests en verde. No modifiques `test_koans.py`.

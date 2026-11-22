# Tarea 0 (nivelación): Python moderno, Decimal y asincronismo

Esta tarea previa asegura que domines lo que usaremos en FastAPI: anotaciones de tipos modernas (`list[str]`, `dict[str, Decimal]`, `str | None`), comprensiones, el error del argumento mutable por defecto, dinero exacto con `Decimal` y corrutinas con `async`/`await`.

Además te sirve para instalar todo **antes** del taller: la primera ejecución de `uv` descarga Python 3.13 y las dependencias, y puede tardar varios minutos con una conexión lenta.

## Cómo ejecutar

Desde esta carpeta (`guide/task0-warmup`):

```bash
uv run pytest -v
```

Al inicio verás 10 tests en rojo. Implementa las funciones de `koans.py` (reemplaza cada `raise NotImplementedError`) hasta que los 10 pasen. No modifiques `test_koans.py`.

## Funciones

1. `normalize_participant_name(raw_name)`: quita espacios repetidos y pasa a formato título.
2. `append_participant_safe(name, group=None)`: devuelve una lista nueva sin mutar la recibida.
3. `parse_amount(raw)`: texto a `Decimal` con 2 decimales y `ROUND_HALF_UP`; rechaza montos inválidos.
4. `filter_valid_amounts(amounts, min_amount)`: list comprehension con montos mayores al mínimo.
5. `split_in_cents(total, count)`: reparto sin perder centavos (`divmod` sobre centavos enteros).
6. `summarize_by_payer(expenses)`: suma por pagador de montos que llegan como texto.
7. `format_currency_tag(amount, currency)`: `"GTQ 15.50"`.
8. `find_top_spender(totals)`: mayor total, con desempate alfabético.
9. `merge_trip_tags(base, extra)`: unión sin duplicados, en minúsculas y ordenada.
10. `fetch_exchange_rate_async(currency, delay)`: espera con `asyncio.sleep` (no `time.sleep`) y devuelve una tasa `Decimal`.

## Pistas

- `Decimal("0.1")` es exacto; `Decimal(0.1)` copia el error del `float`. Crea los `Decimal` desde texto.
- `Decimal("12.345").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` da `Decimal("12.35")`.
- Un valor por defecto como `group=[]` se crea una sola vez, cuando Python define la función.

"""Tarea 0 (nivelación): 10 koans de Python moderno para FastAPI.

Completa cada función reemplazando NotImplementedError hasta que pasen los tests.
"""

import asyncio
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENT = Decimal("0.01")


def normalize_participant_name(raw_name: str) -> str:
    """1. Quita espacios repetidos y pasa a formato título: '  ana   maría  ' -> 'Ana María'."""
    raise NotImplementedError("Implementa normalize_participant_name")


def append_participant_safe(name: str, group: list[str] | None = None) -> list[str]:
    """2. Devuelve una lista NUEVA con el nombre normalizado al final, sin mutar group."""
    raise NotImplementedError("Implementa append_participant_safe")


def parse_amount(raw: str) -> Decimal:
    """3. Convierte texto a Decimal con 2 decimales (ROUND_HALF_UP).

    Lanza ValueError("Monto inválido") si el texto no es un número finito mayor que 0.
    """
    raise NotImplementedError("Implementa parse_amount")


def filter_valid_amounts(amounts: list[Decimal], min_amount: Decimal = Decimal("0")) -> list[Decimal]:
    """4. Con una list comprehension, conserva los montos estrictamente mayores a min_amount."""
    raise NotImplementedError("Implementa filter_valid_amounts")


def split_in_cents(total: Decimal, count: int) -> list[Decimal] | None:
    """5. Reparte total entre count personas sin perder centavos.

    Devuelve None si count <= 0 o total <= 0. Los centavos sobrantes van a las
    primeras posiciones y la suma de la lista es exactamente total.
    """
    raise NotImplementedError("Implementa split_in_cents")


def summarize_by_payer(expenses: list[dict[str, str]]) -> dict[str, Decimal]:
    """6. Suma por pagador montos que llegan como texto: [{'paid_by': 'Ana', 'amount': '25.50'}]."""
    raise NotImplementedError("Implementa summarize_by_payer")


def format_currency_tag(amount: Decimal, currency: str = "USD") -> str:
    """7. Devuelve el código ISO en mayúsculas y el monto con 2 decimales: 'GTQ 15.50'."""
    raise NotImplementedError("Implementa format_currency_tag")


def find_top_spender(totals_by_payer: dict[str, Decimal]) -> str | None:
    """8. Nombre con mayor total; en empate, el primero en orden alfabético. None si está vacío."""
    raise NotImplementedError("Implementa find_top_spender")


def merge_trip_tags(base_tags: list[str], extra_tags: list[str]) -> list[str]:
    """9. Une ambas listas en minúsculas, sin espacios extra, sin duplicados y ordenadas."""
    raise NotImplementedError("Implementa merge_trip_tags")


async def fetch_exchange_rate_async(currency: str, delay_seconds: float = 0.01) -> Decimal:
    """10. Simula una consulta no bloqueante con asyncio.sleep y devuelve la tasa respecto a USD.

    Tasas: USD 1.00, GTQ 7.75, EUR 0.92, MXN 18.50. Moneda desconocida: ValueError('Moneda no soportada').
    """
    raise NotImplementedError("Implementa fetch_exchange_rate_async")

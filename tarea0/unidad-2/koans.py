from __future__ import annotations

from collections.abc import Generator
from datetime import datetime
from typing import Any


def compute_pagination(total: int, page: int, size: int) -> dict[str, int]:
    """Koan 1: Calcula offset y total de páginas (pages) para una consulta SQL.
    - Si page < 1 o size < 1, lanza ValueError.
    - Retorna {"offset": ..., "limit": size, "total": total, "pages": ...}.
    """
    raise NotImplementedError("TODO Koan 1: Implementar compute_pagination")


def normalize_city_filter(city: str | None) -> str | None:
    """Koan 2: Normaliza el filtro de ciudad a minúsculas sin espacios extremos, o None si está vacío."""
    raise NotImplementedError("TODO Koan 2: Implementar normalize_city_filter")


def intervals_overlap(
    start_a: datetime,
    end_a: datetime,
    start_b: datetime,
    end_b: datetime,
) -> bool:
    """Koan 3: Determina si dos intervalos semiabiertos [start_a, end_a) y [start_b, end_b) se traslapan.
    - Si end_a <= start_a o end_b <= start_b, lanza ValueError.
    - Recuerda: dos intervalos contiguos [10:00, 11:00) y [11:00, 12:00) NO se traslapan.
    """
    raise NotImplementedError("TODO Koan 3: Implementar intervals_overlap")


def filter_properties_in_memory(
    rows: list[dict[str, Any]],
    city: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    min_bedrooms: int | None = None,
) -> list[dict[str, Any]]:
    """Koan 4: Filtra la lista de propiedades aplicando solo los criterios no nulos y ordena por id asc."""
    raise NotImplementedError("TODO Koan 4: Implementar filter_properties_in_memory")


def join_properties_with_agencies(
    properties: list[dict[str, Any]],
    agencies: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Koan 5: Une cada propiedad con el nombre de su agencia ('agency_name') en O(N + M)."""
    raise NotImplementedError("TODO Koan 5: Implementar join_properties_with_agencies")


def managed_session_lifecycle(events: list[str]) -> Generator[dict[str, bool]]:
    """Koan 6: Generador con yield y finally que registra 'opened' al iniciar y 'closed' al cerrar."""
    raise NotImplementedError("TODO Koan 6: Implementar managed_session_lifecycle")

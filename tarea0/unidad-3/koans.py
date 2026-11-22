"""Tarea 0 de la Unidad 3: 11 koans de seguridad en Python puro.

Implementa cada función hasta que `uv run pytest -v` quede en verde. No necesitas
FastAPI: son las piezas lógicas que luego usarás en EstateHub Cloud.
"""

from __future__ import annotations

from typing import Any


def sanitize_agent_public(raw_agent: dict[str, Any]) -> dict[str, Any]:
    """Koan 1. Devuelve un dict NUEVO solo con id, name (sin espacios en los extremos),
    email (sin espacios y en minúsculas) y role. Cualquier otro campo se descarta.
    """
    raise NotImplementedError("Koan 1")


def is_token_expired(payload: dict[str, Any], now: int) -> bool:
    """Koan 2. True si 'exp' falta, no es int o exp <= now."""
    raise NotImplementedError("Koan 2")


def claims_problem(payload: dict[str, Any], now: int, issuer: str, audience: str) -> str | None:
    """Koan 3. Revisa los claims en este orden y devuelve el primer problema:
    "expired" (usa el koan 2), "bad_issuer" (iss distinto de issuer) o
    "bad_audience" (aud distinto de audience; aud puede ser str o lista de str).
    Devuelve None si todo está bien.
    """
    raise NotImplementedError("Koan 3")


def evaluate_property_access(current_agent: dict[str, Any] | None, property_owner_id: int) -> int:
    """Koan 4. 401 si no hay agente; 200 si es dueño o su role es "admin"; 403 en otro caso."""
    raise NotImplementedError("Koan 4")


def cors_response_headers(origin: str, allowed_origins: list[str]) -> dict[str, str]:
    """Koan 5. Cabeceras CORS que respondería una API con credenciales.

    - Si "*" está en allowed_origins, lanza ValueError (prohibido con credenciales).
    - Si origin está en la lista (comparación exacta), devuelve
      {"Access-Control-Allow-Origin": origin, "Access-Control-Allow-Credentials": "true",
       "Vary": "Origin"}.
    - Si no está, devuelve {} (el navegador bloqueará la lectura de la respuesta).
    """
    raise NotImplementedError("Koan 5")


def resolve_cloud_run_port(env: dict[str, str]) -> int:
    """Koan 6. Lee env["PORT"] (default "8080"), lo convierte a int y valida 1..65535.
    Si no es un entero válido en ese rango, lanza ValueError.
    """
    raise NotImplementedError("Koan 6")


def verify_hmac_signature(message: str, signature_hex: str, secret_key: str) -> bool:
    """Koan 7. Calcula HMAC-SHA256 de message con secret_key y compáralo con
    signature_hex usando hmac.compare_digest.
    """
    raise NotImplementedError("Koan 7")


def escape_html(text: str) -> str:
    """Koan 8. Escapa & < > " ' como &amp; &lt; &gt; &quot; &#x27; (el & primero)."""
    raise NotImplementedError("Koan 8")


def is_strong_secret(value: str, known_examples: set[str]) -> bool:
    """Koan 9. True solo si value tiene al menos 32 caracteres y value.strip().lower()
    no aparece en known_examples (comparando también en minúsculas).
    """
    raise NotImplementedError("Koan 9")


def public_validation_errors(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Koan 10. Para cada error de Pydantic conserva solo loc (como lista), msg y type.
    Descarta input, ctx, url y cualquier otra llave.
    """
    raise NotImplementedError("Koan 10")


def untrusted_block(data: dict[str, Any]) -> str:
    """Koan 11. Serializa data como JSON (ensure_ascii=False, sort_keys=True), reemplaza
    cada "<" por "\\u003c" y lo envuelve así:
    "<datos_no_confiables>\\n{json}\\n</datos_no_confiables>"
    Así el texto del usuario no puede cerrar la etiqueta que lo delimita en un prompt.
    """
    raise NotImplementedError("Koan 11")

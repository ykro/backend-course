"""Tests de la Tarea 0. Ejecuta: uv run pytest -v"""

import asyncio
from decimal import Decimal

import pytest

from koans import (
    append_participant_safe,
    fetch_exchange_rate_async,
    filter_valid_amounts,
    find_top_spender,
    format_currency_tag,
    merge_trip_tags,
    normalize_participant_name,
    parse_amount,
    split_in_cents,
    summarize_by_payer,
)

D = Decimal


def test_1_normalize_participant_name() -> None:
    assert normalize_participant_name("  ana   maría  ") == "Ana María"
    assert normalize_participant_name("CARLOS") == "Carlos"


def test_2_append_participant_safe_does_not_share_mutable_default() -> None:
    assert append_participant_safe("ana") == ["Ana"]
    assert append_participant_safe("luis") == ["Luis"]
    original = ["Pedro"]
    assert append_participant_safe("sofía", original) == ["Pedro", "Sofía"]
    assert original == ["Pedro"]


def test_3_parse_amount_rounds_half_up_and_rejects_invalid() -> None:
    assert parse_amount(" 12.345 ") == D("12.35")
    assert parse_amount("12.344") == D("12.34")
    assert parse_amount("7") == D("7.00")
    for bad in ["0", "-3.50", "doce", "NaN"]:
        with pytest.raises(ValueError, match="Monto inválido"):
            parse_amount(bad)


def test_4_filter_valid_amounts() -> None:
    raw = [D("-10.00"), D("0.00"), D("12.35"), D("5.10")]
    assert filter_valid_amounts(raw) == [D("12.35"), D("5.10")]
    assert filter_valid_amounts(raw, min_amount=D("10.00")) == [D("12.35")]


def test_5_split_in_cents_never_loses_a_cent() -> None:
    shares = split_in_cents(D("100.00"), 3)
    assert shares == [D("33.34"), D("33.33"), D("33.33")]
    assert sum(shares) == D("100.00")
    assert split_in_cents(D("0.05"), 4) == [D("0.02"), D("0.01"), D("0.01"), D("0.01")]
    assert split_in_cents(D("100.00"), 0) is None
    assert split_in_cents(D("-50.00"), 2) is None


def test_6_summarize_by_payer_with_text_amounts() -> None:
    expenses = [
        {"paid_by": "Ana", "amount": "30.00"},
        {"paid_by": "Luis", "amount": "15.50"},
        {"paid_by": "Ana", "amount": "19.75"},
    ]
    assert summarize_by_payer(expenses) == {"Ana": D("49.75"), "Luis": D("15.50")}


def test_7_format_currency_tag() -> None:
    assert format_currency_tag(D("15.5"), "gtq") == "GTQ 15.50"
    assert format_currency_tag(D("100")) == "USD 100.00"


def test_8_find_top_spender_breaks_ties_alphabetically() -> None:
    assert find_top_spender({"Ana": D("40"), "Luis": D("95"), "Sofía": D("60")}) == "Luis"
    assert find_top_spender({"Sofía": D("50"), "Ana": D("50")}) == "Ana"
    assert find_top_spender({}) is None


def test_9_merge_trip_tags() -> None:
    assert merge_trip_tags(["Beach", " Food "], ["food", "HOTEL"]) == ["beach", "food", "hotel"]


def test_10_fetch_exchange_rate_async() -> None:
    assert asyncio.run(fetch_exchange_rate_async("gtq", delay_seconds=0.001)) == D("7.75")
    with pytest.raises(ValueError, match="Moneda no soportada"):
        asyncio.run(fetch_exchange_rate_async("JPY", delay_seconds=0.001))

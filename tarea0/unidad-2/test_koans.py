from __future__ import annotations

from datetime import UTC, datetime

import pytest

from koans import (
    compute_pagination,
    filter_properties_in_memory,
    intervals_overlap,
    join_properties_with_agencies,
    managed_session_lifecycle,
    normalize_city_filter,
)


def test_01_pagination_math_standard() -> None:
    res = compute_pagination(total=25, page=3, size=10)
    assert res == {"offset": 20, "limit": 10, "total": 25, "pages": 3}


def test_02_pagination_empty_and_invalid() -> None:
    assert compute_pagination(total=0, page=1, size=10)["pages"] == 0
    with pytest.raises(ValueError):
        compute_pagination(total=10, page=0, size=10)


def test_03_normalize_city_filter() -> None:
    assert normalize_city_filter("  Antigua  ") == "antigua"
    assert normalize_city_filter("   ") is None
    assert normalize_city_filter(None) is None


def test_04_intervals_overlap_true_on_partial_collision() -> None:
    t10 = datetime(2027, 5, 15, 10, 0, tzinfo=UTC)
    t11 = datetime(2027, 5, 15, 11, 0, tzinfo=UTC)
    t1030 = datetime(2027, 5, 15, 10, 30, tzinfo=UTC)
    t1130 = datetime(2027, 5, 15, 11, 30, tzinfo=UTC)
    assert intervals_overlap(t10, t11, t1030, t1130) is True


def test_05_intervals_overlap_false_on_adjacent_touching_boundary() -> None:
    t10 = datetime(2027, 5, 15, 10, 0, tzinfo=UTC)
    t11 = datetime(2027, 5, 15, 11, 0, tzinfo=UTC)
    t12 = datetime(2027, 5, 15, 12, 0, tzinfo=UTC)
    assert intervals_overlap(t10, t11, t11, t12) is False


def test_06_intervals_overlap_invalid_window_raises() -> None:
    t10 = datetime(2027, 5, 15, 10, 0, tzinfo=UTC)
    with pytest.raises(ValueError):
        intervals_overlap(t10, t10, t10, t10)


def test_07_filter_properties_multicriteria() -> None:
    rows = [
        {"id": 3, "city": "Antigua", "price": 390000, "bedrooms": 3},
        {"id": 1, "city": "Antigua", "price": 180000, "bedrooms": 1},
        {"id": 2, "city": "Antigua", "price": 285000, "bedrooms": 2},
        {"id": 4, "city": "Guatemala", "price": 450000, "bedrooms": 4},
    ]
    filtered = filter_properties_in_memory(
        rows, city="  antigua ", min_price=200000, max_price=400000, min_bedrooms=2
    )
    assert [r["id"] for r in filtered] == [2, 3]


def test_08_join_properties_with_agencies() -> None:
    agencies = [{"id": 10, "name": "Altamira"}, {"id": 20, "name": "Veranda"}]
    props = [
        {"id": 1, "title": "Loft", "agency_id": 10},
        {"id": 2, "title": "Huérfana", "agency_id": 99},
    ]
    joined = join_properties_with_agencies(props, agencies)
    assert len(joined) == 1
    assert joined[0]["agency_name"] == "Altamira"


def test_09_managed_session_closes_on_normal_exit() -> None:
    events: list[str] = []
    gen = managed_session_lifecycle(events)
    session = next(gen)
    assert session["open"] is True
    with pytest.raises(StopIteration):
        next(gen)
    assert session["open"] is False
    assert events == ["opened", "closed"]


def test_10_managed_session_closes_on_exception() -> None:
    events: list[str] = []
    gen = managed_session_lifecycle(events)
    session = next(gen)
    with pytest.raises(RuntimeError):
        gen.throw(RuntimeError("Database error"))
    assert session["open"] is False
    assert events == ["opened", "closed"]

def test_list_properties_runs_bounded_queries(
    client: TestClient,
    engine: Engine,
    make_agency: Callable[..., Any],
    make_property: Callable[..., Any],
) -> None:
    """Vigila el problema N+1: listar con el nombre de la agencia no puede crecer con N."""
    for i in range(6):
        agency_id = make_agency(f"Agencia Distinta {i}")["id"]
        make_property(agency_id, title=f"Propiedad {i}")

    statements: list[str] = []

    def record(_conn: Any, _cursor: Any, statement: str, *_args: Any) -> None:
        statements.append(statement)

    event.listen(engine, "before_cursor_execute", record)
    try:
        response = client.get("/api/v1/properties", params={"size": 10})
    finally:
        event.remove(engine, "before_cursor_execute", record)

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 6
    assert {p["agency_name"] for p in items} == {f"Agencia Distinta {i}" for i in range(6)}
    selects = [s for s in statements if s.lstrip().upper().startswith("SELECT")]
    assert len(selects) <= 3, f"Se ejecutaron {len(selects)} SELECT: revisa el problema N+1"

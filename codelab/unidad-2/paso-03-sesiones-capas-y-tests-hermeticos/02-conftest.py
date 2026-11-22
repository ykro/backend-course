def engine() -> Generator[Engine]:
    """Engine SQLite en memoria, aislado por test."""
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    test_engine.dispose()

def client(engine: Engine) -> Generator[TestClient]:
    """TestClient cuya dependencia get_session apunta al engine en memoria del test."""
    yield from _client_for(engine)

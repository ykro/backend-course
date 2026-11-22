def get_session() -> Generator[Session]:
    """Abre una sesión por petición HTTP y la cierra al terminar, incluso si hay error."""
    with Session(engine) as session:
        yield session

def get_repository(session: Session = Depends(get_session)) -> EstateRepository:
    """Inyecta un EstateRepository acoplado a la sesión de la petición actual."""
    return EstateRepository(session)

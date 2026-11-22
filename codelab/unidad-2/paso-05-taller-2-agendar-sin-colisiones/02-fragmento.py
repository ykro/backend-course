    def _begin(connection) -> None:
        wants_lock = connection.get_execution_options().get(WRITE_LOCK_OPTION, False)
        connection.exec_driver_sql("BEGIN IMMEDIATE" if wants_lock else "BEGIN")

def begin_write(session: Session) -> None:
    """Abre la transacción de la sesión tomando el candado de escritura (SQLite: BEGIN IMMEDIATE).

    Debe ser lo primero que hace una operación que verifica y luego escribe: así ninguna otra
    escritura se intercala entre la verificación y la escritura. Las lecturas no lo usan.
    En PostgreSQL esta opción no hace nada (allí se usa EXCLUDE o SELECT ... FOR UPDATE).
    """
    session.connection(execution_options={WRITE_LOCK_OPTION: True})

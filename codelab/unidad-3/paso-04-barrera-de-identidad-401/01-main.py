def get_current_agent(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    repo: RepoDep,
) -> Agent:
    """Barrera 1 (identidad): sin token válido no hay agente y la respuesta es 401."""
    if credentials is None:
        raise AuthenticationError("Falta el encabezado Authorization: Bearer <token>.")
    payload = decode_access_token(credentials.credentials)
    subject = payload.get("sub")
    # Solo dígitos ASCII ("٣" también es isdigit) y dentro del rango de un id: nunca un 500.
    if not isinstance(subject, str) or not (subject.isascii() and subject.isdigit()):
        raise AuthenticationError("Token inválido.")
    if len(subject) > 10 or int(subject) > MAX_ID:
        raise AuthenticationError("Token inválido.")
    agent = repo.get_agent_by_id(int(subject))
    if agent is None:
        raise AuthenticationError("Token inválido.")
    return agent

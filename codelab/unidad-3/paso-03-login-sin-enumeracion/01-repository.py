def authenticate_and_issue_token(self, credentials: TokenRequest) -> TokenResponse:
    email = normalize_email(credentials.email)
    agent = self.session.exec(select(Agent).where(Agent.email == email)).first()
    if agent is None:
        # Mismo costo que una contraseña incorrecta: el tiempo no revela si el correo existe.
        verify_password(credentials.password, decoy_password_hash())
        raise AuthenticationError(INVALID_CREDENTIALS_MESSAGE, code="INVALID_CREDENTIALS")
    if not verify_password(credentials.password, agent.hashed_password):
        raise AuthenticationError(INVALID_CREDENTIALS_MESSAGE, code="INVALID_CREDENTIALS")

    assert agent.id is not None
    token = create_access_token(agent_id=agent.id, role=agent.role)
    return TokenResponse(
        access_token=token,
        expires_in_minutes=settings.jwt_expire_minutes,
        agent=to_agent_public(agent),
    )

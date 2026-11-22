def decode_access_token(token: str) -> dict[str, Any]:
    """Verifica firma, algoritmo, expiración, emisor y audiencia. Cualquier fallo es 401."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
            options={"require": REQUIRED_CLAIMS},
        )
    except jwt.ExpiredSignatureError as exc:
        raise AuthenticationError("El token expiró; inicia sesión de nuevo.") from exc
    except jwt.InvalidTokenError as exc:
        raise AuthenticationError("Token inválido.") from exc
    return dict(payload)

uv sync
cp .env.example .env
uv run python -c "import secrets; print(secrets.token_urlsafe(48))"

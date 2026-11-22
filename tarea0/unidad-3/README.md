# Tarea 0 (antes del taller): koans de seguridad

Implementa las 11 funciones de `koans.py` hasta que las 12 pruebas de `test_koans.py` pasen. Son piezas de Python puro (sin FastAPI) que vas a reconocer en el taller dentro de EstateHub Cloud. Tiempo estimado: 45 a 60 minutos.

```bash
cd task0-warmup   # carpeta de la Tarea 0 dentro del material de la unidad
uv sync
uv run pytest -v
uv run ruff check . && uv run ruff format --check .
```

## Qué practicas y dónde lo vuelves a ver

| Koan | Concepto | En EstateHub Cloud | Lo evalúa |
| :--- | :--- | :--- | :--- |
| 1 `sanitize_agent_public` | DTO público sin hash | `AgentPublic`, `to_agent_public` | Taller (paso 3) |
| 2 `is_token_expired` | Claim `exp` y su borde (`exp <= ahora` ya expiró) | `decode_access_token` | Quiz de la unidad |
| 3 `claims_problem` | `iss` y `aud`: un token válido para otro servicio no sirve aquí | `decode_access_token` | Quiz de la unidad |
| 4 `evaluate_property_access` | Matriz 401, 403 y 200 con rol admin | `_get_owned_property_or_raise` | Taller (paso 5) |
| 5 `cors_response_headers` | CORS con lista blanca exacta y sin `*` con credenciales | `CORSMiddleware`, `CORS_ORIGINS` | Práctica de CORS (abajo) |
| 6 `resolve_cloud_run_port` | Contrato de contenedor: puerto desde `PORT` | `Dockerfile` | Despliegue guiado |
| 7 `verify_hmac_signature` | Firma HMAC-SHA256 y comparación en tiempo constante | firma HS256 del JWT | Quiz de la unidad |
| 8 `escape_html` | Escapar antes de pintar HTML (o usar `textContent`) | `app/ui.py` | Taller (consola) |
| 9 `is_strong_secret` | Secreto obligatorio, largo y no publicado | `Settings.jwt_secret_key` | Quiz de la unidad |
| 10 `public_validation_errors` | Errores 422 sin `input` ni `ctx` | handler de `RequestValidationError` | Quiz de la unidad |
| 11 `untrusted_block` | Datos de usuario delimitados en un prompt | `app/pitch.py` | Quiz de la unidad |

Las pruebas `test_05` y `test_06` cubren el mismo koan 5 (lista blanca y comodín); por eso hay 12 pruebas para 11 funciones.

## Práctica de CORS con el navegador (15 minutos)

1. En la raíz de tu repositorio, levanta el API con `CORS_ORIGINS=["http://localhost:3000"]` en tu `.env` (puerto 8000).
2. En otra terminal, sirve una página vacía desde un origen NO permitido: `uv run python -m http.server 5500` y abre `http://localhost:5500`.
3. En la consola del navegador de esa pestaña ejecuta:

   ```js
   fetch("http://127.0.0.1:8000/api/v1/properties").then(r => r.json()).then(console.log)
   ```

   El navegador muestra un error de CORS y tu código no puede leer la respuesta.
4. Repite con `uv run python -m http.server 3000` y `http://localhost:3000`: ahora la lectura funciona porque ese origen está en la lista blanca.
5. En la terminal: `curl -i http://127.0.0.1:8000/api/v1/properties -H "Origin: http://localhost:5500"`. Anota el código, el cuerpo y las cabeceras de la respuesta y compáralos con lo que pudo leer el navegador en el paso 3.

Conclusión que debes poder explicar: CORS lo aplica el navegador para proteger al usuario; no es un control de acceso del servidor. Lo que protege los datos es la autenticación (401) y la autorización (403).

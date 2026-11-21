---
name: fastapi-auth-jwt
description: Usar cuando hay que implementar, revisar o arreglar inicio de sesión, contraseñas, tokens JWT o permisos en un API FastAPI (OAuth2 password, Bearer, roles, "solo el dueño puede..."), o antes de llevar a producción un API que tiene login.
---

# Autenticación y autorización con JWT en FastAPI

Autenticar es saber quién llama; autorizar es decidir si puede tocar ese recurso. La mayoría de los incidentes están en lo segundo (un usuario lee lo de otro cambiando un id), así que un login "arreglado" con rutas sin comprobación de dueño no está listo para producción.

1. Contraseñas con un hash lento y con sal. Usa `pwdlib` con Argon2 (`uv add "pwdlib[argon2]"` y `PasswordHash.recommended()`). Si hay hashes viejos (MD5, SHA-1), verifica con el algoritmo viejo una sola vez y vuelve a guardar con el nuevo al iniciar sesión.
2. El secreto de firma sale del entorno o de un gestor de secretos, con al menos 32 bytes aleatorios, y la app no arranca si falta. Si estuvo en el código o en git, se rota; eso lo hace quien administra producción, y queda como bloqueante hasta que se haga.
3. Al firmar, `sub` como texto, `exp` corto (15 a 60 minutos), `iat` y, si hay varios servicios, `iss` y `aud`.
4. Al verificar, fija el algoritmo (`algorithms=["HS256"]`, nunca `"none"` ni la lista que traiga el token) y exige `exp` y `sub`. Cualquier error de token es 401 con `WWW-Authenticate: Bearer`.
5. Usa `OAuth2PasswordBearer` o `HTTPBearer` y una dependencia `get_current_user` que devuelve el usuario o lanza 401. Si el usuario fue borrado o desactivado, también 401.
6. Autorización en cada recurso por id. El servicio busca con el dueño (`WHERE id = :id AND owner_id = :uid`) o compara y lanza 403 (o 404 si no quieres revelar que existe). El dueño sale del token, nunca del cuerpo. Los roles (`is_admin`) nunca se aceptan desde la entrada del registro.
7. El login responde igual si el correo no existe o si la contraseña está mal (401 y el mismo mensaje), y tiene límite de intentos por cuenta normalizada y por IP, guardado en un almacén compartido (Redis, la base de datos) si hay más de una instancia. Si cambiar la respuesta del login rompe clientes, mantén la forma vieja y avisa.
8. Prueba al menos login correcto, contraseña mala, correo inexistente con la misma respuesta, token vencido, token con `alg` cambiado, token de otro secreto, y otro usuario que intenta leer, editar y borrar un recurso ajeno.
9. Reporta lo arreglado con la salida de los tests y, aparte, los bloqueantes de producción que siguen abiertos. No digas "listo para producción" mientras haya uno.

```python
from datetime import UTC, datetime, timedelta
import jwt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def create_token(user_id: int, key: str) -> str:
    now = datetime.now(UTC)
    return jwt.encode({"sub": str(user_id), "iat": now, "exp": now + timedelta(minutes=30)},
                      key, algorithm="HS256")

def read_user_id(token: str, key: str) -> int:
    data = jwt.decode(token, key, algorithms=["HS256"], options={"require": ["exp", "sub"]})
    return int(data["sub"])
```

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

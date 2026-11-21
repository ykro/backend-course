---
name: fastapi-seguridad-owasp-api
description: Usar cuando hay que revisar la seguridad de un API Python o FastAPI antes de lanzarlo o después de un incidente - auditoría, pentest liviano, OWASP API Top 10, IDOR o BOLA, asignación masiva, SSRF, CORS, límites de uso, secretos en el código o dependencias vulnerables.
---

# Revisión de seguridad de un API con OWASP API Top 10

Una revisión que solo lee el código produce opiniones. Cada hallazgo se demuestra con una petición contra una copia local y se convierte en un test que falla mientras siga abierto. El informe ordena por gravedad y dice qué corregir primero.

1. Levanta el API en local con una base de prueba y dos usuarios (y un admin si hay roles). Nunca pruebes contra producción sin permiso escrito.
2. Recorre la lista con el código abierto y anota candidatos con archivo y línea.

   | Riesgo (OWASP API 2023) | Qué buscar en FastAPI |
   |---|---|
   | API1 Autorización por objeto (BOLA, IDOR) | rutas con `{id}` que no filtran por dueño |
   | API2 Autenticación rota | `algorithms` abiertos o `"none"`, sin `exp`, hash MD5 o SHA, secreto en el código, login sin límite de intentos, mensajes que revelan si la cuenta existe |
   | API3 Autorización por propiedad | modelos de entrada sin `extra="forbid"` que aceptan `owner_id` o `is_admin`; salidas que exponen hash o datos internos |
   | API4 Consumo sin límite | `limit` sin tope, cuerpos y archivos sin tamaño máximo, sin rate limit |
   | API5 Autorización por función | rutas de admin sin comprobar rol |
   | API6 Flujos de negocio sensibles | registro, cupones o reservas automatizables sin freno |
   | API7 SSRF | rutas que piden una URL que da el cliente (`requests.get(url)`) |
   | API8 Mala configuración | CORS `*` con credenciales, `/docs` abierto si no debe, trazas en errores, `--reload` o `debug` en producción |
   | API9 Inventario | versiones viejas o rutas de prueba publicadas |
   | API10 Consumo inseguro de APIs | respuestas externas usadas sin validar ni timeout |

3. Demuestra cada candidato. Escribe la petición que lo explota (`curl` o un test con `TestClient`) y guarda la respuesta. Lo que no se pudo explotar queda como "posible" con la razón.
4. Revisa dependencias y secretos. `uv export --format requirements-txt --no-hashes > /tmp/req.txt && uvx pip-audit -r /tmp/req.txt --no-deps --disable-pip` (el export ya fija todas las versiones, así que pip-audit no necesita crear un entorno con pip), `git log -p | grep -i "secret\|password\|key"` o `gitleaks detect`, y `.env` versionado.
5. Convierte cada hallazgo confirmado en un test que hoy falla, marcado `xfail(strict=True)` con el id del hallazgo, para que el arreglo lo cambie a verde. Corre `pytest --runxfail` una vez para confirmar que cada uno falla por la razón del hallazgo y no por otra.
6. Escribe el informe en un archivo (`SECURITY_REVIEW.md`) con resumen de una línea, tabla de hallazgos (id, riesgo, gravedad, evidencia, archivo y línea, corrección) y el orden de arreglo. Primero lo que permite leer o cambiar datos ajenos, tomar cuentas o gastar dinero.
7. Si te piden arreglar, hazlo por hallazgo con su test, sin mezclar cambios, y vuelve a correr las pruebas de explotación.

La gravedad la da el impacto real con la evidencia. Un IDOR demostrado en datos de clientes es crítico aunque "sea solo lectura".

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

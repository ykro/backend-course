# Skills de backend con FastAPI

Estas quince skills son para tu trabajo después del curso, en cualquier API con FastAPI, uv, pytest y Cloud Run. Cada una es una carpeta con un archivo `SKILL.md`. Tu asistente de código lee su descripción y la usa sola cuando tu pedido coincide; en Claude Code también la puedes llamar por su nombre, como `/fastapi-revisar-codigo-generado`.

Las cinco primeras llevan el método del curso a tus proyectos. Las otras diez cubren lo que un API necesita para llegar a producción.

| Skill | Cuándo te ayuda |
|---|---|
| `fastapi-endpoint-con-contrato` | agregar o cambiar un endpoint empezando por el contrato y los errores |
| `fastapi-tests-que-atrapan-errores` | escribir tests que fallan cuando la lógica se rompe, no solo tests que suben la cobertura |
| `fastapi-revisar-codigo-generado` | revisar un PR o código generado por IA antes de aceptarlo |
| `fastapi-reglas-para-el-agente` | escribir `AGENTS.md` cuando el asistente repite los mismos errores |
| `fastapi-diagnosticar-cloud-run` | entender por qué falla el despliegue o la revisión en Cloud Run |
| `fastapi-modelos-pydantic` | diseñar modelos de entrada y salida, PATCH, dinero y fechas |
| `fastapi-errores-consistentes` | dar a todos los errores la misma forma y códigos estables |
| `fastapi-pruebas-pytest-httpx` | montar las pruebas con base de prueba, overrides y APIs externos sin red |
| `fastapi-auth-jwt` | contraseñas, tokens JWT y permisos de dueño |
| `fastapi-seguridad-owasp-api` | auditar el API contra el OWASP API Top 10 antes de lanzarlo |
| `fastapi-rendimiento-async` | resolver un API que se congela con varias peticiones a la vez |
| `fastapi-migraciones-alembic` | cambiar el esquema de una base con datos reales |
| `fastapi-versionado-api` | cambiar respuestas sin romper a los clientes que ya existen |
| `fastapi-docker-cloud-run` | escribir el Dockerfile y desplegar en Cloud Run con secretos |
| `fastapi-observabilidad` | logs estructurados, request id, trazas y alertas en producción |

Instálalas en tu carpeta personal y nunca dentro del repositorio de una unidad del curso. Un archivo agregado fuera de tus carpetas cuenta como sospecha de integridad en la rúbrica, y una carpeta `.claude/skills/` o `.agents/skills/` dentro del repo cuenta como eso. Descomprime `backend-fastapi-skills.zip` y copia las quince carpetas de `skills/` (cada una con su `SKILL.md`) al lugar de tu herramienta.

1. Claude Code usa `~/.claude/skills/`.
2. Antigravity usa `~/.gemini/antigravity/skills/`.
3. Gemini CLI usa `~/.gemini/skills/` y también reconoce `~/.agents/skills/`.
4. Codex reconoce `~/.agents/skills/`.
5. Cierra y vuelve a abrir la herramienta (o empieza una conversación nueva) y pregúntale "¿qué skills tienes?" para comprobarlo.

En Mac o Linux, dentro de la carpeta `skills` que sale al descomprimir el ZIP, el comando para Claude Code es `mkdir -p ~/.claude/skills && cp -R fastapi-* ~/.claude/skills/`. En Windows, copia las carpetas con el Explorador a `C:\Users\TU_USUARIO\.claude\skills\`.

En tus proyectos fuera del curso puedes ponerlas dentro del repo si tu equipo las quiere compartir. Si una skill dice algo distinto del `AGENTS.md` del proyecto o de su contrato, mandan esos archivos, y lo que entregas sigue siendo tu responsabilidad.

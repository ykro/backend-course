---
name: fastapi-docker-cloud-run
description: Usar cuando hay que escribir o mejorar el Dockerfile de un API Python o FastAPI, desplegarlo en Cloud Run (gcloud run deploy, Artifact Registry, Secret Manager), o la imagen pesa mucho, corre como root, usa --reload o tiene secretos adentro.
---

# Docker y Cloud Run para un API FastAPI

La imagen es reproducible (dependencias del lockfile), pequeña, no corre como root, no trae secretos y escucha en `$PORT`. El servicio corre con su propia cuenta de servicio, lee los secretos de Secret Manager y tiene un tope de instancias. Nada se da por bueno sin construir la imagen y llamar `/health` en local.

1. Revisa qué gestiona dependencias (`uv.lock`, `requirements.txt`) y cómo arranca la app. Si no hay lockfile, créalo (`uv lock`).
2. Escribe el Dockerfile con la forma de abajo y un `.dockerignore` que excluya `.git`, `.venv`, `.env`, `__pycache__`, tests y datos locales.
3. Asegúrate de que el código lee todo secreto y configuración del entorno (con `pydantic-settings`) y no arranca si falta uno obligatorio. Si el secreto sigue escrito en el código, `--set-secrets` no sirve de nada; ese cambio va primero y el secreto viejo se rota.
4. Construye y prueba en local. `docker build -t api .`, `docker run --rm -p 8080:8080 -e PORT=8080 --env-file .env.local api` y `curl localhost:8080/health`. El `.env.local` es tu archivo de valores de prueba, fuera de git. Si la app escribe archivos (SQLite, subidas), crea esa carpeta con dueño `appuser` (`mkdir -p /app/data && chown appuser /app/data`) o el contenedor muere al arrancar. Revisa el tamaño con `docker images api` y que el proceso no sea root (`docker run --rm api id`).
5. Prepara Google Cloud una sola vez. Repositorio en Artifact Registry, secreto en Secret Manager (`gcloud secrets create jwt-secret --data-file=-`), cuenta de servicio de ejecución sin roles de más y `roles/secretmanager.secretAccessor` sobre ese secreto.
6. Despliega con valores explícitos. Pregunta si el API debe ser público; si no, usa `--no-allow-unauthenticated`.

   ```bash
   gcloud run deploy tareas-api --source . --region us-central1 \
     --service-account tareas-api-run@PROJECT_ID.iam.gserviceaccount.com \
     --set-secrets JWT_SECRET=jwt-secret:latest \
     --set-env-vars GOOGLE_CLOUD_PROJECT=PROJECT_ID \
     --max-instances 3 --memory 512Mi --no-allow-unauthenticated
   ```

7. Si la app usa SQLite o escribe archivos, avisa que el disco de Cloud Run es efímero y por instancia; los datos se pierden. Hace falta Cloud SQL, Firestore o un bucket.
8. Comprueba el servicio desplegado (`/health`, una ruta real y los logs de la revisión) y crea una alerta de presupuesto en el proyecto.
9. Reporta tamaño de imagen, usuario, comandos corridos con su salida y lo pendiente. Para errores de despliegue usa la skill `fastapi-diagnosticar-cloud-run`.

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY app ./app
RUN uv sync --locked --no-dev && useradd --create-home appuser
USER appuser
ENV PATH="/app/.venv/bin:$PATH" PORT=8080 FORWARDED_ALLOW_IPS="*"
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers"]
```

Fija en `COPY --from` la versión de uv que usas en tu máquina (`uv --version`). `FORWARDED_ALLOW_IPS` hace que uvicorn confíe en los headers del proxy de Cloud Run; sin él, `--proxy-headers` no tiene efecto y las URLs que arma la app salen con `http`.

Si `AGENTS.md` u otras reglas del repositorio dicen algo distinto de esta skill, mandan las del repositorio; dilo en tu respuesta.

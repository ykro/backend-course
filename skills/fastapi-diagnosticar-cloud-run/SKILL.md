---
name: fastapi-diagnosticar-cloud-run
description: Usar cuando falla el despliegue de un servicio Python o FastAPI a Cloud Run desde GitHub Actions o gcloud - getAccessToken denied, unauthorized_client, iam.serviceAccounts.actAs, Permission denied en Artifact Registry, "Container failed to start and listen on the port", revisión que no arranca, 503, /health con commit viejo, datos que desaparecen.
---

# Diagnosticar un despliegue a Cloud Run

Ubica en qué paso falló (autenticación, subida de la imagen, despliegue, arranque de la revisión o comprobación de salud) y busca la causa de ese paso. Un síntoma puede venir de otro. Si la revisión nueva no arranca, Cloud Run sigue sirviendo la anterior. No crees llaves JSON de cuentas de servicio ni subas `--min-instances` para "arreglar"; no son la causa y cuestan dinero o seguridad.

1. Si hay varios síntomas, sepáralos y atiende uno por uno, empezando por el que impide desplegar. Anota el job, el paso y el error exacto de la corrida más reciente. Pide también el bloque `auth` del workflow y la configuración del proveedor de identidad si el error es de autenticación.
2. Busca el síntoma en la tabla y confirma la causa con el comando de verificación antes de cambiar nada.
3. Arregla una causa, vuelve a correr y anota el resultado.
4. Si el problema es el arranque, lee la revisión. Si `latestCreated` es distinto de `latestReady`, la nueva no arrancó.

   ```bash
   gcloud run services describe "$SERVICE" --region "$REGION" \
     --format='value(status.latestCreatedRevisionName,status.latestReadyRevisionName)'
   gcloud run services logs read "$SERVICE" --region "$REGION" --limit 50
   ```

5. Al final compara lo que responde el servicio (versión o commit en `/health`) con `git rev-parse HEAD`.

| Síntoma | Causa probable | Verificación y arreglo |
|---|---|---|
| `getAccessToken denied` o `unauthorized_client` | la condición de Workload Identity Federation no coincide con el repositorio. `assertion.repository` distingue mayúsculas, y renombrar el repo o hacer push desde un fork lo cambia | `gcloud iam workload-identity-pools providers describe PROVIDER --workload-identity-pool POOL --location global --format="value(attributeCondition,attributeMapping)"` y comparar `attributeCondition` con `owner/repo` exacto; actualizar el binding `principalSet://.../attribute.repository/owner/repo`; revisar el binding con `gcloud iam service-accounts get-iam-policy DEPLOYER_SA`; para que sobreviva a renombres, mapear `attribute.repository_id=assertion.repository_id` y usar ese atributo en la condición y el binding |
| Token obtenido pero falla `iam.serviceAccounts.actAs` | el deployer no tiene `roles/iam.serviceAccountUser` sobre la cuenta de ejecución | `gcloud iam service-accounts get-iam-policy RUNTIME_SA` |
| `Permission denied` al subir la imagen | falta `roles/artifactregistry.writer` en el repositorio | `gcloud artifacts repositories get-iam-policy REPO --location REGION` |
| `Container failed to start and listen on the port` | la app escucha en otro puerto (8000 fijo), usa `--reload`, o se cae al importar | el `CMD` usa `--port ${PORT:-8080}`; correr la imagen local con `-e PORT=8080` y leer el traceback |
| La revisión arranca y se cae con error de configuración | falta una variable o el secreto no se puede leer | `roles/secretmanager.secretAccessor` a la cuenta de ejecución sobre el secreto, y que el secreto tenga versión |
| `/health` con commit viejo | la revisión nueva falló o no hubo despliegue | revisar la corrida y las revisiones |
| 503 intermitente | arranque lento o memoria agotada | logs `Memory limit exceeded`; subir `--memory` o bajar trabajo en el arranque |
| Los datos desaparecen | SQLite o archivos en el disco del contenedor, que es efímero | base de datos administrada (Cloud SQL, Firestore) o bucket |
| Error de política de organización al hacerlo público | la organización prohíbe `allUsers` | proyecto sin esa política o acceso autenticado |

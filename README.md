# Crea tu backend con FastAPI y Python asistido por IA

Curso en línea de tres unidades. En cada una construyes un API con FastAPI y Python, con tests desde el primer paso, y trabajas con un agente de código sin perder el control de lo que entra a tu proyecto: le pides el código, revisas el diff y lo compruebas con los tests.

Este repositorio es el índice del curso. El código de cada unidad está en su propia plantilla de GitHub, con el proyecto base, los tests y la integración continua listos.

[English version](README.en.md)

## Las unidades

| Unidad | Plantilla | Qué construyes |
| :--- | :--- | :--- |
| 1 | [`backend-course-u1-splitmate`](https://github.com/ykro/backend-course-u1-splitmate) | **SplitMate API**, para repartir los gastos de un grupo: contratos HTTP, Pydantic v2, dinero exacto con `Decimal`, capas y pytest. El reto: un `PATCH` parcial de un gasto, atómico y con recálculo. |
| 2 | [`backend-course-u2-estatehub-sql`](https://github.com/ykro/backend-course-u2-estatehub-sql) | **EstateHub SQL**, la agenda de visitas de una inmobiliaria: SQLModel, patrón Repository, `JOIN`, paginación, consultas N+1 y concurrencia. El reto: reprogramar visitas sin choques y armar la agenda de una agencia. |
| 3 | [`backend-course-u3-estatehub-cloud`](https://github.com/ykro/backend-course-u3-estatehub-cloud) | **EstateHub Cloud**, el mismo API listo para producción: JWT, contraseñas, protección contra IDOR, CSP y CORS, y despliegue en Cloud Run desde GitHub Actions sin llaves. El reto: protección contra fuerza bruta en el login. |

## Cómo empezar

1. Abre la plantilla de la unidad y elige **Use this template > Create a new repository**.
2. Ponle tu propio nombre (no el de la plantilla) y elige visibilidad **Private**: así tu solución del reto no queda a la vista de cualquiera.
3. Clona tu repositorio y, en su raíz:

   ```bash
   uv sync            # instala Python 3.13 y las dependencias exactas de uv.lock
   uv run pytest -v   # al inicio: la demo en verde; el taller y el reto en rojo
   ```

El `README.md` de cada plantilla trae el contrato del reto, qué archivos puedes modificar y la lista para revisar antes de entregar.

## Requisitos

- [uv](https://docs.astral.sh/uv/), que instala Python 3.13 y las dependencias de cada proyecto (no hace falta `pip install` global).
- Git y una cuenta gratuita de GitHub.
- Un editor con un agente de código y las extensiones de Python y Ruff.
- Unidad 3: una cuenta de Google Cloud con facturación activa y la CLI `gcloud`. Docker Desktop es opcional (una sola actividad).
- Haber programado antes en algún lenguaje y usar la terminal a nivel básico. No necesitas experiencia previa con FastAPI.

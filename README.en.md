# Build your backend with FastAPI and Python, assisted by AI

Index of a three-unit online course (taught in Spanish). In each unit you build an API with FastAPI and Python, test-first, working with a coding agent while you review every diff and verify it with tests.

| Unit | Template | What you build |
| :--- | :--- | :--- |
| 1 | [`backend-course-u1-splitmate`](https://github.com/ykro/backend-course-u1-splitmate) | **SplitMate API** (shared expenses): HTTP contracts, Pydantic v2, exact money with `Decimal`, layers and pytest. |
| 2 | [`backend-course-u2-estatehub-sql`](https://github.com/ykro/backend-course-u2-estatehub-sql) | **EstateHub SQL** (real-estate visit scheduling): SQLModel, Repository pattern, joins, pagination, N+1 and concurrency. |
| 3 | [`backend-course-u3-estatehub-cloud`](https://github.com/ykro/backend-course-u3-estatehub-cloud) | **EstateHub Cloud**: JWT, passwords, IDOR protection, CSP and CORS, keyless deployment to Cloud Run from GitHub Actions. |

**Getting started:** open a unit template, choose **Use this template > Create a new repository**, give it your own name, make it **Private**, clone it and run `uv sync` and `uv run pytest -v` in its root. The challenge contract for each unit is in its challenge guide, in the course materials.

**Requirements:** uv (installs Python 3.13), Git and a GitHub account, an editor with a coding agent; for Unit 3, a Google Cloud account with billing and the `gcloud` CLI.

**Pre-course On-Ramp (~60 min):** If you want a quick hands-on warm-up before Unit 1 (HTTP, SQLite SQL, `Depends`, JWT, and concurrency), start with [`ykro/backend-onramp`](https://github.com/ykro/backend-onramp) (step-by-step solution: [`ykro/backend-onramp-solution`](https://github.com/ykro/backend-onramp-solution); full index: [`ykro/courses-onramp`](https://github.com/ykro/courses-onramp)).

**Professional Skills Pack (15 skills):** See [`skills/`](skills/README.md) for 15 production FastAPI skills for professional work beyond the course (API contracts, Pydantic, `pytest`/`httpx`, JWT auth, OWASP API security, async performance, Alembic migrations, versioning, Docker/Cloud Run, and observability).

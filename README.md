## Meal Calorie App (Full Stack)

This repository contains the full‑stack meal calorie application (frontend + backend) built for the Xcelpros take‑home test.

The app allows users to:

- Sign up and log in (JWT-based authentication)
- Look up calorie and macro information for a dish using the USDA FoodData Central API
- View fuzzy‑matched similar items
- Persist and retrieve personal search history

Rate limiting is applied per route using `fastapi-limiter` backed by Redis.

---

## Tech Stack

Backend (FastAPI):

- FastAPI, SQLAlchemy, PostgreSQL
- Redis (rate limiting + lightweight caching layer)
- JWT auth (`python-jose` + custom helpers)
- USDA API client (custom wrapper)

Frontend (Next.js 15, React 19):

- App Router + Server Actions
- Zustand (auth store)
- Tailwind CSS + Radix UI primitives

Infrastructure / Tooling:

- Docker + docker-compose (local orchestration)
- Tests (pytest) for backend

---

## Repository Layout

```
backend/    FastAPI application (API, auth, USDA integration, search history)
frontend/   Next.js application (UI, auth forms, search + dashboard pages)
db/         Initialization SQL for local Postgres
docker-compose.yml  Orchestrates backend, frontend, Postgres, Redis
```

---

## Prerequisites

- Docker & Docker Compose installed
- USDA API key (https://fdc.nal.usda.gov/) for live food lookups

---

## Environment Variables

Both the `backend` and `frontend` folders contain a `.env.example`. Copy each to `.env` before starting.

### Backend `.env`

| Variable             | Purpose                      | Suggested Local Value                                              |
| -------------------- | ---------------------------- | ------------------------------------------------------------------ |
| `USDA_API_KEY`       | USDA API key                 | (your key)                                                         |
| `DATABASE_URL`       | SQLAlchemy connection string | `postgresql+psycopg://postgres:postgres@postgres:5432/mealcalorie` |
| `JWT_SECRET`         | JWT signing secret           | `super-secret-here`                                                |
| `JWT_ALGO`           | JWT algorithm                | `HS256`                                                            |
| `JWT_EXPIRE_MINUTES` | Token lifetime (minutes)     | `60`                                                               |
| `REDIS_URL`          | Redis instance URL           | `redis://redis:6379`                                               |

### Frontend `.env`

| Variable                  | Purpose                                 | Suggested Local Value |
| ------------------------- | --------------------------------------- | --------------------- |
| `NEXT_PUBLIC_BACKEND_URL` | Base URL for API calls from the browser | `http://backend:8000` |

---

## Running Locally (Docker)

From the repo root:

```bash
docker compose up
```

Then open:

- Frontend: http://localhost:3000
- Backend (OpenAPI docs): http://localhost:8000/docs

Stop containers:

```bash
docker compose down
```

---

## Core API Endpoints (Backend)

| Method | Path              | Description                             | Auth Required | Rate Limited |
| ------ | ----------------- | --------------------------------------- | ------------- | ------------ |
| GET    | `/`               | Root welcome message                    | No            | Yes          |
| GET    | `/health`         | Health check                            | No            | No           |
| POST   | `/auth/signup`    | Register user & return JWT              | No            | Yes          |
| POST   | `/auth/login`     | Authenticate user & return JWT          | No            | Yes          |
| POST   | `/get-calories`   | Get best match + similar items + macros | Yes (Bearer)  | Yes          |
| GET    | `/search-history` | Retrieve user search history            | Yes (Bearer)  | Yes          |

All protected endpoints expect an `Authorization: Bearer <token>` header.

---

## Frontend Pages

| Route        | Purpose                            |
| ------------ | ---------------------------------- |
| `/`          | Landing page / entry point         |
| `/login`     | User login form                    |
| `/signup`    | User registration form             |
| `/calories`  | Dish calorie lookup form + results |
| `/dashboard` | User dashboard (auth‑guarded)      |

---

## Screenshots

<table>
	<tr>
		<td>
				<img src="./images/login_page.png" alt="Login page" width="480" height="300" />
			<br /><sub>Login</sub>
		</td>
		<td>
				<img src="./images/Searching_meal.png" alt="Searching a meal" width="480" height="300" />
			<br /><sub>Searching a meal</sub>
		</td>
	</tr>
	<tr>
		<td>
				<img src="./images/Similar_results.png" alt="Similar results" width="480" height="300" />
			<br /><sub>Similar results</sub>
		</td>
		<td>
				<img src="./images/search_history_light_mode.png" alt="Search history (light mode)" width="480" height="300" />
			<br /><sub>Search history (light mode)</sub>
		</td>
	</tr>
	<tr>
		<td>
				<img src="./images/search_history_dark_mode.png" alt="Search history (dark mode)" width="480" height="300" />
			<br /><sub>Search history (dark mode)</sub>
		</td>
		<td></td>
	</tr>
  
</table>

---

## Running Backend Tests

Inside the `backend` container or locally with dependencies installed:

```bash
pytest
```

Note: Remove the rate limiter dependencies before running tests.

---

## Decisions & Trade‑Offs

1. Rate Limiter in Tests: To simplify backend test execution, the rate limiter dependency may need to be removed temporarily.
2. Test Coverage: Only backend tests were added. For the Integration test, I couldn't use Playwright as it was not supported on Fedora OS, and I didn't want to delay my submission by using workarounds.
3. Auth Guard: Client‑side `useAuthGuard` was used. A server‑side middleware would be preferable for stronger enforcement; not added as it was not mentioned in doc so wasnt sure.
4. JWTs are created without an external auth service, and the database connection uses SQLAlchemy. Using a managed auth service like Supabase, workos, clerk e.t.c with `supabase-js` library for DB management would make it possible to enable Postgres Row Level Security (RLS) in production. I chose a self‑managed approach to keep the stack simple and easy to run locally and switch with any other offered postgres service .

---

## Hosted Deployments

| Component | Host    | URL                                                                    |
| --------- | ------- | ---------------------------------------------------------------------- |
| Frontend  | Vercel  | https://meal-calorie-thomas-frontend.vercel.app                        |
| Backend   | Railway | https://meal-calorie-thomas-devasia-production-backend.up.railway.app/ |

---

## Quick Reference

| Action        | Command                       |
| ------------- | ----------------------------- |
| Start stack   | `docker compose up`           |
| Stop stack    | `docker compose down`         |
| Backend tests | `pytest` (inside backend env) |

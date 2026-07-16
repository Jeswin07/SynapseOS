# SynapseOS Frontend

Enterprise Decision Intelligence Platform — frontend for the existing FastAPI backend.

Built with React 19, Vite, TypeScript, Tailwind CSS, shadcn/ui, React Router, TanStack Query, Zustand, Axios,
Recharts, Framer Motion, React Hook Form, Zod, and Lucide React — exactly the stack requested, no extras.

## Getting started

```bash
npm install
cp .env.example .env   # set VITE_API_BASE_URL to your backend, e.g. http://localhost:8000
npm run dev
```

The app expects the FastAPI backend from `src__2_.zip` to be running and reachable at `VITE_API_BASE_URL`.

## Architecture

```
UI (features/*)
  ↓
Hooks (hooks/*)            — TanStack Query wraps every server call
  ↓
Services (services/*)      — one file per backend module, thin wrappers around Axios
  ↓
Axios Client (services/apiClient.ts)
  ↓
Backend (FastAPI)
```

- **Server state** lives in TanStack Query — never duplicated into Zustand.
- **UI state** (sidebar collapse, theme, active conversation, streaming toggle, toasts) lives in Zustand,
  persisted where it makes sense (`auth.store`, `theme.store`).
- **Assistant conversations** are stored in `assistant.store` (Zustand) rather than TanStack Query because the
  backend has no conversation-persistence endpoints — this is local session state, not cached server data.

## Backend contract notes (read directly from the provided FastAPI source)

The backend was inspected module-by-module; no endpoints, request bodies, or response shapes were invented.
A few gaps exist between the specification's ambitions and what the backend currently exposes — each is
marked with a `TODO: backend` comment at the call site and surfaced to the user via an inline note in the UI
rather than being silently faked:

| Area | Gap | Frontend behavior |
|---|---|---|
| Auth | `RefreshTokenRequest`/`LogoutRequest` schemas exist but `/auth/refresh` and `/auth/logout` are not wired to a route | Session ends client-side only; a 401 clears the local session |
| Auth | No `/auth/me` | Profile info comes from the login response + stored locally |
| Knowledge | No `GET` list/history of ingested documents | "Document library" shows only documents ingested in the current browser session |
| Forecast | No `GET` list of trained forecasts | A forecast must be trained (or its id known) in the current session before predicting |
| Dashboard | No dedicated summary endpoint | Dashboard composes metrics from `/datasets`, `/predictions/history`, and `/risks/analyze` |
| Scenario Planner | No dedicated `/scenarios` endpoint | Routed through `/assistant/chat` with `metadata.intent = "scenario_planning"`, clearly labeled in the UI |
| Users | No update/deactivate endpoints | Users page is read + create only |
| Tenants | No `GET` for the current tenant | Workspace settings tab explains this is not yet available |

## Scripts

- `npm run dev` — start Vite dev server
- `npm run build` — type-check and build for production
- `npm run lint` — run ESLint

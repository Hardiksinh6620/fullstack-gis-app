# Full-Stack GIS App

FastAPI + PostGIS backend serving spatial queries to a MapLibre frontend.

## Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend
Open `frontend/index.html` in a browser (or serve via `python -m http.server`).

## Endpoints
- `GET /health`
- `GET /cities` — all cities
- `GET /nearby?lat=&lon=&km=` — cities within radius

## Provenance

See [HISTORY.md](HISTORY.md) for collaboration and reconstruction details.

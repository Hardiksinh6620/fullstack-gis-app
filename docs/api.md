# API

- `GET /health` reports application availability.
- `GET /cities` returns known city coordinates.
- `GET /nearby?lat=&lon=&km=` performs a metre-based PostGIS search.

The radius must be positive and no greater than 1,000 km. Database errors are logged server-side and not exposed to clients.

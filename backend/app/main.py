"""FastAPI app exposing spatial endpoints."""
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import os
import logging

DB_URL = os.getenv("DATABASE_URL",
                   "postgresql+psycopg2://gis:gis@localhost:5432/gisdb")
engine = create_engine(DB_URL, pool_pre_ping=True)

app = FastAPI(title="Full-Stack GIS App")
origins=[v for v in os.getenv("CORS_ORIGINS","http://localhost:8000").split(",") if v]
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_methods=["GET"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cities")
def cities():
    sql = text("""
        SELECT name, ST_Y(geom) AS lat, ST_X(geom) AS lon
        FROM cities
    """)
    with engine.connect() as c:
        return [dict(r._mapping) for r in c.execute(sql)]

@app.get("/nearby")
def nearby(lat: float = Query(...), lon: float = Query(...),
           km: float = Query(500, gt=0, le=1000)):
    sql = text("""
        SELECT name,
               ST_Y(geom) AS lat, ST_X(geom) AS lon,
               ROUND((ST_Distance(geom::geography,
                     ST_SetSRID(ST_MakePoint(:lon,:lat),4326)::geography)
                     / 1000)::numeric,1) AS km
        FROM cities
        WHERE ST_DWithin(geom::geography,
              ST_SetSRID(ST_MakePoint(:lon,:lat),4326)::geography,
              :m)
        ORDER BY km
    """)
    try:
        with engine.connect() as c:
            return [dict(r._mapping) for r in
                    c.execute(sql, {"lat": lat, "lon": lon, "m": km * 1000})]
    except Exception:
        logging.exception("Nearby query failed")
        raise HTTPException(500, "Database query failed")

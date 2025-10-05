CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE IF NOT EXISTS cities(id serial primary key,name text unique not null,geom geometry(Point,4326) not null);
INSERT INTO cities(name,geom) VALUES ('Berlin',ST_SetSRID(ST_Point(13.405,52.520),4326)),('Hamburg',ST_SetSRID(ST_Point(9.993,53.551),4326)) ON CONFLICT(name) DO NOTHING;
CREATE INDEX IF NOT EXISTS cities_geom_geography_idx ON cities USING gist ((geom::geography));

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://demotiles.maplibre.org/style.json',
  center: [10.5, 51.0], zoom: 5
});

map.on('load', async () => {
  const r = await fetch('http://localhost:8000/cities');
  const cities = await r.json();
  cities.forEach(c => {
    new maplibregl.Marker()
      .setLngLat([c.lon, c.lat])
      .setPopup(new maplibregl.Popup().setText(c.name))
      .addTo(map);
  });
});

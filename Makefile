.PHONY: start test serve-map clean test-map-ci

start:
	./start.sh

test:
	pytest -q

serve-map:
	cd web/5d-map && python3 -m http.server 5500

clean:
	rm -rf node_modules package-lock.json
	rm -rf __pycache__ */__pycache__ || true

test-map-ci:
	pytest -k "metadata or world_map_data" -v --disable-warnings

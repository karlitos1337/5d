.PHONY: start test serve-map clean test-map-ci coverage

start:
	./start.sh

test:
	pytest -q

serve-map:
	cd web/5d-map && python3 -m http.server 5500

clean:
	rm -rf node_modules package-lock.json
	rm -rf __pycache__ */__pycache__ || true
	rm -rf tests/coverage_html .coverage

test-map-ci:
	pytest -k "metadata or world_map_data" -v --disable-warnings

coverage:
	@echo "Running pytest with coverage..."
	pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html:tests/coverage_html
	@echo ""
	@echo "✅ Coverage report generated:"
	@echo "   - HTML: tests/coverage_html/index.html"
	@echo "   - Terminal output above"
	@echo ""
	@echo "Open HTML report with:"
	@echo "   $$BROWSER tests/coverage_html/index.html"

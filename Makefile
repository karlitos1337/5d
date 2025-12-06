.PHONY: start test serve-map clean test-map-ci coverage sync-docs deploy-prep deploy-check

start:
	./start.sh

test:
	pytest -q

serve-map:
	cd web/5d-map && python3 -m http.server 5500

sync-docs:
	@echo "📦 Syncing web/5d-map/ → docs/5d-map/ for GitHub Pages..."
	cp -r web/5d-map/* docs/5d-map/
	@echo "✅ Sync complete. Ready for deployment."
	@echo "   Commit with: git add docs/5d-map/ && git commit -m 'Update map for GitHub Pages'"

deploy-check:
	@echo "🔍 Running pre-deployment validation..."
	@bash scripts/pre_deploy_check.sh

deploy-prep: sync-docs deploy-check
	@echo "🚀 Deployment preparation complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. git add docs/5d-map/"
	@echo "  2. git commit -m 'Update 5D Map for deployment'"
	@echo "  3. git push"
	@echo "  4. GitHub Actions will deploy automatically"
	@echo ""
	@echo "Monitor: https://github.com/karlitos1337/5d/actions"

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

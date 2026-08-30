sed -i 's/uses: actions\/setup-python@v3/uses: actions\/setup-python@v5/g' .github/workflows/ci.yml || true
sed -i 's/uses: actions\/setup-python@v3.0.0/uses: actions\/setup-python@v5/g' .github/workflows/ci.yml || true
sed -i 's/uses: actions\/setup-python@v4/uses: actions\/setup-python@v5/g' .github/workflows/ci.yml || true

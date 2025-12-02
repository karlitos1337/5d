Param(
    [switch]$Install,
    [switch]$Tests,
    [switch]$Dashboard,
    [switch]$Hook,
    [switch]$ValidateMd,
    [switch]$Fix
)

# UV Script: schnelle Umgebung + typische Aktionen
# Voraussetzungen: `uv` (https://github.com/astral-sh/uv) im PATH

function Ensure-Uv {
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Host "uv nicht gefunden. Installation siehe https://github.com/astral-sh/uv" -ForegroundColor Yellow
    }
}

Ensure-Uv

if ($Install) {
    # Installiere Abhängigkeiten mit uv; fallback auf pip
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        uv pip install -r requirements_extended.txt
    } else {
        pip install -r requirements_extended.txt
    }
    # Dev-Tools
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        uv pip install ruff black mypy
    } else {
        pip install ruff black mypy
    }
}

if ($Tests) {
    C:/Users/1/Documents/ki/resonance-formula-5d-intelligence/5d/.venv/Scripts/python.exe -m pytest tests -q
}

if ($Dashboard) {
    C:/Users/1/Documents/ki/resonance-formula-5d-intelligence/5d/.venv/Scripts/python.exe -m streamlit run 5d_dashboard.py
}

# Zusatzbefehle: Lint/Format/Types
if ($PSBoundParameters.ContainsKey('Tests') -and -not $Dashboard -and -not $Install) {
    Write-Host "Ruff Lint..."; ruff check .
    Write-Host "Black Check..."; black --check .
    Write-Host "Mypy..."; mypy src
}

if ($Hook) {
    # Pre-Commit installieren/aktualisieren
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        uv pip install pre-commit
    } else {
        pip install pre-commit
    }
    pre-commit install
    Write-Host "Pre-commit Hook installiert." -ForegroundColor Green
}

if ($ValidateMd) {
    # Manifest Markdown validieren; optional fixen
    $fixFlag = ""
    if ($Fix) { $fixFlag = "--fix" }
    C:/Users/1/Documents/ki/resonance-formula-5d-intelligence/5d/.venv/Scripts/python.exe scripts/validate_manifest_md.py manifest $fixFlag
}

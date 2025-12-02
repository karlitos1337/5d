Param(
    [switch]$Install,
    [switch]$Tests,
    [switch]$Dashboard
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
}

if ($Tests) {
    C:/Users/1/Documents/ki/resonance-formula-5d-intelligence/5d/.venv/Scripts/python.exe -m pytest tests -q
}

if ($Dashboard) {
    C:/Users/1/Documents/ki/resonance-formula-5d-intelligence/5d/.venv/Scripts/python.exe -m streamlit run 5d_dashboard.py
}

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_devcontainer_uses_single_python_source() -> None:
    devcontainer_path = ROOT / ".devcontainer" / "devcontainer.json"
    dockerfile_path = ROOT / ".devcontainer" / "Dockerfile"

    devcontainer = json.loads(devcontainer_path.read_text(encoding="utf-8"))
    dockerfile = dockerfile_path.read_text(encoding="utf-8")

    assert "mcr.microsoft.com/devcontainers/python:3.12-bullseye" in dockerfile
    assert "ghcr.io/devcontainers/features/python:1" not in devcontainer.get("features", {})

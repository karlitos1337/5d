#!/usr/bin/env python3
"""GitHub OAuth Integration - NUR für Zugangskontrolle.

KRITISCH: KEINE Speicherung personenbezogener Daten!
"""

import os
import secrets
from datetime import datetime, timedelta

import requests


class GitHubAuth:
    """GitHub OAuth nur zur Authentifizierung, nicht zur Identifikation."""

    def __init__(self):
        self.client_id = os.getenv("GITHUB_CLIENT_ID")
        self.client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/callback")

        if not self.client_id or not self.client_secret:
            raise ValueError("GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET must be set")

    def get_authorization_url(self, state: str | None = None) -> str:
        """Generiert OAuth Authorization URL."""
        if state is None:
            state = secrets.token_urlsafe(32)

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "",  # Keine Scopes - nur Login-Verifikation!
            "state": state,
        }

        url = "https://github.com/login/oauth/authorize"
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])

        return f"{url}?{query_string}"

    def exchange_code_for_token(self, code: str) -> str | None:
        """Tauscht Authorization Code gegen Access Token.

        WICHTIG: Token wird NUR zur Verifikation verwendet,
        dann sofort verworfen!
        """
        url = "https://github.com/login/oauth/access_token"

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }

        headers = {"Accept": "application/json"}

        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")

        return None

    def verify_user_exists(self, access_token: str) -> bool:
        """Verifiziert dass GitHub-User existiert.

        KEINE Speicherung von User-Daten!
        """
        url = "https://api.github.com/user"
        headers = {"Authorization": f"token {access_token}", "Accept": "application/json"}

        response = requests.get(url, headers=headers, timeout=10)

        return response.status_code == 200

    def generate_session_token(self) -> str:
        """Generiert anonyme Session-ID.

        Diese ID ist NICHT mit GitHub-Account verknüpft!
        """
        return secrets.token_urlsafe(32)

    def authenticate(self, code: str) -> dict | None:
        """Vollständiger OAuth-Flow.

        Returns:
            Session-Token (anonym) oder None bei Fehler
        """
        # 1. Code gegen Token tauschen
        access_token = self.exchange_code_for_token(code)
        if not access_token:
            return None

        # 2. Verifizieren dass User existiert
        if not self.verify_user_exists(access_token):
            return None

        # 3. Anonyme Session generieren
        session_token = self.generate_session_token()

        # 4. WICHTIG: Access Token sofort verwerfen!
        # KEINE Speicherung von:
        # - github_username
        # - github_email
        # - github_id
        # - access_token

        return {
            "session_token": session_token,
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            "created_at": datetime.now().isoformat(),
        }


class SessionManager:
    """Verwaltet anonyme Sessions."""

    def __init__(self):
        self.sessions = {}  # In Produktion: Redis oder Datenbank

    def create_session(self, session_token: str, expires_at: str) -> None:
        """Erstellt neue Session."""
        self.sessions[session_token] = {
            "expires_at": expires_at,
            "created_at": datetime.now().isoformat(),
            "survey_completed": False,
        }

    def validate_session(self, session_token: str) -> bool:
        """Prüft ob Session gültig ist."""
        if session_token not in self.sessions:
            return False

        session = self.sessions[session_token]
        expires_at = datetime.fromisoformat(session["expires_at"])

        if datetime.now() > expires_at:
            del self.sessions[session_token]
            return False

        return True

    def mark_survey_completed(self, session_token: str) -> None:
        """Markiert Survey als abgeschlossen."""
        if session_token in self.sessions:
            self.sessions[session_token]["survey_completed"] = True

    def destroy_session(self, session_token: str) -> None:
        """Löscht Session."""
        if session_token in self.sessions:
            del self.sessions[session_token]


if __name__ == "__main__":
    # Test (nur lokal!)
    print("GitHub OAuth Test")
    print("Setze Umgebungsvariablen:")
    print("export GITHUB_CLIENT_ID='your_client_id'")
    print("export GITHUB_CLIENT_SECRET='your_client_secret'")

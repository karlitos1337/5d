#!/usr/bin/env python3
"""GitHub OAuth Integration - NUR für Zugangskontrolle.

KRITISCH: KEINE Speicherung personenbezogener Daten!
"""

import os
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests


class GitHubAuth:
    """GitHub OAuth nur zur Authentifizierung, nicht zur Identifikation.

    Usage Pattern:
    1. Call `get_authorization_url()` to get the URL and a `state` token.
    2. Store the `state` token in the user's session (e.g., HTTP-only cookie).
    3. Redirect the user to the returned URL.
    4. In the callback handler, retrieve the `state` from the query params and the stored `state`.
    5. Call `authenticate(code, received_state, stored_state)` to complete the login.
    """

    def __init__(self):
        self.client_id = os.getenv("GITHUB_CLIENT_ID")
        self.client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/callback")

        if not self.client_id or not self.client_secret:
            raise ValueError("GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET must be set")

    def get_authorization_url(self, state: str | None = None) -> tuple[str, str]:
        """Generiert OAuth Authorization URL.

        Returns:
            Tuple[str, str]: (Authorization URL, state token)
            The caller MUST store the state token and pass it back to `authenticate`.
        """
        if state is None:
            state = secrets.token_urlsafe(32)

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "",  # Keine Scopes - nur Login-Verifikation!
            "state": state,
        }

        base_url = "https://github.com/login/oauth/authorize"
        query_string = urlencode(params)

        return f"{base_url}?{query_string}", state

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

        # Sentinel: Added timeout=10 to prevent hanging
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

        # Sentinel: Added timeout=10 to prevent hanging
        response = requests.get(url, headers=headers, timeout=10)

        return response.status_code == 200

    def generate_session_token(self) -> str:
        """Generiert anonyme Session-ID.

        Diese ID ist NICHT mit GitHub-Account verknüpft!
        """
        return secrets.token_urlsafe(32)

    def authenticate(self, code: str, received_state: str, expected_state: str) -> dict | None:
        """Vollständiger OAuth-Flow mit CSRF-Protection.

        Args:
            code: Authorization Code von GitHub
            received_state: State Parameter von GitHub Callback
            expected_state: Ursprünglich generierter State (aus Session)

        Returns:
            Session-Token (anonym) oder None bei Fehler
        """
        # 0. CSRF Check
        if not received_state or not expected_state:
            return None

        # Constant time comparison to prevent timing attacks
        if not secrets.compare_digest(received_state, expected_state):
            print("❌ CSRF Attack detected! State mismatch.")
            return None

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

    MAX_SESSIONS = 1000  # DoS Protection: Limit active sessions

    def __init__(self):
        self.sessions = {}  # In Produktion: Redis oder Datenbank

    def _cleanup_expired_sessions(self) -> None:
        """Entfernt abgelaufene Sessions."""
        now = datetime.now()
        expired_tokens = []
        for token, data in self.sessions.items():
            if now > datetime.fromisoformat(data["expires_at"]):
                expired_tokens.append(token)

        for token in expired_tokens:
            del self.sessions[token]

    def _evict_oldest_session(self) -> None:
        """Entfernt die älteste Session wenn Limit erreicht."""
        if not self.sessions:
            return

        # Sort by creation time
        oldest_token = min(
            self.sessions.keys(),
            key=lambda k: self.sessions[k]["created_at"]
        )
        del self.sessions[oldest_token]

    def create_session(self, session_token: str, expires_at: str) -> None:
        """Erstellt neue Session mit Limit-Prüfung."""
        # 1. Cleanup expired first
        self._cleanup_expired_sessions()

        # 2. Check limit
        if len(self.sessions) >= self.MAX_SESSIONS:
            self._evict_oldest_session()

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

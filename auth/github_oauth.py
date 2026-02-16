import os

import requests


class GitHubAuth:
    def __init__(self):
        self.client_id = os.environ.get("GITHUB_CLIENT_ID")
        self.client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
        self.redirect_uri = os.environ.get("GITHUB_REDIRECT_URI")
        self.auth_url = "https://github.com/login/oauth/authorize"
        self.token_url = "https://github.com/login/oauth/access_token"
        self.user_url = "https://api.github.com/user"

    def get_auth_url(self):
        return f"{self.auth_url}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=user"

    def get_access_token(self, code):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        headers = {"Accept": "application/json"}
        response = requests.post(self.token_url, data=payload, headers=headers)
        return response.json().get("access_token")

    def get_user_info(self, access_token):
        headers = {"Authorization": f"token {access_token}"}
        response = requests.get(self.user_url, headers=headers)
        return response.json()

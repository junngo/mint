import requests
from django.conf import settings 

class KoreaInvestAPI:
    def __init__(self):
        if settings.USE_SIMULATED_API:
            self.app_key = settings.SIM_APP_KEY
            self.app_secret = settings.SIM_APP_SECRET
            self.api_domain = settings.SIM_API_DOMAIN
        else:
            self.app_key = settings.LIVE_APP_KEY
            self.app_secret = settings.LIVE_APP_SECRET
            self.api_domain = settings.LIVE_API_DOMAIN

    def get_headers(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8'
        }

    def get_token(self):
        url = f"{self.api_domain}/oauth2/tokenP"
        headers = self.get_headers()
        body = {
            'grant_type': 'client_credentials',
            'appkey': self.app_key,
            'appsecret': self.app_secret
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to get token, status code: {response.status_code}"}

import requests
from django.conf import settings
from django.core.cache import cache

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

        self.token_cache_key = 'korea_invest_api_token'
        self.token_expiry_time = 1430 * 60  # 1430분(23시간 50분) * 60초

    def get_headers(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8'
        }

    def get_token(self):
        token = cache.get(self.token_cache_key)
        if token:
            return token

        response = self.request_token_from_api()

        if 'access_token' in response:
            token = response['access_token']
            cache.set(self.token_cache_key, token, timeout=self.token_expiry_time)
            return token
        else:
            return None

    def request_token_from_api(self):
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
            print(f"Failed to retrieve access token.: {response.json()}")
            return {"error": f"Failed to get token, status code: {response.status_code}"}

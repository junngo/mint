from django.core.management.base import BaseCommand
from stocks.services import KoreaInvestAPI

class Command(BaseCommand):
    help = 'Get access token from Korea Investment API'

    def handle(self, *args, **kwargs):
        api = KoreaInvestAPI()
        token_response = api.get_token()

        if 'error' in token_response:
            self.stdout.write(self.style.ERROR(token_response['error']))
        else:
            access_token = token_response.get('access_token', 'No token found')
            self.stdout.write(self.style.SUCCESS(f"Access Token: {access_token}"))

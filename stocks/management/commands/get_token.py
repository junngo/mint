from django.core.management.base import BaseCommand
from stocks.services import KoreaInvestAPI

class Command(BaseCommand):
    help = 'Get access token from Korea Investment API'

    def handle(self, *args, **kwargs):
        api = KoreaInvestAPI()
        token = api.get_token()

        if token is None:
            self.stdout.write(self.style.ERROR("Failed to retrieve access token."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Access Token: {token}"))

from datetime import datetime, date, timedelta
from django.core.management.base import BaseCommand
from stocks.models import Stock, DailyStockData
from stocks.services import KoreaInvestAPI

class Command(BaseCommand):
    help = "Fetch daily stock data for a specific stock or all stocks within a date range"

    def add_arguments(self, parser):
        parser.add_argument(
            '--ticker',
            type=str,
            help="Specify the stock ticker to fetch data for (e.g., 005930). Leave blank to fetch all stocks."
        )
        parser.add_argument(
            '--start_date',
            type=str,
            help="Specify the start date (YYYYMMDD). Defaults to today.",
            default=date.today().strftime('%Y%m%d')
        )
        parser.add_argument(
            '--end_date',
            type=str,
            help="Specify the end date (YYYYMMDD). Defaults to today.",
            default=date.today().strftime('%Y%m%d')
        )
        parser.add_argument(
            '--period_code',
            type=str,
            help="Period code (D, W, M, Y). Default D",
            default="D"
        )

    def handle(self, *args, **options):
        api = KoreaInvestAPI()
        ticker = options.get('ticker')
        start_date = datetime.strptime(options.get('start_date'), '%Y%m%d').date()
        end_date = datetime.strptime(options.get('end_date'), '%Y%m%d').date()
        period_code = options.get('period_code')

        if ticker:
            self.fetch_data_for_ticker(api, ticker, start_date, end_date, period_code)
        else:
            # Fetch data for all stocks in the database
            stocks = Stock.objects.filter(group_code="ST")
            for stock in stocks:
                self.fetch_data_for_ticker(api, stock.ticker, start_date, end_date, period_code)

    def fetch_data_for_ticker(self, api, ticker, start_date, end_date, period_code):
        current_date = start_date
        while current_date <= end_date:
            start_date_str = current_date.strftime('%Y%m%d')
            end_date_str = current_date.strftime('%Y%m%d')

            self.stdout.write(f"Fetching data for {ticker} on {start_date_str} - {end_date_str}...")
            data = api.fetch_daily_stock_data(ticker, start_date_str, end_date_str, period_code)

            if "error" in data:
                self.stdout.write(self.style.ERROR(f"Failed to fetch data for {ticker} on {current_date}: {data['error']}"))
            else:
                self.save_daily_data(ticker, data)

            current_date += timedelta(days=1)

    def save_daily_data(self, ticker, data):
        try:
            stock = Stock.objects.get(ticker=ticker)

            for record in data.get('output2', []):
                business_date = datetime.strptime(record['stck_bsop_date'], '%Y%m%d').date()
                close_price = float(record['stck_clpr'])
                open_price = float(record['stck_oprc'])
                high_price = float(record['stck_hgpr'])
                low_price = float(record['stck_lwpr'])
                volume = int(record['acml_vol'])

                DailyStockData.objects.update_or_create(
                    stock=stock,
                    date=business_date,
                    defaults={
                        'open_price': open_price,
                        'high_price': high_price,
                        'low_price': low_price,
                        'close_price': close_price,
                        'volume': volume,
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Successfully saved data for {ticker}"))
        except Stock.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Stock with ticker {ticker} does not exist in the database."))
        except:
            self.stdout.write(self.style.ERROR(f"Error with ticker {ticker}, data: {data}"))
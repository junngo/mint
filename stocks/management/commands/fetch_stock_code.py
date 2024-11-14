import os
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from stocks.constants import MarketType
from stocks.models import Stock
from stocks.services import KoreaInvestAPI


class Command(BaseCommand):
    help = 'Fetch the data for KOSPI and KOSDAQ listings'

    def handle(self, *args, **kwargs):
        api = KoreaInvestAPI()
        base_dir = os.getcwd()

        # 코스피 코스닥 종목 데이터를 각각 다운로드 및 처리
        for market in [MarketType.KOSPI, MarketType.KOSDAQ]:
            # 종목 파일 다운로드
            self.stdout.write(f"Downloading {market} data...")
            api.download_and_extract_stock_data(base_dir, market)
            
            # 데이터프레임으로 변환
            self.stdout.write(f"Processing {market} data to DataFrame...")
            df = api.get_stock_data_dataframe(base_dir, market)

            for _, row in df.iterrows():
                ticker = row['단축코드']
                isin_code = row['표준코드']
                name = row['한글명'] if market == MarketType.KOSPI else row['한글종목명']
                group_code = row['그룹코드'] if market == MarketType.KOSPI else row['증권그룹구분코드']

                # 상장일자 필드
                listing_date_str = row.get('상장일자') if market == MarketType.KOSPI else row.get('주식 상장 일자')
                listing_date = datetime.strptime(str(listing_date_str), "%Y%m%d").date() if listing_date_str else None

                Stock.objects.update_or_create(
                    ticker=ticker,
                    defaults={
                        'name': name,
                        'market_type': market.value,
                        'isin_code': isin_code,
                        'group_code': group_code,
                        'listing_date': listing_date,
                    }
                )

            self.stdout.write(f"{market} data processed and saved to the database.")

        self.stdout.write("Data import completed successfully.")

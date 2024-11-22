from django.db import models
from .constants import MarketType


class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)   # 단축코드 (e.x, 005930)
    name = models.CharField(max_length=100)                 # 종목명 (e.x, 삼성전자)
    market_type = models.CharField(max_length=10, choices=MarketType.choices())     # 시장 구분 (e.x, KOSPI)
    isin_code = models.CharField(max_length=20, blank=True, null=True)              # ISIN 코드 (e.x, KR7005930003)
    group_code = models.CharField(max_length=10, blank=True, null=True)             # 그룹코드(e.x, ST:주권, MF:증권투자회사)
    listing_date = models.DateField(blank=True, null=True)  # 상장일자 (e.x, 1975-06-11)
    created_at = models.DateTimeField(auto_now_add=True)    # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)        # 수정 날짜

    class Meta:
        db_table = 'stock'

    def __str__(self):
        return f"{self.name} ({self.ticker})"


class DailyStockData(models.Model):
    """
    일자별 주식 데이터 모델
    """
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='daily_data')
    date = models.DateField()                                          # 일자
    open_price = models.DecimalField(max_digits=10, decimal_places=2)  # 시가
    high_price = models.DecimalField(max_digits=10, decimal_places=2)  # 고가
    low_price = models.DecimalField(max_digits=10, decimal_places=2)   # 저가
    close_price = models.DecimalField(max_digits=10, decimal_places=2) # 종가
    volume = models.BigIntegerField()                                  # 거래량
    created_at = models.DateTimeField(auto_now_add=True)               # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)                   # 수정 날짜

    class Meta:
        db_table = 'daily_stock_data'
        unique_together = ('stock', 'date')  # 같은 종목, 같은 날짜의 데이터 중복 방지

    def __str__(self):
        return f"{self.stock.name} ({self.date}) - Close: {self.close_price}"

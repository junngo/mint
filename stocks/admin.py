from django.contrib import admin
from .models import Stock, DailyStockData

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'market_type', 'isin_code', 'group_code', 'listing_date', 'created_at', 'updated_at')
    list_display_links = ('ticker', 'name')
    list_filter = ('market_type', 'group_code')
    search_fields = ('ticker', 'name', 'isin_code')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('ticker', 'name', 'market_type', 'isin_code', 'listing_date')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(DailyStockData)
class DailyStockDataAdmin(admin.ModelAdmin):
    """
    일자별 주식 데이터 관리 페이지 설정
    """
    list_display = (
        'stock',           # 종목
        'date',            # 날짜
        'open_price',      # 시가
        'high_price',      # 고가
        'low_price',       # 저가
        'close_price',     # 종가
        'volume',          # 거래량
        'created_at',      # 생성일
        'updated_at'       # 수정일
    )
    search_fields = ('stock__name', 'stock__ticker')    # 검색 필드
    ordering = ('-date',)                               # 기본 정렬 순서 (날짜 내림차순)
    date_hierarchy = 'date'                             # 날짜 필터 계층

from django.contrib import admin
from .models import Stock

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

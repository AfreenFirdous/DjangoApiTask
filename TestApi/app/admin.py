from django.contrib import admin
from app.models import CryptoPrice

@admin.register(CryptoPrice)
class CryptoPriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'exchange_rate', 'from_symbol', 'to_symbol', 'bid_price', 'ask_price', 'created_on']

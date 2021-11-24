from django.db import models

class CryptoPrice(models.Model):
    exchange_rate = models.FloatField(blank=False)
    from_symbol = models.CharField(max_length=3, blank=False, default='BTC')
    to_symbol = models.CharField(max_length=3, blank=False, default='USD')
    bid_price = models.FloatField(blank=False)
    ask_price = models.FloatField(blank=False)
    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
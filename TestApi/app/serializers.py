from django.db.models.base import Model
from rest_framework import serializers
from app.models import CryptoPrice

class CryptoPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoPrice
        fields = ['id', 'exchange_rate', 'from_symbol', 'to_symbol', 'bid_price', 'ask_price', 'created_on']
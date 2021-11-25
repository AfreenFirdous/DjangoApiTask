import requests
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from app.serializers import CryptoPriceSerializer
from app.models import CryptoPrice
from django.utils import timezone
import os
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

def pull_crypto_data():
    API_KEY = os.getenv("API_KEY")
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&interval=60min&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    return data

@api_view(['GET']) 
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def exchange_rates(request):
    if request.method == 'GET':
        crypto_data = pull_crypto_data()
        data = crypto_data['Realtime Currency Exchange Rate']
        obj= CryptoPrice.objects.filter().order_by('-created_on').first()
        if obj is None: # if table is empty, insert first record
            new_obj = CryptoPrice.objects.create(exchange_rate=data['5. Exchange Rate'],
                        from_symbol=data['1. From_Currency Code'],
                        to_symbol=data['3. To_Currency Code'],
                        bid_price=data['8. Bid Price'],
                        ask_price=data['9. Ask Price'])
            data = CryptoPriceSerializer(instance=new_obj).data
            return Response({'Exchange Rate':data})
        one_hr_later = obj.created_on + timezone.timedelta(hours=1)
        if timezone.now() >= one_hr_later:
            new_obj = CryptoPrice.objects.create(exchange_rate=data['5. Exchange Rate'],
                        from_symbol=data['1. From_Currency Code'],
                        to_symbol=data['3. To_Currency Code'],
                        bid_price=data['8. Bid Price'],
                        ask_price=data['9. Ask Price'])
            data = CryptoPriceSerializer(instance=new_obj).data
            return Response({'Exchange Rate':data})
        else:
            data = CryptoPriceSerializer(instance=obj).data
            return Response({'Exchange Rate':data})

@api_view(['GET', 'POST'])
def crypto_currencies(request):
    if request.method == 'GET':
        obj= CryptoPrice.objects.filter().order_by('-created_on').first()
        data = CryptoPriceSerializer(instance=obj).data
        return Response({'Exchange Rate':data})
    if request.method == 'POST':
        crypto_data = pull_crypto_data()
        data = crypto_data['Realtime Currency Exchange Rate']
        result = dict()
        result = {
            "exchange_rate": data['5. Exchange Rate'],
            'from_symbol': data['1. From_Currency Code'],
            'to_symbol': data['3. To_Currency Code'],
            "bid_price": data['8. Bid Price'],
            "ask_price": data['9. Ask Price'],
            "created_on": data['6. Last Refreshed']
        }
        return Response({'Exchange Rate':result})


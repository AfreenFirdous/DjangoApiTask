from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/exchange_rates', views.exchange_rates),
    path('api/v1/quotes', views.crypto_currencies),
]

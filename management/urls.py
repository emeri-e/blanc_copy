# urls.py
from django.urls import path
from .views import CoinPriceView

urlpatterns = [
    path('coin-price/<str:coin_name>/', CoinPriceView.as_view(), name='coin-price'),
]

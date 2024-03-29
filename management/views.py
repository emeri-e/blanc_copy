from django.shortcuts import render
import requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


from management.models import BitgoWallet
from management.serializers import BitgoWalletSerializer

# Create your views here.

class BitgoWalletViewSet(viewsets.ModelViewSet):
    queryset = BitgoWallet.objects.all()
    serializer_class = BitgoWalletSerializer
    # permission_classes = [IsOwnerOrAdmin]


class CoinPriceView(APIView):
    def get(self, request, coin_name):
        response = requests.get(f'https://api.example.com/coin-price/{coin_name}/naira')
        
        if response.status_code == 200:
            price_data = response.json()
            return Response(price_data)
        else:
            return Response({'error': 'Failed to fetch coin price'}, status=response.status_code)


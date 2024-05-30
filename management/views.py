from django.shortcuts import render
import requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status
from bitgo.bitgo_base import BitGo


from management.models import BitgoWallet
from management.serializers import BitgoWalletSerializer

# Create your views here.

class BitgoWalletViewSet(viewsets.ModelViewSet):
    queryset = BitgoWallet.objects.all()
    serializer_class = BitgoWalletSerializer
    # permission_classes = [IsOwnerOrAdmin]

    def create(self, request, *args, **kwargs):
        _type = request.data.get('_type')
        
        if BitgoWallet.objects.filter(_type=_type).exists():
            raise ValidationError({'_type': 'Wallet of this type already exists.'})

        bitgo = Bitgo()
        wallet_data = bitgo.generate_wallet_exppress(_type)

        serializer = self.get_serializer(data={
            'wallet_id': wallet_data['wallet_id'],
            '_type': _type
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class CoinPriceView(APIView):
    def get(self, request, coin_name):
        response = requests.get(f'https://api.example.com/coin-price/{coin_name}/naira')
        
        if response.status_code == 200:
            price_data = response.json()
            return Response(price_data)
        else:
            return Response({'error': 'Failed to fetch coin price'}, status=response.status_code)


from rest_framework import serializers

from management.models import BitgoWallet

class BitgoWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitgoWallet
        fields = ['id', '_type']
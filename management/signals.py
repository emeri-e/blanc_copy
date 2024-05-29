import json
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import BitgoWallet

# @receiver(post_migrate)
# def create_bitgo_wallet_types(sender, **kwargs):
#     if kwargs.get('created'):
#         print('here')
#         data = json.load('bitgo_wallets.json')
#         BitgoWallet.from_dict(data)

#     print('or here')
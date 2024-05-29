from django.db import models
from django.conf import settings

from dashboard.profile_model import Profile
from .bitgo_base import BitGo

from management.models import BitgoWallet


class Address(models.Model):

    id = models.CharField(max_length=50, primary_key=True, editable=False)
    address = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='addresses')
    wallet = models.CharField(max_length=50)
    bitgo_wallet = models.ForeignKey(BitgoWallet, on_delete = models.CASCADE, related_name = 'addresses')
    _is_active = models.BooleanField(default = False)

    def __str__(self):
        return self.profile.user.username + self._type
    
    @property
    def _type(self):
        return self.bitgo_wallet._type
    
    @property
    def bitgo_balance(self):
        pass

    @classmethod
    def initialise_addresses(cls, profile):
        bitgo = BitGo()
        
        wallets = BitgoWallet.objects.all()
        for wallet in wallets:
            # all wallet classes should be imported instead
            data = bitgo.create_address(wallet._type, wallet.wallet_id)
            data['profile'] = profile
            data['bitgo_wallet'] = wallet

            data['_type'] = wallet._type
            if data['_type'] != BitgoWallet.Type.ETH:
                data['_is_active'] = True

            
            try:
                Address.objects.get_or_create(wallet=wallet.id, defaults= data)

            except:
                print('failed to create address')



class Transaction(models.Model):
    pass
#     transaction_id = models.CharField(max_length=100, unique=True)
#     amount = models.DecimalField(max_digits=1000, decimal_places=2)
#     is_withdrawn = models.BooleanField(default=False)  # True if withdrawn, False otherwise
#     address = models.ForeignKey(Address, on_delete= models.CASCADE, related_name='transactions')
#     def __str__(self):
#         return self.transaction_id
    
#     @classmethod
#     def update_transactions(cls, profile):
#         addresses = profile.addreses
#         if addresses < BitgoWallet.objects.count():
#             Address.initialise_addresses(profile)
#             return 
        
#         for address in addresses:
#             bitgo = BitGo()
#             # to be completed





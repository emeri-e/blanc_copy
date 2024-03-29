from django.conf import settings
from bitgo.models import Address
from .bitgo_base import BitGo


def create_addresses(profile):
    Address.initialise_addresses(profile)
    

def fetch_deposits(profile):
    bitgo = BitGo()
    addresses = profile.addresses

    deposits = []
    for address in addresses:
        response = bitgo.get_transactions(address._type, wallet_id=address.wallet, address=address)
       
        
        for transfer in response['transfers']:
            try:
                data = {}
                data['transaction_id'] = transfer['id']
                data['amount'] = int(transfer['baseValueWithoutFees']) - int(transfer['feeString']) - int(transfer['payGoFee'])
                data['address'] = address
                data['comment'] = transfer.get('comment')

                deposits.append(data)
            except: continue
    return deposits    

def update_comment(txn):
    bitgo = BitGo()
    bitgo.update_comment(txn.address._type,txn.address.wallet,txn.transaction_id)
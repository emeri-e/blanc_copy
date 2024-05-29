from rest_framework import viewsets
from core_app_root.user_services.bankmanagement.serializers.bankmanagementserializer import BankManagementSerializer,UserBankDetailsSerializer
from rest_framework import permissions
from core_app_root.user_services.bankmanagement.models import BankAdminManager
import requests
from requests.exceptions import JSONDecodeError
from rest_framework.response import Response
from rest_framework import status
from core_app_root.user_services.bankmanagement.models import BankAdminManager,UserBankAccountDetails

# Define your secret key and base URL

import requests
class BankManagementViewset(viewsets.ModelViewSet):
    http_method_names=['get']
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=BankManagementSerializer
    def list(self,request):
        all_banks = BankAdminManager.objects.all()

# Extract bank names from the queryset
        bank_names = [bank.bank_name for bank in all_banks]
        return Response({"data":bank_names},status=status.HTTP_200_OK) 
    
    

class UserBankDetailsViewset(viewsets.ModelViewSet):
    serializer_class=UserBankDetailsSerializer
    permission_classes=[permissions.IsAuthenticated]
    http_method_names=['get','post']
    
    def create(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            print("is valid")
            import requests
            from requests.exceptions import JSONDecodeError

            # Define your secret key and base URL
            secret_key = 'sk_live_7f39f77453508b7b3b71d48e4dc5fdbbdfe9d2e7'
            base_url = 'https://api.paystack.co'

            import requests

            # Define your secret key and base URL
            base_url = 'https://api.paystack.co'

            # Define endpoint and parameters
            endpoint = '/bank/resolve'
            params = {
                'account_number': str(serializer.validated_data['account_number']),
                'bank_code': str(serializer.validated_data['bank_code'])
            }

            # Define headers
            headers = {
                'Authorization': f'Bearer {secret_key}'
            }

            # Make GET request
            response = requests.get(f'{base_url}{endpoint}', params=params, headers=headers)

            data=response.json()
            account_name=data['data']['account_name']
            UserBankAccountDetails.objects.create(account_name=str(account_name),account_number=str(serializer.validated_data['account_number']),bank_name=str(serializer.validated_data['bank_name']),user=str(request.user))
            return Response({"data":response.json()},status=status.HTTP_200_OK) 
    def get_queryset(self):
        return super().get_queryset()
    
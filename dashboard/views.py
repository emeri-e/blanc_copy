from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView

from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from dashboard.base_viewsets import RUViewSet, RViewSet, RLViewSet
from dashboard.models import Wallet, Bank_Account, Deposit, Withdrawal, Notification
from dashboard.profile_model import Profile
from .serializers import NotificationSerializer, ProfileSerializer, WalletSerializer, BankAccountSerializer, DepositSerializer, WithdrawalSerializer
from .permissions import IsOwnerOrAdmin, IsOwnerOrAdminCanDelete



class ProfileViewSet(RUViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admin users can view all profiles
            return Profile.objects.all()
        else:
            # Non-admin users can only view their own profile
            return Profile.objects.filter(user=user)
        


class WalletViewSet(RViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    # permission_classes = [IsOwnerOrAdmin]


class BankAccountViewSet(viewsets.ModelViewSet): 
    queryset = Bank_Account.objects.all()
    serializer_class = BankAccountSerializer
    # permission_classes = [IsOwnerOrAdminCanDelete]


class NotificationViewSet(RLViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    


class DepositViewSet(RLViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

class WithdrawalViewSet(RLViewSet):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer



class ConfirmDepositView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            if user.profile:
                Deposit.update_deposits(user.profile)
            else:
                Profile.objects.get_or_create(user=user)

class WithdrawView(APIView):
    def post(self, request):
        user = request.user
        amount = request.POST['amount']
        acc_no = request.POST['account_number']

        if user.is_authenticated:
            if user.profile:
                bank_acc = get_object_or_404(Bank_Account, acc_no=acc_no)
                withdrawal = Withdrawal.objects.create(user=user, amount=amount, bank_account=bank_acc)
                withdrawal.confirm()
            else:
                Profile.objects.get_or_create(user=user)
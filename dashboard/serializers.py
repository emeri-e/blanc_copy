from rest_framework import serializers

from dashboard.profile_model import Profile
from .models import Bank_Account, Deposit, Wallet, Notification, Withdrawal

class ProfileSerializer(serializers.ModelSerializer):
    profile_pix = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'phone', 'dark_mode', 'use_biometrics', 'profile_pix']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'profile', 'available', 'usdt_balance']

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank_Account
        fields = ['id', 'name', 'acc_no', 'profile', 'bank', 'is_default', 'bank_name']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'subject', 'message', 'date', 'user']

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['id', 'status', 'timestamp', 'transaction_id', 'amount', 'is_withdrawn', 'address']

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['id', 'profile', 'amount', 'status', 'timestamp', 'bank_account']



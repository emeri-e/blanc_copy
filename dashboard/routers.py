from rest_framework import routers
from .views import DepositViewSet, ProfileViewSet, NotificationViewSet, WithdrawalViewSet, WalletViewSet, BankAccountViewSet

app_name='dashboard'

router = routers.SimpleRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'deposits', DepositViewSet, basename='deposits')
router.register(r'withdrawals', WithdrawalViewSet, basename='withdrawals')
router.register(r'wallet', WalletViewSet, basename='wallet')
router.register(r'banks', BankAccountViewSet, basename='bank')



urlpatterns=[
    *router.urls
]
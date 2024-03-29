# urls.py
from django.urls import path
from .views import ConfirmDepositView, WithdrawView

urlpatterns = [
    path('confirm-deposit/', ConfirmDepositView.as_view(), name='confirm-deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
]

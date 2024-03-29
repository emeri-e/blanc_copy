from rest_framework import routers
from .views import BitgoWalletViewSet

router = routers.SimpleRouter()
router.register(r'bitgo_wallets', BitgoWalletViewSet, basename='bitgo_wallets')

urlpatterns=[
    *router.urls
]
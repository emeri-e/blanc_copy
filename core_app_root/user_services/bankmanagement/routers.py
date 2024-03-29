from rest_framework import routers
from core_app_root.user_services.bankmanagement.viewsets.bankmanagementviewset import BankManagementViewset,UserBankDetailsViewset
router=routers.SimpleRouter()
router.register(r'bankmanagement',BankManagementViewset,basename='bankmanagement')
router.register(r'userbankdetails',UserBankDetailsViewset,basename='userbankdetails')


urlpatterns=[
    *router.urls
]

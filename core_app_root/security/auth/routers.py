from rest_framework import routers
from core_app_root.security.auth.viewsets.register import RegisterViewSet
from core_app_root.security.auth.viewsets.login import LoginViewSet
router=routers.SimpleRouter()
router.register(r'register',RegisterViewSet,basename='register')
router.register(r'login',LoginViewSet,basename='login')


urlpatterns=[
    *router.urls
]

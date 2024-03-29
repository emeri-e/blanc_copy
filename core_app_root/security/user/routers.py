from rest_framework import routers
from core_app_root.security.user.viewsets.user import UserViewset

router=routers.SimpleRouter()
router.register(r'user',UserViewset,basename='user')


urlpatterns=[
    *router.urls
]

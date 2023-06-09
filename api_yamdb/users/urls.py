from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, create_token, create_user

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/auth/', include([
        path('token/', create_token),
        path('signup/', create_user),
    ])),
    path('v1/', include(router.urls)),
]

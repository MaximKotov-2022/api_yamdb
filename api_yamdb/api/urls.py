from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

from .views import UserViewSet, create_token, create_user

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles'),
router.register('categories', CategoryViewSet, basename='categories'),
router.register('genres', GenreViewSet, basename='genres'),


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include([
        path('token/', create_token),
        path('signup/', create_user)
    ]))
]

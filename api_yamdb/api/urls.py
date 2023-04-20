from django.urls import include, path
from rest_framework import routers
from api.views import (TitleViewSet, CategoryViewSet, GenreViewSet,)

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, basename='titles'),
router.register('categories', CategoryViewSet, basename='categories'),
router.register('genres', GenreViewSet, basename='genres'),

urlpatterns = [
    path('v1/', include(router.urls)),
]

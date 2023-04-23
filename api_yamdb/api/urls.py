from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitlesViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('titles', TitlesViewSet, basename='titles'),
router.register('categories', CategoryViewSet, basename='categories'),
router.register('genres', GenreViewSet, basename='genres'),
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')


urlpatterns = [
    path('v1/', include(router.urls)),

]

from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class ListCreateDeleteMixin(GenericViewSet, CreateModelMixin,
                            ListModelMixin, DestroyModelMixin):
    pass


class TitleReviewCommentViewSet(viewsets.ModelViewSet):
    pass

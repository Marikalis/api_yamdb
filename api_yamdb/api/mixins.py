from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnly


class CreateListDeleteViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass

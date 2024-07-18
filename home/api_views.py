from rest_framework import routers, serializers, viewsets
from .serializers import *


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = ProductSerializer


import django_filters.rest_framework
from .serializers import *
from rest_framework import generics
from rest_framework import filters


class ProductListView(generics.ListAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['category', 'stock', 'label', 'brand']
    search_fields = ['name','description','specification']
    ordering_fields = ['id', 'name', 'price']


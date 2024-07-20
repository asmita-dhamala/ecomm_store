from django.urls import path, include
from rest_framework import routers
from .api_views import *


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path("product_api/", ProductListView.as_view(), name="product_api"),
    path("product_crud/<int:pk>", ProductDetail.as_view(), name="product_crud"),
    
]
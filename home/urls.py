from .views import *
from django.urls import path,include

urlpatterns = [
    path("",HomeView.as_view(),name = "home"),
    path("product/<slug>", ProductView.as_view(), name="product"),
    path("category/<slug>", CategoryView.as_view(), name="category"),
    path("brand/<slug>", BrandView.as_view(), name="brand"),
    path("search", SearchView.as_view(), name="search"),
    path("signup", signup, name="signup"),
    path("add_to_cart/<slug>", add_to_cart, name="add_to_cart"),
    path("reduce_cart/<slug>", reduce_cart, name="reduce_cart"),
    path("delete_cart/<slug>", delete_cart, name="delete_cart"),
    path("my_cart",CartView.as_view(),name = "my_cart"),
    path("product_review/<slug>", product_review, name="product_review"),

]
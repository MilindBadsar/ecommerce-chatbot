from django.urls import path
from .views import ProductListView, ProductDetailView, ProductSearchAPIView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/search/', ProductSearchAPIView.as_view(), name='product-search'),
]
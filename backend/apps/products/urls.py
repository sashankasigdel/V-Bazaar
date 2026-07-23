from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/products/', views.BusinessProductListView.as_view(), name='business_products'),
    path('<slug:slug>/products/manage/', views.MyProductListView.as_view(), name='my_products'),
    path('products/<int:pk>/', views.MyProductDetailView.as_view(), name='product_detail'),
]

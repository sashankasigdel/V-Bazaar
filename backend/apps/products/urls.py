from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/products/', views.BusinessProductListView.as_view(), name='business_products'),
    path('<slug:slug>/products/manage/', views.MyProductListView.as_view(), name='my_products'),
    path('products/<int:pk>/', views.MyProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/categories/', views.MyProductCategoryListView.as_view(), name='my_product_categories'),
    path('categories/<int:pk>/', views.MyProductCategoryDetailView.as_view(), name='product_category_detail'),
]

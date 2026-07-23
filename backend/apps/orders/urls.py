from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerOrderListView.as_view(), name='customer_orders'),
    path('<int:pk>/', views.CustomerOrderDetailView.as_view(), name='order_detail'),
    path('business/<slug:slug>/', views.BusinessOrderListView.as_view(), name='business_orders'),
    path('business/<slug:slug>/<int:pk>/', views.BusinessOrderDetailView.as_view(), name='business_order_detail'),
]

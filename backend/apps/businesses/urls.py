from django.urls import path
from . import views

urlpatterns = [
    path('', views.BusinessListView.as_view(), name='business_list'),
    path('featured/', views.featured_businesses, name='featured'),
    path('nearby/', views.nearby_businesses, name='nearby'),
    path('categories/', views.BusinessCategoryListView.as_view(), name='categories'),
    path('my/', views.MyBusinessListView.as_view(), name='my_businesses'),
    path('my/<slug:slug>/', views.MyBusinessDetailView.as_view(), name='my_business_detail'),
    path('my/<slug:slug>/hours/', views.BusinessHoursView.as_view(), name='business_hours'),
    path('my/<slug:slug>/analytics/', views.business_analytics, name='analytics'),
    path('<slug:slug>/', views.BusinessDetailView.as_view(), name='business_detail'),
]

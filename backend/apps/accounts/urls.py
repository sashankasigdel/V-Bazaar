from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/customer/', views.CustomerProfileView.as_view(), name='customer_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('saved-businesses/', views.saved_businesses, name='saved_businesses'),
    path('saved-businesses/<int:business_id>/toggle/', views.toggle_save_business, name='toggle_save'),
]

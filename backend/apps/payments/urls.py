from django.urls import path
from . import views

urlpatterns = [
    path('khalti/initiate/', views.initiate_khalti, name='khalti'),
    path('esewa/initiate/', views.initiate_esewa, name='esewa'),
]

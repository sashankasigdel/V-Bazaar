from django.urls import path
from . import admin_views

urlpatterns = [
    path('stats/', admin_views.admin_stats, name='admin_stats'),
    path('businesses/', admin_views.admin_businesses, name='admin_businesses'),
    path('businesses/<int:pk>/', admin_views.admin_update_business, name='admin_update_business'),
    path('businesses/<int:pk>/delete/', admin_views.admin_delete_business, name='admin_delete_business'),
    path('users/', admin_views.admin_users, name='admin_users'),
    path('users/<int:pk>/', admin_views.admin_update_user, name='admin_update_user'),
    path('orders/', admin_views.admin_orders, name='admin_orders'),
    path('reviews/', admin_views.admin_reviews, name='admin_reviews'),
    path('reviews/<int:pk>/', admin_views.admin_update_review, name='admin_update_review'),
    path('reviews/<int:pk>/delete/', admin_views.admin_delete_review, name='admin_delete_review'),
    path('categories/', admin_views.admin_categories, name='admin_categories'),
    path('categories/create/', admin_views.admin_create_category, name='admin_create_category'),
    path('categories/<int:pk>/delete/', admin_views.admin_delete_category, name='admin_delete_category'),
    path('advertisements/', admin_views.admin_advertisements, name='admin_advertisements'),
    path('advertisements/create/', admin_views.admin_create_advertisement, name='admin_create_advertisement'),
    path('advertisements/<int:pk>/', admin_views.admin_update_advertisement, name='admin_update_advertisement'),
    path('advertisements/<int:pk>/delete/', admin_views.admin_delete_advertisement, name='admin_delete_advertisement'),
]
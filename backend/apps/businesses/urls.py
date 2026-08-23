from django.urls import path
from . import views

urlpatterns = [
    path('', views.BusinessListView.as_view(), name='business_list'),
    path('featured/', views.featured_businesses, name='featured'),
    path('advertisements/', views.active_advertisements, name='advertisements'),
    path('nearby/', views.nearby_businesses, name='nearby'),
    path('categories/', views.BusinessCategoryListView.as_view(), name='categories'),
    path('my/', views.MyBusinessListView.as_view(), name='my_businesses'),
    path('my/qr-bulk/', views.business_qr_bulk, name='business_qr_bulk'),
    path('my/export/', views.business_export, name='business_export'),
    path('my/<slug:slug>/', views.MyBusinessDetailView.as_view(), name='my_business_detail'),
    path('my/<slug:slug>/hours/', views.BusinessHoursView.as_view(), name='business_hours'),
    path('my/<slug:slug>/analytics/', views.business_analytics, name='analytics'),
    path('my/<slug:slug>/gallery/', views.BusinessGalleryListView.as_view(), name='business_gallery'),
    path('gallery/<int:pk>/', views.BusinessGalleryDeleteView.as_view(), name='delete_gallery_photo'),
    path('my/<slug:slug>/archive/', views.archive_branch, name='archive_branch'),
    path('my/<slug:slug>/restore/', views.restore_branch, name='restore_branch'),
    path('my/<slug:slug>/reset-password/', views.reset_branch_admin_password, name='reset_branch_admin_password'),
    path('my/<slug:slug>/qr/', views.business_qr, name='business_qr'),
    path('<slug:slug>/', views.BusinessDetailView.as_view(), name='business_detail'),
]

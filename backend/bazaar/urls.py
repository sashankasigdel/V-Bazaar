from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

FRONTEND_DIR = os.path.join(settings.BASE_DIR.parent, 'frontend')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/businesses/', include('apps.businesses.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/notifications/', include('apps.notifications.urls')),

    # Serve frontend CSS, JS, images with correct MIME types
    re_path(r'^css/(?P<path>.*)$', serve, {'document_root': os.path.join(FRONTEND_DIR, 'css')}),
    re_path(r'^js/(?P<path>.*)$', serve, {'document_root': os.path.join(FRONTEND_DIR, 'js')}),
    re_path(r'^images/(?P<path>.*)$', serve, {'document_root': os.path.join(FRONTEND_DIR, 'images')}),

    # Serve frontend HTML pages
    path('', serve, {'path': 'index.html', 'document_root': FRONTEND_DIR}),
    path('login/', serve, {'path': 'login.html', 'document_root': FRONTEND_DIR}),
    path('register/', serve, {'path': 'register.html', 'document_root': FRONTEND_DIR}),
    path('business/', serve, {'path': 'business.html', 'document_root': FRONTEND_DIR}),
    path('search/', serve, {'path': 'search.html', 'document_root': FRONTEND_DIR}),
    path('checkout/', serve, {'path': 'checkout.html', 'document_root': FRONTEND_DIR}),
    path('dashboard/', serve, {'path': 'dashboard.html', 'document_root': FRONTEND_DIR}),
    path('business-dashboard/', serve, {'path': 'business-dashboard.html', 'document_root': FRONTEND_DIR}),
    path('payment-success/', serve, {'path': 'payment-success.html', 'document_root': FRONTEND_DIR}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

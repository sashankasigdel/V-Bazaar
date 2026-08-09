from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
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
    path('api/admin-panel/', include('apps.accounts.admin_urls')),

    # Serve frontend CSS, JS, images with correct MIME types
    re_path(r'^css/(?P<path>.*)$', serve, {'document_root': os.path.join(FRONTEND_DIR, 'css')}),
    re_path(r'^js/(?P<path>.*)$', serve, {'document_root': os.path.join(FRONTEND_DIR, 'js')}),
    re_path(r'^images/(?P<path>.*)$', serve, {'document_root': os.path.join(FRONTEND_DIR, 'images')}),

    # Serve uploaded media (business logos/banners/gallery) — explicit view instead of
    # django.conf.urls.static.static() because that helper is a no-op when DEBUG=False,
    # which silently broke every uploaded photo URL in production.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # PWA: service worker must be served from the root scope, manifest from a stable top-level path.
    path('sw.js', serve, {'path': 'sw.js', 'document_root': FRONTEND_DIR}),
    path('manifest.json', serve, {'path': 'manifest.json', 'document_root': FRONTEND_DIR}),
    path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': FRONTEND_DIR}),

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
    path('admin-dashboard/', serve, {'path': 'admin-dashboard.html', 'document_root': FRONTEND_DIR}),
    path('admin-login/', serve, {'path': 'admin-login.html', 'document_root': FRONTEND_DIR}),
    path('admin-add-business/', serve, {'path': 'admin-add-business.html', 'document_root': FRONTEND_DIR}),
    path('about/', serve, {'path': 'about.html', 'document_root': FRONTEND_DIR}),
    path('contact/', serve, {'path': 'contact.html', 'document_root': FRONTEND_DIR}),
]

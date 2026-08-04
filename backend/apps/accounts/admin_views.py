from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from apps.businesses.models import Business, BusinessCategory, Advertisement
from apps.orders.models import Order
from apps.reviews.models import Review
from apps.products.models import Product

User = get_user_model()


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.role == 'admin')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    now = timezone.now()
    month_ago = now - timedelta(days=30)
    week_ago = now - timedelta(days=7)

    total_users = User.objects.count()
    total_businesses = Business.objects.count()
    active_businesses = Business.objects.filter(status='active').count()
    pending_businesses = Business.objects.filter(status='pending').count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(Sum('total'))['total__sum'] or 0
    total_reviews = Review.objects.count()
    total_customers = User.objects.filter(role='customer').count()
    total_owners = User.objects.filter(role='business_owner').count()

    orders_this_month = Order.objects.filter(created_at__gte=month_ago).count()
    orders_this_week = Order.objects.filter(created_at__gte=week_ago).count()
    revenue_this_month = Order.objects.filter(status='delivered', created_at__gte=month_ago).aggregate(Sum('total'))['total__sum'] or 0
    new_users_this_month = User.objects.filter(date_joined__gte=month_ago).count()
    new_businesses_this_month = Business.objects.filter(created_at__gte=month_ago).count()

    return Response({
        'total_users': total_users,
        'total_customers': total_customers,
        'total_owners': total_owners,
        'total_businesses': total_businesses,
        'active_businesses': active_businesses,
        'pending_businesses': pending_businesses,
        'total_orders': total_orders,
        'total_revenue': str(total_revenue),
        'total_reviews': total_reviews,
        'orders_this_month': orders_this_month,
        'orders_this_week': orders_this_week,
        'revenue_this_month': str(revenue_this_month),
        'new_users_this_month': new_users_this_month,
        'new_businesses_this_month': new_businesses_this_month,
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_businesses(request):
    from apps.businesses.serializers import BusinessListSerializer
    status_filter = request.query_params.get('status', '')
    search = request.query_params.get('search', '')
    qs = Business.objects.all().select_related('category', 'owner')
    if status_filter:
        qs = qs.filter(status=status_filter)
    if search:
        q = Q(name__icontains=search)
        if search.isdigit():
            q |= Q(id=int(search))
        qs = qs.filter(q)
    qs = qs.order_by('-created_at')

    data = []
    for b in qs:
        data.append({
            'id': b.id,
            'name': b.name,
            'slug': b.slug,
            'owner_email': b.owner.email,
            'owner_name': b.owner.get_full_name(),
            'category': b.category.name if b.category else '',
            'status': b.status,
            'is_featured': b.is_featured,
            'average_rating': str(b.average_rating),
            'total_orders': b.total_orders,
            'total_views': b.total_views,
            'city': b.city,
            'phone': b.phone,
            'created_at': b.created_at.isoformat(),
        })
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_update_business(request, pk):
    try:
        business = Business.objects.get(pk=pk)
        if 'status' in request.data:
            business.status = request.data['status']
        if 'is_featured' in request.data:
            business.is_featured = request.data['is_featured']
        business.save()
        return Response({
            'id': business.id,
            'status': business.status,
            'is_featured': business.is_featured,
        })
    except Business.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_business(request, pk):
    try:
        business = Business.objects.get(pk=pk)
        business.delete()
        return Response({'message': 'Business deleted.'})
    except Business.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_users(request):
    role = request.query_params.get('role', '')
    search = request.query_params.get('search', '')
    qs = User.objects.all()
    if role:
        qs = qs.filter(role=role)
    if search:
        qs = qs.filter(email__icontains=search) | qs.filter(first_name__icontains=search)
    qs = qs.order_by('-date_joined')

    data = []
    for u in qs:
        data.append({
            'id': u.id,
            'email': u.email,
            'full_name': u.get_full_name(),
            'username': u.username,
            'role': u.role,
            'is_active': u.is_active,
            'is_verified': u.is_verified,
            'phone': u.phone,
            'date_joined': u.date_joined.isoformat(),
        })
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if 'is_active' in request.data:
            user.is_active = request.data['is_active']
        if 'is_verified' in request.data:
            user.is_verified = request.data['is_verified']
        user.save()
        return Response({'id': user.id, 'is_active': user.is_active})
    except User.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_orders(request):
    status_filter = request.query_params.get('status', '')
    qs = Order.objects.all().select_related('customer', 'business').order_by('-created_at')[:100]
    if status_filter:
        qs = Order.objects.filter(status=status_filter).select_related('customer', 'business').order_by('-created_at')[:100]

    data = []
    for o in qs:
        data.append({
            'id': o.id,
            'customer_email': o.customer.email,
            'customer_name': o.customer.get_full_name(),
            'business_name': o.business.name,
            'status': o.status,
            'total': str(o.total),
            'payment_method': o.payment_method,
            'is_paid': o.is_paid,
            'created_at': o.created_at.isoformat(),
        })
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_reviews(request):
    qs = Review.objects.all().select_related('customer', 'business').order_by('-created_at')[:100]
    data = []
    for r in qs:
        data.append({
            'id': r.id,
            'customer_name': r.customer.get_full_name(),
            'customer_email': r.customer.email,
            'business_name': r.business.name,
            'rating': r.rating,
            'title': r.title,
            'content': r.content,
            'is_approved': r.is_approved,
            'created_at': r.created_at.isoformat(),
        })
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_update_review(request, pk):
    try:
        review = Review.objects.get(pk=pk)
        if 'is_approved' in request.data:
            review.is_approved = request.data['is_approved']
        review.save()
        return Response({'id': review.id, 'is_approved': review.is_approved})
    except Review.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_review(request, pk):
    try:
        Review.objects.get(pk=pk).delete()
        return Response({'message': 'Review deleted.'})
    except Review.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_categories(request):
    cats = BusinessCategory.objects.all()
    data = [{'id': c.id, 'name': c.name, 'slug': c.slug, 'icon': c.icon, 'order': c.order, 'business_count': c.businesses.count()} for c in cats]
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_category(request):
    from django.utils.text import slugify
    name = request.data.get('name', '')
    icon = request.data.get('icon', '🏪')
    order = request.data.get('order', 0)
    if not name:
        return Response({'error': 'Name is required.'}, status=400)
    slug = slugify(name)
    cat = BusinessCategory.objects.create(name=name, slug=slug, icon=icon, order=order)
    return Response({'id': cat.id, 'name': cat.name, 'slug': cat.slug, 'icon': cat.icon})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_category(request, pk):
    try:
        BusinessCategory.objects.get(pk=pk).delete()
        return Response({'message': 'Category deleted.'})
    except BusinessCategory.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_advertisements(request):
    ads = Advertisement.objects.select_related('business').all()
    data = [{
        'id': a.id,
        'image': a.image.url if a.image else None,
        'business_id': a.business_id,
        'business_name': a.business.name,
        'is_active': a.is_active,
        'order': a.order,
    } for a in ads]
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_create_advertisement(request):
    business_id = request.data.get('business_id')
    image = request.data.get('image')
    if not business_id or not image:
        return Response({'error': 'business_id and image are required.'}, status=400)
    try:
        business = Business.objects.get(pk=business_id)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found.'}, status=404)
    ad = Advertisement.objects.create(business=business, image=image)
    return Response({'id': ad.id, 'business_name': business.name}, status=201)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_update_advertisement(request, pk):
    try:
        ad = Advertisement.objects.get(pk=pk)
        if 'is_active' in request.data:
            ad.is_active = request.data['is_active']
        if 'order' in request.data:
            ad.order = request.data['order']
        ad.save()
        return Response({'id': ad.id, 'is_active': ad.is_active, 'order': ad.order})
    except Advertisement.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_advertisement(request, pk):
    try:
        Advertisement.objects.get(pk=pk).delete()
        return Response({'message': 'Advertisement deleted.'})
    except Advertisement.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)
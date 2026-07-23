from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from apps.orders.models import Order
from .models import Payment


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initiate_khalti(request):
    try:
        order = Order.objects.get(id=request.data.get('order_id'), customer=request.user)
        Payment.objects.update_or_create(order=order, defaults={'method': 'khalti', 'amount': order.total})
        return Response({'message': 'Khalti payment initiated', 'amount': str(order.total)})
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=404)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def initiate_esewa(request):
    try:
        order = Order.objects.get(id=request.data.get('order_id'), customer=request.user)
        Payment.objects.update_or_create(order=order, defaults={'method': 'esewa', 'amount': order.total})
        return Response({'message': 'eSewa payment initiated', 'amount': str(order.total)})
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=404)

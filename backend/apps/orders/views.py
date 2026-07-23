from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order, OrderStatusHistory
from .serializers import OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer


class CustomerOrderListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).select_related('business')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)


class CustomerOrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class BusinessOrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(business__owner=self.request.user, business__slug=self.kwargs['slug'])


class BusinessOrderDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return Order.objects.filter(business__owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status and new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save(update_fields=['status'])
            OrderStatusHistory.objects.create(order=order, status=new_status, note=request.data.get('note', ''))
            return Response({'status': new_status})
        return Response({'error': 'Invalid status.'}, status=400)

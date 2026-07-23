from rest_framework import serializers, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'customer_name', 'rating', 'title', 'content', 'owner_reply', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']

    def validate(self, data):
        user = self.context['request'].user
        business = self.context['business']
        if Review.objects.filter(customer=user, business=business).exists():
            raise serializers.ValidationError("You have already reviewed this business.")
        return data

    def create(self, validated_data):
        return Review.objects.create(
            customer=self.context['request'].user,
            business=self.context['business'],
            **validated_data
        )


class BusinessReviewListView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        return ReviewCreateSerializer if self.request.method == 'POST' else ReviewSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()] if self.request.method == 'POST' else [permissions.AllowAny()]

    def get_queryset(self):
        return Review.objects.filter(business__slug=self.kwargs['slug'], is_approved=True)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        from apps.businesses.models import Business
        ctx['business'] = Business.objects.get(slug=self.kwargs['slug'])
        return ctx


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def owner_reply(request, pk):
    try:
        review = Review.objects.get(pk=pk, business__owner=request.user)
        review.owner_reply = request.data.get('reply', '')
        review.save(update_fields=['owner_reply'])
        return Response({'reply': review.owner_reply})
    except Review.DoesNotExist:
        return Response({'error': 'Not found.'}, status=404)

from django.urls import path
from .views import BusinessReviewListView, owner_reply

urlpatterns = [
    path('<slug:slug>/reviews/', BusinessReviewListView.as_view(), name='business_reviews'),
    path('<int:pk>/reply/', owner_reply, name='owner_reply'),
]

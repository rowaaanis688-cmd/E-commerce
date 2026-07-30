from django.urls import path
from .views import CheckoutView, OrderListView,OrderDetailView

urlpatterns = [
    path('api/orders/checkout/', CheckoutView.as_view(), name='checkout'),
    path('api/orders/', OrderListView.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
from django.urls import path
from .views import CartView, CartItemDetailView

urlpatterns = [
    path('api/cart/', CartView.as_view(), name='cart-main'),

    path('api/cart/items/<int:item_id>/', CartItemDetailView.as_view(), name='cart-item-detail'),
]
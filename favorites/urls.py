from django.urls import path
from .views import FavoriteListCreateView, FavoriteToggleView

urlpatterns = [
    path('', FavoriteListCreateView.as_view(), name='favorite-list'),
    path('toggle/<int:product_id>/', FavoriteToggleView.as_view(), name='favorite-toggle'),
]

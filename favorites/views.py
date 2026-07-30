from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions,generics
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Favorite
from .serializers import FavoriteSerializer

class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
class FavoriteToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        favorite = Favorite.objects.filter(user=request.user, product=product).first()

        if favorite:
            favorite.delete()
            return Response(
                {"message": "product removed from favorites successfully", "is_favorited": False},
                status=status.HTTP_200_OK
            )
        else:
            Favorite.objects.create(user=request.user, product=product)
            return Response(
                {"message": "product added to favorites successfully", "is_favorited": True},
                status=status.HTTP_201_CREATED
            )
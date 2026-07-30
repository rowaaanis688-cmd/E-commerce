from rest_framework import serializers
from .models import Favorite
from products.serializers import ProductSerializer

class FavoriteSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'product_details', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs.get('product')

        if Favorite.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("it's already in your favorites")
        
        return attrs
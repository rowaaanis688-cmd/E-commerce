from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product

class CartView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        if quantity <= 0:
            return Response({'error': 'الكمية يجب أن تكون أكبر من 0'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)

        if product.stock < quantity:
            return Response({'error': f'المخزون المتاح حالياً هو {product.stock} فقط'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            if product.stock < (cart_item.quantity + quantity):
                return Response({'error': 'الكمية الإجمالية تتجاوز المخزون المتاح!'}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        return Response({'message': 'تم إضافة المنتج إلى السلة بنجاح!'}, status=status.HTTP_200_OK)

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'message': 'تم تفريغ السلة بالكامل بنجاح!'}, status=status.HTTP_200_OK)



class CartItemDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        new_quantity = int(request.data.get('quantity', 1))

        if new_quantity <= 0:
            return Response({'error': 'الكمية يجب أن تكون 1 أو أكثر'}, status=status.HTTP_400_BAD_REQUEST)

        if cart_item.product.stock < new_quantity:
            return Response({'error': f'المخزون المتاح فقط هو {cart_item.product.stock}'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = new_quantity
        cart_item.save()
        return Response({'message': 'تم تعديل كمية المنتج بنجاح!'}, status=status.HTTP_200_OK)


    def delete(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return Response({'message': 'تم حذف المنتج من السلة بنجاح!'}, status=status.HTTP_200_OK)


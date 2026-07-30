from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer
from .permissions import IsOrderOwnerOrAdmin  
class CheckoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({'error': 'السلة فارغة، لا يمكنك إتمام الطلب!'}, status=status.HTTP_400_BAD_REQUEST)
        
        for item in cart_items:
            if item.product.stock < item.quantity:
                return Response(
                    {'error': f'المنتج {item.product.name} المخزون المتاح منه هو {item.product.stock} فقط!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        with transaction.atomic():
            order = Order.objects.create(user=user, total_price=0)
            total_price = 0
            for item in cart_items:
                item_total = item.product.price * item.quantity
                total_price += item_total

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                product = item.product
                product.stock -= item.quantity
                product.save()

            order.total_price = total_price
            order.save()

            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response({'message': 'تم إتمام الطلب بنجاح!', 'order': serializer.data}, status=status.HTTP_201_CREATED)


class OrderListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#################################################################################permission
class CheckoutView(views.APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response({'error': 'السلة فارغة، لا يمكنك إتمام الطلب!'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            if item.product.stock < item.quantity:
                return Response(
                    {'error': f'المنتج {item.product.name} المخزون المتاح منه هو {item.product.stock} فقط!'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        with transaction.atomic():
            order = Order.objects.create(user=user, total_price=0)
            total_price = 0

            for item in cart_items:
                item_total = item.product.price * item.quantity
                total_price += item_total

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

                product = item.product
                product.stock -= item.quantity
                product.save()

            order.total_price = total_price
            order.save()
            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response({'message': 'تم إتمام الطلب بنجاح!', 'order': serializer.data}, status=status.HTTP_201_CREATED)


class OrderListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(views.APIView):
    permission_classes = [IsAuthenticated, IsOrderOwnerOrAdmin]  

    def get_object(self, pk):
        order = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(self.request, order)
        return order

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request, pk):
        order = self.get_object(pk)
        
        if order.status != 'Pending':
            return Response({'error': 'لا يمكنك إلغاء طلب تم شحنه أو إكتماله!'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            for item in order.items.all():
                item.product.stock += item.quantity
                item.product.save()
            
            order.status = 'Canceled'
            order.save()

        return Response({'message': 'تم إلغاء الطلب وإرجاع المنتجات للمخزن بنجاح.'}, status=status.HTTP_200_OK)
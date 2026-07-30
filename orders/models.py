from django.db import models
from django.contrib.auth.models import User
from products.models import Product 

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'قيد الانتظار'),
        ('Completed', 'مكتمل'),
        ('Canceled', 'ملغي'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"
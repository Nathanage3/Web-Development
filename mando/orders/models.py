from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.conf import settings
from courses.models import Course, Customer
from uuid import uuid4


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed")
    ]

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    date_purchased = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_PENDING
    )

    def __str__(self):
        return f'Order {self.id} by {self.user.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2,
    validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return f'{self.course.title} in Order {self.order.id}'


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'Cart {self.id} for {self.user.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['cart', 'course']]

    def __str__(self):
        return f'{self.quantity} x {self.course.title} in Cart {self.cart.id}'

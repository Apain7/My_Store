from django.db import models

# Create your models here.

class Order(models.Model):
   
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=50, blank=True, null=True)
    customer_address = models.TextField(blank=True, null=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('processing', 'قيد المعالجة'),
        ('done', 'مكتمل'),
        ('canceled', 'ملغي'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Order #{self.id} - {self.customer_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_image = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product_name}x{self.quantity}'
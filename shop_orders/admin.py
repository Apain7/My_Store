from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_image', 'price', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_price', 'status', 'created_at')
    inlines = [OrderItemInline]
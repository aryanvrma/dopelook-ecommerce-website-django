from django.contrib import admin
from .models import Order, OrderProduct , refund_requested
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]
class RefundAdmin(admin.ModelAdmin):
    model = refund_requested
    readonly_fields = ('user', 'order', 'order_number', 'email')
    extra = 0

admin.site.register(Order, OrderAdmin)
admin.site.register(refund_requested, RefundAdmin)
admin.site.register(OrderProduct)

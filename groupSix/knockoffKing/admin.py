from django.contrib import admin
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import UserModel, Product, Admin, Customer, Seller, Transactions, \
    OrderHistory, ShippingInfo, Order, ShoppingCart, CartItem, OrderItem, ActiveOrders

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'seller_list', 'subTotal', 'status', 'dateCreated', 'dateShipped')
    list_filter = ('status', ('customer', admin.RelatedOnlyFieldListFilter))
    search_fields = ('customer__user__email', 'sellers__user__email')
    ordering = ('-dateCreated',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer').annotate(
            customer_email=Lower('customer__user__email'),
            seller_emails=Lower('sellers__user__email'),
        )
    
    def seller_list(self, obj):
        return ", ".join([seller.name for seller in obj.sellers.all()])

class ProductAdmin(admin.ModelAdmin):
    list_display = ('seller', 'name', 'price', 'quantity', 'id')
    list_filter = ('seller', 'price', 'quantity')
    ordering = ('seller',)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'total_price']

    def total_price(self, obj):
        return obj.total_price()
    total_price.admin_order_field = 'total_price'

admin.site.register(UserModel)
admin.site.register(Product, ProductAdmin)
admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(ActiveOrders)
admin.site.register(OrderHistory)
admin.site.register(ShippingInfo)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShoppingCart)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Transactions)

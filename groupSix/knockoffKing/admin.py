from django.contrib import admin

# Register your models here.
from .models import UserModel, Product, Admin, Customer, Seller, \
    OrderHistory, ShippingInfo, Order, ShoppingCart, CartItem, OrderItem

admin.site.register(UserModel)
admin.site.register(Product)
admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(OrderHistory)
admin.site.register(ShippingInfo)
admin.site.register(Order)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(OrderItem)

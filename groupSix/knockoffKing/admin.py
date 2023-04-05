from django.contrib import admin

# Register your models here.
from .models import User, Product, Admin, Customer, Seller, \
    OrderDetails, ShippingInfo, Order, ShoppingCart, CartItem

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(OrderDetails)
admin.site.register(ShippingInfo)
admin.site.register(Order)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)

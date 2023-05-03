from django.contrib import admin
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import UserModel, Product, Customer, Seller, Transactions, \
    OrderHistory, ShippingInfo, Order, ShoppingCart, CartItem, OrderItem, ActiveOrders

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'seller_list', 'subTotal', 'status', 'date_created', 'date_shipped')
    list_filter = ('dateCreated', 'dateShipped')
    search_fields = ('customer__user__email', 'sellers__user__email')
    ordering = ('-dateCreated',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer').annotate(
            customer_email=Lower('customer__user__email'),
            seller_emails=Lower('sellers__user__email'),
        )
    
    def seller_list(self, obj):
        return ", ".join([seller.name for seller in obj.sellers.all()])   
    
    def date_created(self, obj):
        return obj.dateCreated
    
    date_created.short_description = "Date Created"

    def date_shipped(self, obj):
        return obj.dateShipped
    
    date_created.short_description = "Date Shipped"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('seller', 'name', 'product_price', 'quantity', 'id')
    list_filter = ('seller', 'price', 'quantity')
    search_fields = ('seller__user__email', 'name')
    ordering = ('seller',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('seller').annotate(
            seller_emails=Lower('seller__user__email'),
        )
    
    def product_price(self, obj):
        return f"${obj.price}"


class SellerAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'store_owner', 'owner_email', 'authenticated')
    list_filter = ('authenticated',)
    search_fields = ('user__email', 'name')
    ordering = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').annotate(
            seller_emails=Lower('user__email'),
        )

    def store_name(self, obj):
        return obj.name
    
    def store_owner(self, obj):
        return f"{obj.user.firstName} {obj.user.lastName}"
    
    def owner_email(self, obj):
        return obj.user.email

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_email', 'customer_name', 'join_date')
    list_filter = ('user__joinDate',)
    search_fields = ('user__email',)
    ordering = ('user__lastName',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').annotate(
            customer_emails=Lower('user__email'),
        )
    
    def customer_name(self, obj):
        return f"{obj.user.firstName} {obj.user.lastName}"
    
    def customer_email(self, obj):
        return obj.user.email
    
    def join_date(self, obj):
        return obj.user.joinDate
    
    customer_email.short_description = "Email"

    join_date.short_description = "Date Joined"


class ShippingInfoAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_name', 'address_one', 'address_two', 'city', 'state', 'zipCode')
    search_fields = ('user__email',)
    ordering = ('user__email',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').annotate(
            customer_emails=Lower('user__email'),
        )
    
    def user_name(self, obj):
        return f"{obj.user.firstName} {obj.user.lastName}"
    
    def user_email(self, obj):
        return obj.user.email
    
    def address_one(self, obj):
        return obj.address1
    
    def address_two(self, obj):
        return obj.address2
    
    user_email.short_description = "Email"

    user_name.short_description = "Name"

    address_one.short_description = "Address"

    address_two.short_description = "Address 2"

class ActiveOrdersAdmin(admin.ModelAdmin):
    list_display = ('order', 'user_display', 'seller_list', 'subtotal', 'status', 'date_created', 'date_shipped')
    list_filter = ('order__dateCreated', 'order__dateShipped')
    search_fields = ('order__id', 'user__email', 'order__sellers__user__email')
    ordering = ('-order__dateCreated',) 

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order__customer').annotate(
            customer_email=Lower('order__customer__user__email'),
            seller_emails=Lower('order__sellers__user__email'),
        )
    
    def status(self, obj):
        return dict(Order.statusChoices)[obj.order.status]

    def subtotal(self, obj):
        return obj.order.subTotal

    def seller_list(self, obj):
        return ", ".join([seller.name for seller in obj.order.sellers.all()])

    def user_display(self, obj):
        return f"{obj.user.email}"

    def date_created(self, obj):
        return obj.order.dateCreated

    def date_shipped(self, obj):
        return obj.order.dateShipped
    
    user_display.short_description = 'Customer'

    date_created.admin_order_field = 'order__dateCreated'
    date_created.short_description = 'Date Created'

    date_shipped.admin_order_field = 'order__dateShipped'
    date_shipped.short_description = 'Date Shipped'

class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_email', 'total_price')
    search_fields = ('user__user__email',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user__user').annotate(
            customer_email=Lower('user__user__email'),
        )
    
    def total_price(self, obj):
        return f"${obj.get_total_price()}"

    def customer_email(self, obj):
        return f"{obj.user.user.email}"
    
    customer_email.short_description = 'Customer Email'

class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'user_display', 'seller_list', 'subtotal', 'status', 'date_created', 'date_shipped')
    list_filter = ('order__dateCreated', 'order__dateShipped')
    search_fields = ('order__id', 'user__email', 'order__sellers__user__email')
    ordering = ('-order__dateCreated',) 

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order__customer').annotate(
            customer_email=Lower('order__customer__user__email'),
            seller_emails=Lower('order__sellers__user__email'),
        )
    
    def status(self, obj):
        return dict(Order.statusChoices)[obj.order.status]

    def subtotal(self, obj):
        return obj.order.subTotal

    def seller_list(self, obj):
        return ", ".join([seller.name for seller in obj.order.sellers.all()])

    def user_display(self, obj):
        return f"{obj.user.email}"

    def date_created(self, obj):
        return obj.order.dateCreated

    def date_shipped(self, obj):
        return obj.order.dateShipped
    
    user_display.short_description = 'Customer'

    date_created.admin_order_field = 'order__dateCreated'
    date_created.short_description = 'Date Created'

    date_shipped.admin_order_field = 'order__dateShipped'
    date_shipped.short_description = 'Date Shipped'

class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'user_name', 'join_date')
    list_filter = ('joinDate',)
    search_fields = ('email',)
    ordering = ('email',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').annotate(
            seller_emails=Lower('email'),
        )

    def user_name(self, obj):
        return f"{obj.firstName} {obj.lastName}"
    
    def join_date(self, obj):
        return obj.joinDate
    
    user_name.short_description = "Name"

    join_date.short_description = "Date Joined"

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('seller_email', 'date', 'amount', 'category')
    list_filter = ('date', 'amount',)
    search_fields = ('seller__user__email',)
    ordering = ('date',)


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('seller__user').annotate(
            seller_emails=Lower('seller__user__email'),
        )

    def seller_email(self, obj):
        return obj.seller.user.email
    
    seller_email.short_descrption = "Seller Email"

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_customer', 'order_item', 'quantity', 'item_price')
    search_fields = ('order__sellers__user__email', 'order__customer__user__email')
    ordering = ('order__id',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order__customer').annotate(
            customer_email=Lower('order__customer__user__email'),
            seller_emails=Lower('order__sellers__user__email'),
        )
    
    def order_id(self, obj):
        return obj.order.id
    
    def order_customer(self, obj):
        return obj.order.customer

    def order_item(self, obj):
        return f"{obj.product.name} ({obj.product.seller.name})"

    def item_price(self, obj):
        return obj.total_price()
    
    order_customer.short_description = "Customer Email"

admin.site.register(UserModel, UserModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(ActiveOrders, ActiveOrdersAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(ShippingInfo, ShippingInfoAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Transactions, TransactionsAdmin)

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


# Path Converters:
# int: numbers
# str: strings
# path: whole urls /
# slug: hyphen-and_underscores_stuff
# UUID: universally unique identifiers

# ~~~~~ URLs ~~~~~
urlpatterns = [

    # Navbar
    path('', views.Home, name='home'),
    path('orders/', views.order_history_view, name='orders'),
    path('cart/', views.cart_view, name='cart'),
    path('products/', views.products_view, name='products'),
    path('profile/', views.profile_view, name='profile'),

    # Users
    path('admin/', views.admin_view, name='admin'),
    path('customer/', views.customer_view, name='customer'),
    path('seller/', views.seller_view, name='seller'),

    # Sequences
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('delete_product/<product_id>', views.delete_product_view, name='delete-product'),
    path('update_product/<product_id>', views.update_product_view, name='update-product'),
    

    # Generic Views
    path('seller/<slug:nameSlug>', views.seller_detail_view, name='seller-detail'),
    path('product/<uuid:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order_history/', views.order_history_view, name='order_history_view'),

    # Testing
    path('dashboard/', views.dashboard_view, name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ~~~~~
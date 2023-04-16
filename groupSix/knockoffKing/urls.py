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

    # ~ Home
    path('', views.Home, name='home'),

    # ~ Login/out & Register
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # ~ Profile
    path('profile/', views.profile_view, name='profile'),

    # ~ Stores
    path('seller/<slug:nameSlug>', views.seller_detail_view, name='seller-detail'),

    # ~ Products
    path('products/', views.products_view, name='products'),
    path('product/<uuid:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('update_product/<product_id>', views.update_product_view, name='update-product'),
    path('add_product/', views.add_product_view, name='add-product'),
    path('delete_product/<product_id>', views.delete_product_view, name='delete-product'),
    
    # ~ Cart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    # ~ Checkout & Orders
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.orders_view, name='orders'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ~~~~~
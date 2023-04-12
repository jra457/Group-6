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
    path('orders/', views.orders_view, name='orders'),
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
    

    # Generic Views
    path('seller/<slug:nameSlug>', views.SellerDetailView.as_view(), name='seller-detail'),

    # Testing
    path('dashboard/', views.dashboard_view, name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ~~~~~
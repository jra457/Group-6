from django.urls import path
from . import views

# Path Converters:
# int: numbers
# str: strings
# path: whole urls /
# slug: hyphen-and_underscores_stuff
# UUID: universally unique identifiers

# ~~~~~ URLs ~~~~~
urlpatterns = [

    # Home
    path('', views.Home, name='home'),

    # Users
    path('admin/', views.admin_view, name='admin'),
    path('customer/', views.customer_view, name='customer'),
    path('seller/', views.seller_view, name='seller'),

    # Sequences
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Testing
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
# ~~~~~
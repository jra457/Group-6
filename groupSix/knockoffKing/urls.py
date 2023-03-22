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

    path('', views.Home, name='home'),

]
# ~~~~~
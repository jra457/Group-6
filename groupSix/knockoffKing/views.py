from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from .models import *
from django.http import HttpResponseRedirect



# ~~~~~~~~~~ Home View ~~~~~~~~~~
def Home(request):
    # Check for [HTTP] POST method
    if request.method == 'POST':

        # Fetch username & password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check username & password with database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login user with credentials
            login(request, user)

            # Redirect user to home
            return redirect('home')

    sellerList = Seller.objects.all()

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'sellerList': sellerList,
    }
    # If not [HTTP] POST, render home
    return render(request, 'knockoffKing/home.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Admin View ~~~~~~~~~~
def admin_view(request):

    # ~~~~~ Return Generated Values ~~~~~
    context = {

    }
    return render(request, 'knockoffKing/admin.html', context=context)
    # ~~~~~
# ~~~~~


# ~~~~~~~~~~ Customer View ~~~~~~~~~~
def customer_view(request):

    # ~~~~~ Return Generated Values ~~~~~
    context = {

    }
    return render(request, 'knockoffKing/customer.html', context=context)
    # ~~~~~
# ~~~~~



# ~~~~~~~~~~ Seller View ~~~~~~~~~~
def seller_view(request):

    # ~~~~~ Return Generated Values ~~~~~
    context = {

    }
    return render(request, 'knockoffKing/buyer.html', context=context)
    # ~~~~~
# ~~~~~



# ~~~~~ Seller Detail View ~~~~~
class SellerDetailView(generic.DetailView):
    model = Seller

    slug_field = 'nameSlug'
    slug_url_kwarg = 'nameSlug'

    def seller_detail_view(request, slug):
        seller = get_object_or_404(Seller, nameSlug=slug)

        # ~~~~~ Return Generated Values ~~~~~
        context = {
            'seller': seller,
        }
        return render(request, 'knockoffKing/seller_detail.html', context=context)
        # ~~~~~
# ~~~~~



# ~~~~~~~~~~ Login View ~~~~~~~~~~
def login_view(request):
    # Check for [HTTP] POST method
    if request.method == 'POST':

        # Fetch email & password
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check username & password with database
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Redirect to home if username && password is valid
            login(request, user)
            return redirect('home')
        else:
            # Error output for invalid username || password
            error = 'Invalid username or password'
    else:
        # If not [HTTP] POST, render login page
        error = None

    # Redirect to login page for invalid username || password
    return render(request, 'knockoffKing/login.html', {'error': error})
# ~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Logout View ~~~~~~~~~~
def logout_view(request):

    # Logout user
    logout(request)

    # Redirect to home page after logout
    return redirect('home')
# ~~~~~~~~~~~~~~~~~~~~
    


# ~~~~~~~~~~ Register View ~~~~~~~~~~
def register_view(request):
    print("TEST1")
    if request.method == 'POST':
        # Get the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("TEST2")
        
        # Check if email already exists in database
        if User.objects.filter(email=email).exists():
            print("TEST3")
            return render(request, 'knockoffKing/register.html', {'error': 'Email already in use'})
            
        # Create the user object but do not save it yet
        user = User(first_name=first_name, last_name=last_name, email=email, username=email)
        user.set_password(password)
        print("TEST4")
        # Save the user object to the database
        user.save()

        usermodel = UserModel(user=user, email=email, firstName=first_name, lastName=last_name)
        usermodel.setPass(password)
        usermodel.save()
        
        # Redirect to success page
        return render(request, 'knockoffKing/home.html', {'user': user})
    print("TEST5")
    return render(request, 'knockoffKing/register.html')
# ~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Dashboard View ~~~~~~~~~~
def dashboard_view(request):

    # ~~~~~ Return Generated Values ~~~~~
    context = {

    }
    return render(request, 'knockoffKing/dashboard.html', context=context)
    # ~~~~~
# ~~~~~



# ~~~~~~~~~~ Delete Product ~~~~~~~~~~
def delete_product_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# ~~~~~

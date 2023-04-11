from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group



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

    seller_name = None
    if request.user.is_authenticated:
        try:
            user_instance = request.user
            print("user_instance:", user_instance)

            user_model_instance = UserModel.objects.get(user=user_instance)
            print("user_model_instance:", user_model_instance)
            print("USER EXISTS")
            # Check if the user is a Seller
            try:
                seller = Seller.objects.get(user=user_model_instance)
                print("seller:", seller)

                seller_name = seller.name
                print("seller_name:", seller_name)
                print("USER IS SELLER")

            # If the user is not a Seller, try to find a Customer instance
            except Seller.DoesNotExist:
                try:
                    customer = Customer.objects.get(user=user_model_instance)
                    print("customer:", customer)

                    customer_name = customer.user.firstName
                    print("customer_name:", customer_name)
                    print("USER IS CUSTOMER")

                except Customer.DoesNotExist:
                    print("USER IS NOT CUSTOMER")
                    pass

        except UserModel.DoesNotExist:
            print("USER DOES NOT EXIST")
            pass


    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'sellerList': sellerList,
        # 'user': user,
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

    # URL attributes
    slug_field = 'nameSlug'
    slug_url_kwarg = 'nameSlug'

    def seller_detail_view(request, slug):
        # Get Seller instance from Seller (slug) name
        seller = get_object_or_404(Seller, nameSlug=slug)

        # ~~~~~ Return Generated Values ~~~~~
        context = {
            'seller': seller,
        }
        # Redirect to Seller Detail Page
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

        # Get the form attributes
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('usrTypeSelect')
        
        # Check if email already exists in database
        if User.objects.filter(email=email).exists():
            # Redirect to register page if email already exists
            return render(request, 'knockoffKing/register.html', {'error': 'Email already in use'})
            
        # ~~~ Django User
        user = User(first_name=first_name, last_name=last_name, email=email, username=email) # Create user object
        user.set_password(password) # Set user object password
        user.save() # Save user object

        # ~~~ User Model
        usermodel = UserModel(user=user, email=email, firstName=first_name, lastName=last_name) # Create user model instance
        usermodel.setPass(password) # Set user model instance password
        usermodel.save() # Save user model instance

        # Check user type (Customer or Seller)
        if user_type == 'Customer':
            customer = Customer(user=usermodel) # Create user model instance 
            customer.save() # Save user model instance as customer
            group = Group.objects.get(name='Customer') # Get Customer group
            group.user_set.add(user)  # Add buyer to Customer group
            group.save() # Save group

        elif user_type == 'Seller':
            seller = Seller(user=usermodel) # Create user model instance
            seller.save() # Save user model instance as seller
            group = Group.objects.get(name='Seller') # Get seller group
            group.user_set.add(user)  # Add seller to Seller group
            group.save() # Save group

        # Redirect to home page if success
        return redirect('home')
    
    # Redirect to register page if invalid form
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



# # ~~~~~~~~~~ Review ~~~~~~~~~~
# def review(request, product_id):

#     if request.method == 'POST':
#         # Get the form data
#         review = request.POST.get('reviewValue')

#         product = Product.objects.get(pk=product_id)

#         product.updateReview(review)

#     print("TEST5")
#     return render(request, 'knockoffKing/register.html')
# # ~~~~~~~~~~~~~~~~~~~~

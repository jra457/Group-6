from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required



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
    customer = None
    seller = None
    user_test = None
    group_name = None

    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
            user_test = user_model_instance.user
            group = user_test.groups.first()
            if group:
                group_name = group.name
            else:
                group_name = None

            # Check if the user is a Seller
            try:
                seller = Seller.objects.get(user=user_model_instance)
                seller_name = seller.name

            # If the user is not a Seller, try to find a Customer instance
            except Seller.DoesNotExist:
                try:
                    customer = Customer.objects.get(user=user_model_instance)
                    customer_name = customer.user.firstName

                except Customer.DoesNotExist:
                    pass

        except UserModel.DoesNotExist:
            print("USER DOES NOT EXIST")
            pass

    book_nook = Seller.objects.get(name='Book Nook')
    # books = Product.objects.filter(seller=book_nook)
    book_list = Product.objects.filter(seller=book_nook)[:4]

    sports_world = Seller.objects.get(name='Sports World')
    equipment_list = Product.objects.filter(seller=sports_world)[:4]
    
    

    context = {
        'sellerList': sellerList,
        'customer': customer,
        'seller': seller,
        'user_test': user_test,
        'groupName': group_name,

        'book_nook': book_nook,
        'book_list': book_list,

        'sports_world': sports_world,
        'equipment_list': equipment_list,
    }

    return render(request, 'knockoffKing/home.html', context=context)
# ~~~~~



# ~~~~~~~~~~ Orders View ~~~~~~~~~~
def orders_view(request):

    # ~~~~~ Return Generated Values ~~~~~
    context = {

    }
    return render(request, 'knockoffKing/orders.html', context=context)
    # ~~~~~
# ~~~~~



# ~~~~~~~~~~ Cart View ~~~~~~~~~~
def cart_view(request):
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
        except Customer.DoesNotExist:
            pass

        print("user_instance:", user_instance)
        print("user_model_instance:", user_model_instance)

        cart_instance = ShoppingCart.objects.get(user=user_model_instance)
        cart = cart_instance.items.all()

        print("cart_items:", cart_instance)
        
    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'cart': cart_instance,
    }
    return render(request, 'knockoffKing/cart.html', context=context)
    # ~~~~~
# ~~~~~

@login_required
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
        except Customer.DoesNotExist:
            pass

        print("user_instance:", user_instance)
        print("user_model_instance:", user_model_instance)

        product = get_object_or_404(Product, id=product_id)
        cart, created = ShoppingCart.objects.get_or_create(user=user_model_instance)

        quantity = request.POST.get('quantity', 1)

        cart.add_item(product, quantity)
        context = {'cart': cart}
    return redirect('home')

@login_required
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
        except Customer.DoesNotExist:
            pass

        print("user_instance:", user_instance)
        print("user_model_instance:", user_model_instance)

        product = get_object_or_404(Product, id=product_id)
        cart, created = ShoppingCart.objects.get_or_create(user=user_model_instance)

        cart.remove_item(product)
    return redirect('cart')



# ~~~~~~~~~~ Checkout View ~~~~~~~~~~
@login_required
def checkout_view(request):
    if request.user.is_authenticated:
        user_instance = request.user
        user_model_instance = UserModel.objects.get(user=user_instance)

        cart_instance = ShoppingCart.objects.get(user=user_model_instance)

        # Create a new order
        order = Order()
        order.save()

        # Copy items from the cart to the order
        for cart_item in cart_instance.cartitem_set.all():
            order_item = OrderItem()
            order_item.order = order
            order_item.product = cart_item.product
            order_item.quantity = cart_item.quantity
            order_item.save()

        # Calculate the total price for the order
        order.total_price = cart_instance.get_total_price()
        order.save()

        # Clear the shopping cart
        cart_instance.items.clear()

        # Add order to order history
        order_history = OrderHistory(user=user_model_instance, order=order)
        order_history.save()

        context = {'order': order}
        return render(request, 'knockoffKing/checkout.html', context=context)
    else:
        return redirect('login')
# ~~~~~



# ~~~~~~~~~~ Order History View ~~~~~~~~~~
@login_required
def order_history_view(request):
    if request.user.is_authenticated:
        user_instance = request.user
        user_model_instance = UserModel.objects.get(user=user_instance)
        order_history = OrderHistory.objects.filter(user=user_model_instance)

        context = {'order_history': order_history}
        return render(request, 'knockoffKing/orders.html', context=context)
    else:
        return redirect('login')
# ~~~~~



# ~~~~~~~~~~ Products View ~~~~~~~~~~
def products_view(request):
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
            seller_model_instance = Seller.objects.get(user=user_model_instance)
            seller = seller_model_instance
        except Customer.DoesNotExist:
            pass

        print("user_instance:", user_instance)
        print("user_model_instance:", user_model_instance)
        print("seller_model_instance:", seller_model_instance)

        product_list = Product.objects.filter(seller=seller_model_instance)

        product_test = Product.objects.filter(seller=seller_model_instance)[:1]
        product_test = product_test[0]
        print("product_list:", product_list)
        print("product_test:", product_test)

        print("test", product_test.get_absolute_url())
        
    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'seller': seller,
        'product_list': product_list,
    }
    return render(request, 'knockoffKing/products.html', context=context)
    # ~~~~~
# ~~~~~



# ~~~~~~~~~~ Profile View ~~~~~~~~~~
def profile_view(request):

    # ~~~~~ Return Generated Values ~~~~~
    context = {

    }
    return render(request, 'knockoffKing/profile.html', context=context)
    # ~~~~~
# ~~~~~



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
def seller_detail_view(request, nameSlug):
    # current_user = None
    # seller = None
    # user = None
    # usermodel = None

    # if request.user.is_authenticated:
    #     current_user = request.user
    # try:
    #     usermodel = UserModel.objects.get(user=current_user)
    # except UserModel.DoesNotExist:
    #     pass
    user_instance = None
    user_model_instance = None
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
            user_test = user_model_instance.user
            group = user_test.groups.first()
            if group:
                group_name = group.name
            else:
                group_name = None

            # Check if the user is a Seller
            try:
                seller = Seller.objects.get(user=user_model_instance)
                seller_name = seller.name

            # If the user is not a Seller, try to find a Customer instance
            except Seller.DoesNotExist:
                try:
                    customer = Customer.objects.get(user=user_model_instance)
                    customer_name = customer.user.firstName

                except Customer.DoesNotExist:
                    pass

        except UserModel.DoesNotExist:
            print("USER DOES NOT EXIST")
            pass
    # Get Seller instance from Seller (slug) name
    seller = get_object_or_404(Seller, nameSlug=nameSlug)

    # print("usermodel.getUserID():", usermodel.getUserID())

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'seller': seller,
        # 'current_user': user_instance,
        'user': user_instance,  # Pass the 'User' object to the context
        'usermodel': user_model_instance,  # You can still pass the 'UserModel' object if needed
    }
    # Redirect to Seller Detail Page
    return render(request, 'knockoffKing/seller_detail.html', context=context)
# ~~~~~



# ~~~~~ Seller Detail View ~~~~~
class ProductDetailView(generic.DetailView):
    model = Product

    def product_detail_view(request, primary_key):
        product = get_object_or_404(Product, pk=primary_key)
        context = {
        'product': product,
        }
        return render(request, 'knockoffKing/product_detail.html', context=context)
# ~~~~~



# ~~~~~~~~~~ Update Product ~~~~~~~~~~
def update_product_view(request, product_id):
    if request.method == 'POST':
        # Fetch email & password
        newName = request.POST.get('newName')
        newPrice = request.POST.get('newPrice')
        newQuantity = request.POST.get('newQuantity')

        print("newName:", newName)
        print("newPrice:", newPrice)
        print("newQuantity:", newQuantity)

    product = Product.objects.get(pk=product_id)
    
    product.name = newName
    product.price = newPrice
    product.quantity = newQuantity
    product.save()
    print("product:", product)
    print("product.name:", product.name)
    print("product.price:", product.price)
    print("product.quantity:", product.quantity)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# ~~~~~



# ~~~~~~~~~~ Login View ~~~~~~~~~~
def login_view(request):
    # Check for [HTTP] POST method
    if request.method == 'POST':
        error = "None"
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
            error = 'cock and ball torture!'
    else:
        # If not [HTTP] POST, render login page
        error = "None"

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
    error = "None"
    if request.method == 'POST':
        error = "None"
        
        # Get the form attributes
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('usrTypeSelect')
        
        # Check if email already exists in database
        if User.objects.filter(email=email).exists():
            # Redirect to register page if email already exists
            error = "Email already in use."
            return render(request, 'knockoffKing/register.html', {'error': error})
            
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
    return render(request, 'knockoffKing/register.html', {'error': error})
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

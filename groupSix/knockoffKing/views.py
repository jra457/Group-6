from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage


# ~~~~~~~~~~ Home View ~~~~~~~~~~
def Home(request):

    book_nook = Seller.objects.get(name='Book Nook')
    book_list = Product.objects.filter(seller=book_nook)[:4]

    sports_world = Seller.objects.get(name='Sports World')
    equipment_list = Product.objects.filter(seller=sports_world)[:4]

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
            print("REDIRECT")
            # Redirect user to home
            return redirect('home')

    sellerList = Seller.objects.all()

    seller_name = None
    customer = None
    seller = None
    user_test = None
    group_name = None
    print("TEST1")
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            print("TEST2")
            user_model_instance = UserModel.objects.get(user=user_instance)
            user_test = user_model_instance.user
            group = user_test.groups.first()
            if group:
                group_name = group.name
            else:
                group_name = None

            # Check if the user is a Seller
            try:
                print("TEST3")
                seller = Seller.objects.get(user=user_model_instance)
                seller_name = seller.name

            # If the user is not a Seller, try to find a Customer instance
            except Seller.DoesNotExist:
                try:
                    print("TEST4")
                    customer = Customer.objects.get(user=user_model_instance)
                    customer_name = customer.user.firstName

                except Customer.DoesNotExist:
                    print("TEST5")
                    pass

        except UserModel.DoesNotExist:
            print("USER DOES NOT EXIST")
            pass

    else:
        print("TEST6")
        # ~~~~~ Return Generated Values ~~~~~
        context = {
            'seller': seller,

            'book_nook': book_nook,
            'book_list': book_list,

            'sports_world': sports_world,
            'equipment_list': equipment_list,
        }

        return render(request, 'knockoffKing/home.html', context=context)

    print("TEST7")
    print("request.user:", request.user)
    # print("usermodel.getUserID:", user_model_instance.getUserID())
    # print("seller.user.id", seller.user.id)
    # print("book_list[0].seller:", book_list[0].seller.user_id)
    # print("user_instance.id", user_instance.id)
    print("TEST8")
    # ~~~~~ Return Generated Values ~~~~~
    context = {
        # 'sellerList': sellerList,
        # 'customer': customer,
        'seller': seller,
        # 'user_test': user_test,
        # 'groupName': group_name,
        'usermodel': user_model_instance,

        'book_nook': book_nook,
        'book_list': book_list,

        'sports_world': sports_world,
        'equipment_list': equipment_list,
    }

    return render(request, 'knockoffKing/home.html', context=context)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
            error = 'Incorrect email or password.'
    else:
        # If not [HTTP] POST, render login page
        error = "None"

    # Redirect to login page for invalid username || password
    return render(request, 'knockoffKing/login.html', {'error': error})
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~ Logout View ~~~~~~~~~~
def logout_view(request):

    # Logout user
    logout(request)

    # Redirect to home page after logout
    return redirect('home')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~ Register View ~~~~~~~~~~
def register_view(request):
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
        user = User(first_name=first_name, last_name=last_name, email=email, username=email)  # Create user object
        user.set_password(password)  # Set user object password
        user.save()  # Save user object

        # ~~~ User Model
        # Create user model instance
        usermodel = UserModel(user=user, email=email, firstName=first_name, lastName=last_name)
        usermodel.setPass(password)  # Set user model instance password
        usermodel.save()  # Save user model instance

        # Check user type (Customer or Seller)
        if user_type == 'Customer':
            customer = Customer(user=usermodel)  # Create user model instance
            customer.save()  # Save user model instance as customer
            group = Group.objects.get(name='Customer')  # Get Customer group
            group.user_set.add(user)  # Add buyer to Customer group
            group.save()  # Save group

        elif user_type == 'Seller':
            seller = Seller(user=usermodel)  # Create user model instance
            seller.save()  # Save user model instance as seller
            group = Group.objects.get(name='Seller')  # Get seller group
            group.user_set.add(user)  # Add seller to Seller group
            group.save()  # Save group

        # Redirect to home page if success
        return redirect('home')

    # Redirect to register page if invalid form
    return render(request, 'knockoffKing/register.html', {'error': error})
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~ Profile View ~~~~~~~~~~
@login_required
def profile_view(request):
    success = False
    if request.user.is_authenticated:
        user_instance = request.user
        user_model_instance = UserModel.objects.get(user=user_instance)
        
        if request.method == 'POST':
            # Fetch new First Name/Last Name/Email
            newEmail = request.POST.get('newEmail')
            newFirstName = request.POST.get('newFirstName')
            newLastName = request.POST.get('newLastName')

            if newEmail:
                user_instance.username = newEmail
                user_instance.email = newEmail
                user_model_instance.email = newEmail
            if newFirstName:
                user_instance.first_name = newFirstName
                user_model_instance.firstName = newFirstName
            if newLastName:
                user_instance.last_name = newLastName
                user_model_instance.lastName = newLastName

            user_instance.save()
            user_model_instance.save()
            success = True

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'success': success,

    }
    return render(request, 'knockoffKing/profile.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~ Seller Detail View ~~~~~
def seller_detail_view(request, nameSlug):
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

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'seller': seller,
        # 'current_user': user_instance,
        'user': user_instance,  # Pass the 'User' object to the context
        # You can still pass the 'UserModel' object if needed
        'usermodel': user_model_instance,
    }
    # Redirect to Seller Detail Page
    return render(request, 'knockoffKing/seller_detail.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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

        product_list = Product.objects.filter(seller=seller_model_instance)

        product_test = Product.objects.filter(seller=seller_model_instance)[:1]
        product_test = product_test[0]

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'seller': seller,
        'product_list': product_list,
    }
    return render(request, 'knockoffKing/products.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~ Seller Detail View ~~~~~
class ProductDetailView(generic.DetailView):
    model = Product

    def product_detail_view(request, primary_key):
        product = get_object_or_404(Product, pk=primary_key)

        # ~~~~~ Return Generated Values ~~~~~
        context = {
            'product': product,
        }
        return render(request, 'knockoffKing/product_detail.html', context=context)
        # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~ Update Product ~~~~~~~~~~
def update_product_view(request, product_id):
    if request.method == 'POST':
        # Fetch new Name/Price/Quantity
        newName = request.POST.get('newName')
        newPrice = request.POST.get('newPrice')
        newQuantity = request.POST.get('newQuantity')

        # Fetch product by ID
        product = Product.objects.get(pk=product_id)

    # Update product instance values
    product.name = newName
    product.price = newPrice
    product.quantity = newQuantity
    product.save()  # Save updated product instance

    # Return to update product page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~ Update Product ~~~~~~~~~~
def add_product_view(request):
    error = "None"
    success = False
    if request.method == 'POST':
        # Check if User is logged in
        if request.user.is_authenticated:
            user_instance = request.user
            # Attempt to get seller
            try:
                user_model_instance = UserModel.objects.get(user=user_instance)
                seller = Seller.objects.get(user=user_model_instance)

            # If User is not Seller, Error out
            except Seller.DoesNotExist:
                error = "You must be logged in as a seller to add a product."
                return render(request, 'knockoffKing/add_product.html', {'error': error})

        # Fetch Product Name
        name = request.POST.get('productName')

        # Check if email already exists in database
        if Product.objects.filter(name=name).exists():
            # Redirect to register page if email already exists
            error = "Product already exists."
            return render(request, 'knockoffKing/add_product.html', {'error': error})

        # Fetch the Product Description, Price, Quantity & Image
        descrip = request.POST.get('productDescrip')
        price = request.POST.get('productPrice')
        quantity = request.POST.get('productQuantity')
        image = request.FILES['productImage']

        # Save the image file
        image_path = default_storage.save('products/' + image.name, image)

        # Create the new Product
        product = Product()
        product.name = name
        product.description = descrip
        product.price = price
        product.quantity = quantity
        product.image = image_path
        product.seller = seller
        product.save()
        success = True

        # ~~~~~ (POST) Return Generated Values ~~~~~
        context = {
            'success': success,
            'product': product,
        }
        return render(request, 'knockoffKing/add_product.html', context=context)
        # ~~~~~

    # ~~~~~ (GET) Return Generated Values ~~~~~
    context = {
        'success': success,
    }
    return render(request, 'knockoffKing/add_product.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~ Delete Product ~~~~~~~~~~
def delete_product_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~ Cart View ~~~~~~~~~~
def cart_view(request):
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
        except UserModel.DoesNotExist:  # Update this line
            pass


        cart_instance = ShoppingCart.objects.get(user=user_model_instance)
        cart = cart_instance.items.all()

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'cart': cart_instance,
    }
    return render(request, 'knockoffKing/cart.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@login_required
# ~~~~~~~~~~ Add to Cart View ~~~~~~~~~~
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
        except UserModel.DoesNotExist:  # Update this line
            pass

        product = get_object_or_404(Product, id=product_id)
        cart, created = ShoppingCart.objects.get_or_create(user=user_model_instance)

        quantity = request.POST.get('quantity', 1)

        cart.add_item(product, quantity)
        context = {'cart': cart}
    return redirect('home')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@login_required
# ~~~~~~~~~~ Remove from Cart View ~~~~~~~~~~
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        product = get_object_or_404(Product, id=product_id)
        cart, created = ShoppingCart.objects.get_or_create(customer=customer)

        cart.remove_item(product)
    return redirect('cart')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~ Check Out Cart View ~~~~~~~~~~
@login_required
def checkout_view(request):
    if request.user.is_authenticated:
        user_instance = request.user
        user_model_instance = UserModel.objects.get(user=user_instance)

        cart_instance = ShoppingCart.objects.get(user=user_model_instance)

        # Create a new order
        order = Order()
        order.save()

        # Set to keep track of unique sellers in the order
        sellers_in_order = set()

        # Copy items from the cart to the order
        for cart_item in cart_instance.cartitem_set.all():
            order_item = OrderItem()
            order_item.order = order
            order_item.product = cart_item.product

            # Get product instance & update quantity available
            product = Product.objects.get(pk=order_item.product.id)
            product.quantity = product.quantity - cart_item.quantity
            product.save()

            order_item.quantity = cart_item.quantity
            order_item.save()

            # Add the product's seller to the set
            sellers_in_order.add(product.seller)

        # Assign the unique sellers to the order
        for seller in sellers_in_order:
            order.sellers.add(seller)

        # Calculate the total price for the order
        print("cart_instance.get_total_price():", cart_instance.get_total_price())
        orderTotal = cart_instance.get_total_price()
        print("orderTotal:", orderTotal)
        order.subTotal = orderTotal
        print("order.subTotal:", order.subTotal)
        order.save()

        # Clear the shopping cart
        cart_instance.items.clear()

        # Add order to active orders
        active_order = ActiveOrders(user=user_model_instance, order=order)
        active_order.subTotal = orderTotal
        active_order.save()

        context = {'order': order}
        return render(request, 'knockoffKing/checkout.html', context=context)
    else:
        return redirect('login')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~ Orders View ~~~~~~~~~~
@login_required
def orders_view(request):
    if request.user.is_authenticated:
        user_role = None
        try:
            user_instance = request.user
            user_model_instance = UserModel.objects.get(user=user_instance)
        
            active_orders = ActiveOrders.objects.filter(user=user_model_instance)
            try:
                Seller.objects.get(user_id=user_model_instance.id)
                print("SELLER")
                user_role = 'Seller'
            except Seller.DoesNotExist:
                try:
                    Customer.objects.get(user_id=user_model_instance.id)
                    print("CUSTOMER")
                    user_role = 'Customer'
                except Customer.DoesNotExist:
                    pass
        except UserModel.DoesNotExist:
            pass

        # Print the user role in the terminal
        print(f"User {user_instance} is a {user_role}")
        
        print("active_orders:", active_orders[1].order.sellers.all())

        # ~~~~~ Return Generated Values ~~~~~
        context = {
            'active_orders': active_orders,
            'customer': user_model_instance,
        }
        return render(request, 'knockoffKing/orders.html', context=context)
        # ~~~~~
    else:
        return redirect('login')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~ Order Seller View ~~~~~~~~~~
@login_required
def orders_seller_view(request):
        
    if request.user.is_authenticated:
        user_instance = request.user
    try:
        user_model_instance = UserModel.objects.get(user=user_instance)
        seller_model_instance = Seller.objects.get(user=user_model_instance)
        seller = seller_model_instance
    except Seller.DoesNotExist:
        redirect('orders')

    # seller = Seller.objects.get(pk=seller_id)
    active_orders = Order.objects.filter(sellers=seller)
    print("orders:", active_orders[1].subTotal)
    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'active_orders': active_orders,
        'seller': seller,
    }
    return render(request, 'knockoffKing/seller_orders.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

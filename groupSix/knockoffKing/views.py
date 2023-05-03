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
import re


# ~~~~~~~~~~ Home View ~~~~~~~~~~
def Home(request):
    # Initialize return values
    message = "None"    
    customer = None
    seller = None
    user_model_instance = None

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

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)

            # Check if the user is a Seller
            try:
                seller = Seller.objects.get(user=user_model_instance)

            # If the user is not a Seller, try to find a Customer instance
            except Seller.DoesNotExist:
                try:
                    customer = Customer.objects.get(user=user_model_instance)

                except Customer.DoesNotExist:
                    pass
        # Exception for guests
        except UserModel.DoesNotExist:
            pass

    # Generate seller content for the home page
    book_nook = Seller.objects.get(name='Book Nook')
    book_list = Product.objects.filter(seller=book_nook)[:4]

    sports_world = Seller.objects.get(name='Sports World')
    equipment_list = Product.objects.filter(seller=sports_world)[:4]
    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'usermodel': user_model_instance,
        'seller': seller,
        'customer': customer,

        'book_nook': book_nook,
        'book_list': book_list,

        'sports_world': sports_world,
        'equipment_list': equipment_list,

        'message': message,
    }
    # Get add to cart message
    messages_data = messages.get_messages(request)
    message = next((m for m in messages_data if m.level == messages.SUCCESS), None)
    if message:
        context['message'] = message.message
    return render(request, 'knockoffKing/home.html', context=context)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Login View ~~~~~~~~~~
def login_view(request):
    # Initialize return values
    error = "None"

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
    # Initialize return values    
    error = "None"
    

    if request.method == 'POST':

        # Get form fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('usrTypeSelect')

        # Check if passwords match
        if password1 != password2:
            # Redirect to register page if passwords do not match
            error = "Password do not match."        

        # Check if email already exists in database
        if User.objects.filter(email=email).exists():
            # Redirect to register page if email already exists
            error = f"The email {email} is already in use."
    
        pattern = r'^[a-zA-Z\'\-]+$'
        name = f"{first_name}{last_name}"
        print("name", name)
        if not re.match(pattern, name):
            # Redirect to register page if email already exists\
            print("FALSE")
            error = f"Please enter a valid name containing letters, spaces, apostrophes, and hyphens only."
        

        # ~~~~~ Return Field Inputs ~~~~~
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'user_type': user_type,
            'error': error,
        }
        # ~~~~~

        # Return to register page if error
        if error != "None":
            return render(request, 'knockoffKing/register.html', context=context)


        # ~~~ Django User
        user = User(username=email, email=email, first_name=first_name, last_name=last_name)  # Create user object
        user.set_password(password1)  # Set user object password
        user.save()  # Save user object

        # ~~~ User Model
        # Create user model instance
        usermodel = UserModel(user=user, email=email, firstName=first_name, lastName=last_name)
        usermodel.setPass(password1)  # Set user model instance password
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
    # Initialize return values
    success = False
    error = False
    user_model_instance = None
    user_instance_exists = False
    seller_instance_exists = False
    pattern = r'^[a-zA-Z\'\-]+$'

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
            user_instance_exists = True

        except:
            user_instance_exists = False
        shipping_info, created = ShippingInfo.objects.get_or_create(user=user_model_instance)

        # Check if the user is a Seller
        if user_instance.groups.filter(name='Seller').exists():
            seller = Seller.objects.get(user=user_model_instance)
            seller_instance_exists = True
        else:
            seller = None
        
        if request.method == 'POST':
            # Fetch new First Name/Last Name/Email
            newEmail = request.POST.get('newEmail')
            newFirstName = request.POST.get('newFirstName')
            newLastName = request.POST.get('newLastName')
            newPass1 = request.POST.get('newPass1')
            newPass2 = request.POST.get('newPass2')
            if seller_instance_exists:
                newStoreName = request.POST.get('newStoreName')

            newAdd1 = request.POST.get('newAdd1')
            newAdd2 = request.POST.get('newAdd2')
            newCity = request.POST.get('newCity')
            newState = request.POST.get('newState')
            newZip = request.POST.get('newZip')

            # ~ Update email
            if newEmail:
                # Check if email already exists in database
                if User.objects.filter(email=newEmail).exclude(email=user_instance.email).exists():
                    # Redirect to register page if email already exists
                    error = f"The email {newEmail} is already in use."
                else:
                    user_instance.username = newEmail
                    user_instance.email = newEmail
                    if user_instance_exists:
                        user_model_instance.email = newEmail

            # ~ Update First Name
            if newFirstName:
                if not re.match(pattern, newFirstName):
                    # Redirect to register page if email already exists
                    error = f"Please enter a valid name containing letters, spaces, apostrophes, and hyphens only."
                else:
                    user_instance.first_name = newFirstName
                    if user_instance_exists:
                        user_model_instance.firstName = newFirstName

            # ~ Update Last Name
            if newLastName:
                if not re.match(pattern, newLastName):
                    # Redirect to register page if email already exists
                    error = f"Please enter a valid name containing letters, spaces, apostrophes, and hyphens only."
                else:
                    user_instance.last_name = newLastName
                    if user_instance_exists:
                        user_model_instance.lastName = newLastName

            # ~ Update Password
            if newPass2:
                # Check if passwords match
                if newPass1 == newPass2:
                    user_instance.password = newPass1
                    if user_instance_exists:
                        user_model_instance.password = newPass1
                else:
                    # Redirect to profile page if passwords do not match
                    error = "Password do not match."

            # ~ Update Store Name
            if seller_instance_exists and newStoreName:
                seller.name = newStoreName
                seller.nameSlug = slugify(newStoreName)
                seller.save()

            # ~ Update Address Line 1
            if newAdd1:
                shipping_info.address1 = newAdd1

            # ~ Update Address Line 2
            if newAdd2:
                shipping_info.address2 = newAdd2

            # ~ Update City
            if newCity:
                shipping_info.city = newCity

            # ~ Update State
            if newState:
                shipping_info.state = newState

            # ~ Update Zip Code
            if newZip:
                shipping_info.zipCode = newZip
            
            # Save new information if not error
            if not error:
                user_instance.save()
                shipping_info.save()
                success = True
                if user_instance_exists:
                    user_model_instance.save()

    if seller_instance_exists and not seller.authenticated:
        error = "Seller account is pending approval."

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'user': user_instance,
        'ship': shipping_info,
        'success': success,
        'seller': seller,
        'error': error,
    }
    return render(request, 'knockoffKing/profile.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~ Seller Detail View ~~~~~
def store_view(request, nameSlug):
    # Initialize return values
    user_instance = None
    user_model_instance = None
    seller = None
    customer = None

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)

            # Check if the user is a Seller
            try:
                seller = Seller.objects.get(user=user_model_instance)

            # If the user is not a Seller, try to find a Customer instance
            except Seller.DoesNotExist:
                try:
                    customer = Customer.objects.get(user=user_model_instance)

                except Customer.DoesNotExist:
                    pass
        # Exception for Guests & Admins
        except UserModel.DoesNotExist:
            pass

    # Get Seller instance from Seller (slug) name
    seller = get_object_or_404(Seller, nameSlug=nameSlug)

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'usermodel': user_model_instance,
        'seller': seller,
        'customer': customer,        
    }
    # Redirect to Seller Detail Page
    return render(request, 'knockoffKing/store.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Products View ~~~~~~~~~~
@login_required
def products_view(request):
    # Initialize return values
    seller = None
    customer = None
    seller_model_instance = None
    product_list = None
    seller_instance_exists = False
    error = "None"

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)

            # Check if the user is a Seller
            try:
                seller_model_instance = Seller.objects.get(user=user_model_instance)
                seller = seller_model_instance
                seller_instance_exists = True

            # If the user is not a Seller, try to find a Customer instance
            except Seller.DoesNotExist:
                try:
                    customer = Customer.objects.get(user=user_model_instance)

                except Customer.DoesNotExist:
                    pass
        # Exception for Admins
        except UserModel.DoesNotExist:
            pass

        # Get Products for Seller
        if seller_instance_exists:
            product_list = Product.objects.filter(seller=seller_model_instance)

        # Generate error message if User is Admin or Customer
        else:
            error = "You must be logged in as a Seller to view the Products Page!"

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'seller': seller,
        'product_list': product_list,
        'error': error,
    }
    return render(request, 'knockoffKing/products.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~ Product Detail View ~~~~~
def product_detail_view(request, pk):
    # Get product by Product ID
    product = get_object_or_404(Product, pk=pk)

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        # Check if the user is a Seller
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
            seller = Seller.objects.get(user=user_model_instance)
        # Exception for Admins
        except Seller.DoesNotExist:
            pass

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'product': product,
        'seller': seller,
        'usermodel': user_model_instance,
    }
    return render(request, 'knockoffKing/product_detail.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Update Product ~~~~~~~~~~
@login_required
def update_product_view(request, product_id):
    # Check for [HTTP] POST method
    if request.method == 'POST':
        # Fetch new Name/Price/Quantity
        newName = request.POST.get('newName')
        newDescrip = request.POST.get('newDescrip')
        newPrice = request.POST.get('newPrice')
        newQuantity = request.POST.get('newQuantity')

        # Fetch product by ID
        product = Product.objects.get(pk=product_id)

    # Update product instance values
    product.name = newName
    product.price = newPrice
    product.quantity = newQuantity

    # Check if new description was provided
    if newDescrip.strip() != '':
        product.description = newDescrip

    # Check if new image was provided
    if request.FILES.get('newImage', None) is not None:
        # Save the image file
        newImage = request.FILES['newImage']
        product.image  = default_storage.save('products/' + newImage.name, newImage)
    
    product.save()  # Save updated product instance

    # Return to update product page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Update Product ~~~~~~~~~~
def add_product_view(request):
    # Initialize return values
    error = "None"
    success = False

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user

        # Check if the user is a Seller
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
            seller = Seller.objects.get(user=user_model_instance)

        # If User is not Seller, Error out
        except Seller.DoesNotExist:
            error = "You must be logged in as a seller to add a product."
            return render(request, 'knockoffKing/add_product.html', {'error': error})
        
    # Check for [HTTP] POST method
    if request.method == 'POST':

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
            'seller': seller,
            'success': success,
            'product': product,
        }
        return render(request, 'knockoffKing/add_product.html', context=context)
        # ~~~~~

    # ~~~~~ (GET) Return Generated Values ~~~~~
    context = {
        'seller': seller,
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
    # Initialize return values
    errors = []
    user_model_instance = None
    user_instance_exists = False
    cart_instance = None

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
            user_instance_exists = True
        except UserModel.DoesNotExist:
            pass

        # Populate cart objects or create cart
        if user_instance_exists:
            cart_instance, created = ShoppingCart.objects.get_or_create(user=user_model_instance)
            cart = cart_instance.items.all()
        
            # Check quantity of products in cart
            for product in cart:
                if product.quantity <= 0:
                    # Create error message
                    errors.append(f"The product '{product.name}' is currently out of stock and was removed your from cart.")
                    # Remove item from cart
                    cart_instance.remove_item(product)
            
    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'errors': errors,
        'cart': cart_instance,
    }
    return render(request, 'knockoffKing/cart.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Add to Cart View ~~~~~~~~~~
@login_required
def add_to_cart(request, product_id):
    # Initialize return values
    message = "None"

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
        except UserModel.DoesNotExist:
            pass

        # Add product to cart, create cart if it does not exist
        product = get_object_or_404(Product, id=product_id)
        cart, created = ShoppingCart.objects.get_or_create(user=user_model_instance)
        
        quantity = request.POST.get('quantity', 1)

        # Create success message
        message = f"({quantity}) {product.name} was added to your cart."
        messages.success(request, message)

        cart.add_item(product, quantity)
        context = {
            'message': message,
            'cart': cart,
        }
    return redirect('home')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Remove from Cart View ~~~~~~~~~~
@login_required
def remove_from_cart(request, product_id):
    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
        except UserModel.DoesNotExist:
            pass

        product = get_object_or_404(Product, id=product_id)
        cart, created = ShoppingCart.objects.get_or_create(user=user_model_instance)

        cart.remove_item(product)
        context = {'cart': cart}
    return redirect('cart')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Check Out Cart View ~~~~~~~~~~
@login_required
def checkout_view(request):
    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        user_model_instance = UserModel.objects.get(user=user_instance)
        customer_instance = Customer.objects.get(user=user_model_instance)
        cart_instance = ShoppingCart.objects.get(user=user_model_instance)

        # Create a new order
        order = Order()
        order.customer = customer_instance
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
            order_item.price = product.price

            # Get seller instance & update seller's income
            seller_object = Seller.objects.get(name=product.seller.name)
            earnings = (product.price * order_item.quantity)
            seller_object.checkout(earnings)            
            
            order_item.save()

            # Add the product's seller to the set
            sellers_in_order.add(product.seller)

        # Assign the unique sellers to the order
        for seller in sellers_in_order:
            order.sellers.add(seller)

        # Calculate the total price for the order
        orderTotal = cart_instance.get_total_price()
        order.subTotal = orderTotal
        order.save()

        # Clear the shopping cart
        cart_instance.items.clear()

        # Add order to active orders
        active_order = ActiveOrders(user=user_model_instance, order=order)
        active_order.subTotal = orderTotal
        active_order.save()

        return redirect(reverse('checkout-success', args=[order.id]))
    else:
        return redirect('login')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Orders View ~~~~~~~~~~
@login_required
def checkout_success_view(request, pk):
    # Initialize return values
    user_model_instance = None
    order = get_object_or_404(Order, id=pk)
    order_products = order.items.all()
    

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)

            # Check if the user is a Seller
            try:
                Seller.objects.get(user_id=user_model_instance.id)

            # If the user is not a Seller, try to find a Customer instance
            except Seller.DoesNotExist:
                try:
                    Customer.objects.get(user_id=user_model_instance.id)

                except Customer.DoesNotExist:
                    pass

        # Exception for Admins
        except UserModel.DoesNotExist:
            pass

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'order': order,
        'order_products': order_products,
    }
    return render(request, 'knockoffKing/checkout_success.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Orders View ~~~~~~~~~~
@login_required
def orders_customer_view(request):
    # Initialize return values
    user_model_instance = None
    active_orders = None

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
            active_orders = ActiveOrders.objects.filter(user=user_model_instance)

            # Check if the user is a Seller
            try:
                Seller.objects.get(user_id=user_model_instance.id)

            # If the user is not a Seller, try to find a Customer instance
            except Seller.DoesNotExist:
                try:
                    Customer.objects.get(user_id=user_model_instance.id)

                except Customer.DoesNotExist:
                    pass

        # Exception for Admins
        except UserModel.DoesNotExist:
            pass
        
    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'active_orders': active_orders,
        'customer': user_model_instance,
    }
    return render(request, 'knockoffKing/orders_customer.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~ Order Detail View ~~~~~
@login_required
def order_detail_view(request, pk):
    # Initialize return values
    seller = None

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
        try:
            user_model_instance = UserModel.objects.get(user=user_instance)
            seller = Seller.objects.get(user=user_model_instance)
        except Seller.DoesNotExist:
            pass

    order_history = get_object_or_404(Order, id=pk)
    order_items = order_history.orderitem_set.all()

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'order': order_history,
        'seller': seller,
        'order_items': order_items,
    }
    return render(request, 'knockoffKing/order_detail.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Order Seller View ~~~~~~~~~~
@login_required
def orders_seller_view(request):
    # Initialize return values
    seller = None
    seller_instance_exists = False

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
    try:
        user_model_instance = UserModel.objects.get(user=user_instance)
        seller = Seller.objects.get(user=user_model_instance)
        seller_instance_exists = True
    
    # Exception for Admins
    except Seller.DoesNotExist:
        pass

    # Redirect Customers Orders page
    if not seller_instance_exists:
        return redirect('orders')

    # Exception for Admins
    try:
        active_orders = Order.objects.filter(sellers=seller)
    except:
        active_orders = None

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'active_orders': active_orders,
        'seller': seller,
    }
    return render(request, 'knockoffKing/orders_seller.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Return View ~~~~~~~~~~
@login_required
def return_view(request, oID, pID):
    # Initialize return values
    error = "None"

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
    try:
        user_model_instance = UserModel.objects.get(user=user_instance)
    except User.DoesNotExist:
        redirect('orders')

    # Get Order and Product being returned
    order = get_object_or_404(Order, id=oID)
    product = get_object_or_404(Product, id=pID)

    # Get the Order Item from Product & Order
    item = get_object_or_404(OrderItem, order=order, product=product)

    # Error out if Product cannot be returned
    if not item.return_available():
        error = f"Error: {product.name} in order ({order.id}) has already been returned."

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'error': error,
        'oID': oID,
        'pID': pID,
        'order': order,
        'item': item,
        'product': product,
    }
    return render(request, 'knockoffKing/return.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Return View ~~~~~~~~~~
@login_required
def return_process_view(request, oID, pID):
    # Initialize return values
    quantity = 0

    # Check for [HTTP] POST method
    if request.method == 'POST':
        # Fetch return quantity
        quantity = request.POST.get('quantity')

    # Get Order and Product instances
    quantity = int(quantity)
    order = get_object_or_404(Order, id=oID)
    product = get_object_or_404(Product, id=pID)
    seller = get_object_or_404(Seller, user=product.seller.user)
    item = get_object_or_404(OrderItem, order=order, product=product)

    # Calculate return value
    value = quantity * item.price
    seller.refund(value)

    # Add the Product back to the Seller
    item.returnQuantity += quantity
    item.save()
    product.quantity += quantity
    product.save()

    # Error if Product cannot be returned
    if (item.return_available()):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
    else:
        return redirect('order-detail', pk=oID)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Deposit View ~~~~~~~~~~
def deposit_view(request):
    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
    # Check if the user is a Seller
    try:
        user_model_instance = UserModel.objects.get(user=user_instance)
        seller = Seller.objects.get(user=user_model_instance)
    # Redirect to Orders if invalid Seller
    except Seller.DoesNotExist:
        redirect('orders')

    # Update Seller's balance
    Transactions.objects.create(seller=seller, amount=seller.income, category='Deposit')
    seller.deposit()
    
    # Redirect to seller orders
    return redirect('seller-orders')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Withdraw View ~~~~~~~~~~
def withdraw_view(request):
    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
    # Check if the user is a Seller
    try:
        user_model_instance = UserModel.objects.get(user=user_instance)
        seller = Seller.objects.get(user=user_model_instance)
    # Redirect to Orders if invalid Seller
    except Seller.DoesNotExist:
        redirect('orders')

    # Update Seller's balance
    Transactions.objects.create(seller=seller, amount=seller.income, category='Withdraw')
    seller.withdraw()
    
    # Redirect to seller orders
    return redirect('seller-orders')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Withdraw History View ~~~~~~~~~~
@login_required
def transactions_view(request):
    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user
    # Check if the user is a Seller
    try:
        user_model_instance = UserModel.objects.get(user=user_instance)
        seller = Seller.objects.get(user=user_model_instance)
    # Redirect to Orders if invalid Seller
    except Seller.DoesNotExist:
        redirect('orders')

    # Create list of transactions for corresponding Seller
    transactions = Transactions.objects.filter(seller=seller)

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'transactions': transactions,
        'seller': seller,
    }
    return render(request, 'knockoffKing/transactions.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~ Search View ~~~~~~~~~~
def search_view(request):
    # Initialize return values
    seller = None
    user_model_instance = None

    # If user is logged in, get UserModel instance
    if request.user.is_authenticated:
        user_instance = request.user

        try:
            user_model_instance = UserModel.objects.get(user=user_instance)

            # Check if the user is a Seller
            if user_instance.groups.filter(name='Seller').exists():
                seller = Seller.objects.get(user=user_model_instance)
            else:
                seller = None
        # Exception for Admins
        except:
            pass

    # Get Search query
    query = request.GET.get('q')

    # Search Database for Search query
    products = Product.objects.filter(name__icontains=query)

    # ~~~~~ Return Generated Values ~~~~~
    context = {
        'seller': seller,
        'usermodel': user_model_instance,
        'query': query,
        'products': products
    }
    return render(request, 'knockoffKing/search.html', context=context)
    # ~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
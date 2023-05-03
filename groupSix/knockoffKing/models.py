import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

# ~~~~~ User Model ~~~~~
class UserModel(models.Model):
    """Model representing the User."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    email = models.EmailField(max_length=255, verbose_name='email address', help_text='Enter your Email.', unique=True)

    password = models.CharField(max_length=128)

    firstName = models.CharField(max_length=64, default='', help_text='Enter your Last Name.')

    lastName = models.CharField(max_length=64, default='', help_text='Enter your First Name..')

    joinDate = models.DateTimeField(auto_now_add=True)

    def setPass(self, rawPass):
        """Sets the Password for the User."""
        self.password = make_password(rawPass)

    def testPass(self, rawPass):
        """Checks the User's Password."""
        return check_password(rawPass, self.password)

    def getUserID(self):
        """String for representing the Model object."""
        return self.id

    def __str__(self):
        return f'{self.lastName}, {self.firstName}, {self.email}'

    class Meta:
        verbose_name = "User Model"
        verbose_name_plural = "User Models"
        ordering = ['lastName', 'firstName']

# ~~~~~


# ~~~~~ Product Model ~~~~~
class Product(models.Model):
    """Model representing the Product."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=64, default='',
                            help_text='Enter the product Name.')

    description = models.TextField(
        default='', max_length=1000, help_text='Enter the product Description.')

    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, help_text='Enter product Price')

    quantity = models.IntegerField(
        default=1, help_text='Enter product Quantity')

    image = models.ImageField(upload_to='products/', blank=True, null=True)

    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, null=True, blank=True, help_text='Select the Product.')

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    def getName(self):
        """String for representing the Model object."""
        return self.name

    def __str__(self):
        try:
            return f'{self.seller.name}, {self.name}, ${self.price} ({self.quantity})'
        except:
            return ''

    def get_absolute_url(self):
        """Returns the url to access a particular location instance."""
        return reverse('product-detail', args=[str(self.id)])
# ~~~~~


# ~~~~~ Admin Model ~~~~~
class Admin(models.Model):
    """Model representing the Admin."""
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    def __str__(self):
        """String for representing the Model object."""
        return self.user.email
# ~~~~~


# ~~~~~ Customer Model ~~~~~
class Customer(models.Model):
    """Model representing the Customer."""
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    def __str__(self):
        """String for representing the Model object."""
        return self.user.email
# ~~~~~


# ~~~~~ Seller Model ~~~~~
class Seller(models.Model):
    """Model representing the Seller."""
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    name = models.CharField(max_length=64, default='', help_text='Enter the store Name.')

    nameSlug = models.SlugField(unique=True, null=True, blank=True, default=user)

    income = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    prevWithdraw = models.DateTimeField(null=True, blank=True)

    authenticated = models.BooleanField(default=False, help_text='Authenticate Seller.')

    def get_absolute_url(self):
        nameSlug = slugify(self.name)

        """Returns the url to access a particular location instance."""
        return reverse('seller-detail', args=[nameSlug])

    def checkout(self, val):
        self.income += val
        self.save()

    def refund(self, val):
        self.income -= val
        self.save()

    def deposit(self):
        self.income = 0
        self.save()

    def withdraw(self):
        self.income = 0
        self.prevWithdraw = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        """Override the save method to set the slug_name field."""
        if self.name == '':
            self.nameSlug = slugify(self.user.email)
            self.name = self.nameSlug
        else:
            self.name = self.name
            self.nameSlug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        if self.user is not None:
            return f'{self.name} ({self.user.email})'
        else:
            return f'{self.name} (No associated user)'

    def __uuid__(self):
        return self.user.id

    class Meta:
        ordering = ['name', 'user__email']
# ~~~~~


# ~~~~~ Shipping Info Model ~~~~~
class Transactions(models.Model):
    """Model representing the transaction history for a Seller."""
    categories = (
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
    )

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)

    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    category = models.CharField(
        max_length=10, choices=categories, default='Deposit')
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
# ~~~~~


# ~~~~~ Shipping Info Model ~~~~~
class ShippingInfo(models.Model):
    """Model representing the Shipping Info."""
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    address1 = models.CharField(max_length=16, default='', help_text='Address Line 1', db_column="streetNumber")

    address2 = models.CharField(max_length=64, default='', help_text='Address Line 2', db_column="streetName")

    city = models.CharField(max_length=64, default='', help_text='City')

    # ~~~~~ Location State
    Alabama, Alaska, Arizona = 'AL', 'AK', 'AZ'
    Arkansas, California, Colorado = 'AR', 'CA', 'CO'
    Connecticut, Delaware, Florida = 'CT', 'DE', 'FL'
    Georgia, Hawaii, Idaho = 'GA', 'HI', 'ID'
    Illinois, Indiana, Iowa = 'IL', 'IN', 'IA'
    Kansas, Kentucky, Louisiana = 'KS', 'KY', 'LA'
    Maine, Maryland, Massachusetts = 'ME', 'MD', 'MA'
    Michigan, Minnesota, Mississippi = 'MI', 'MN', 'MS'
    Missouri, Montana, Nebraska = 'MO', 'MT', 'NE'
    Nevada, New_Hampshire, New_Jersey = 'NV', 'NH', 'NJ'
    New_Mexico, New_York, North_Carolina = 'NM', 'NY', 'NC'
    North_Dakota, Ohio, Oklahoma = 'OR', 'PA', 'RI'
    Oregon, Pennsylvania, Rhode_Island = 'OR', 'PA', 'RI'
    South_Carolina, South_Dakota, Tennessee = 'SC', 'SD', 'TN'
    Texas, Utah, Vermont = 'TX', 'UT', 'VT'
    Virginia, Washington, West_Virginia = 'VA', 'WA', 'WV'
    Wisconsin, Wyoming = 'WI', 'WY'

    stateChoices = [
        (Alabama, 'Alabama'), (Alaska, 'Alaska'), (Arizona, 'Arizona       '),
        (Arkansas, 'Arkansas'), (California,
                                 'California'), (Colorado, 'Colorado      '),
        (Connecticut, 'Connecticut'), (Delaware,
                                       'Delaware'), (Florida, 'Florida       '),
        (Georgia, 'Georgia'), (Hawaii, 'Hawaii'), (Idaho, 'Idaho         '),
        (Illinois, 'Illinois'), (Indiana, 'Indiana'), (Iowa, 'Iowa          '),
        (Kansas, 'Kansas'), (Kentucky, 'Kentucky'), (Louisiana, 'Louisiana     '),
        (Maine, 'Maine'), (Maryland, 'Maryland'), (Massachusetts, 'Massachusetts '),
        (Michigan, 'Michigan'), (Minnesota,
                                 'Minnesota'), (Mississippi, 'Mississippi   '),
        (Missouri, 'Missouri'), (Montana, 'Montana'), (Nebraska, 'Nebraska      '),
        (Nevada, 'Nevada'), (New_Hampshire,
                             'New Hampshire'), (New_Jersey, 'New Jersey    '),
        (New_Mexico, 'New Mexico'), (New_York,
                                     'New York'), (North_Carolina, 'North Carolina'),
        (North_Dakota, 'North Dakota'), (Ohio,
                                         'Ohio'), (Oklahoma, 'Oklahoma      '),
        (Oregon, 'Oregon'), (Pennsylvania,
                             'Pennsylvania'), (Rhode_Island, 'Rhode Island  '),
        (South_Carolina, 'South Carolina'), (South_Dakota,
                                             'South Dakota'), (Tennessee, 'Tennessee     '),
        (Texas, 'Texas'), (Utah, 'Utah'), (Vermont, 'Vermont       '),
        (Virginia, 'Virginia'), (Washington,
                                 'Washington'), (West_Virginia, 'West Virginia '),
        (Wisconsin, 'Wisconsin'), (Wyoming, 'Wyoming')
    ]

    state = models.CharField(
        max_length=2,
        choices=stateChoices,
        blank=True,
        default='',
        help_text="State",
    )
    # ~~~~~

    zipCode = models.IntegerField(null=True, blank=True, help_text='Zip Code')

    def getAddress(self):
        """String for representing the Model object."""
        return f"{self.address1} {self.address2}, {self.city}, {self.state}"

    def __str__(self):
        """String for representing the Model object."""
        if self.address2:
            returnStr = f"({self.user.email}) {self.address1}, {self.address2}, {self.city}, {self.state}, {self.zipCode}"
        else:
            returnStr = f"({self.user.email}) {self.address1}, {self.city}, {self.state}, {self.zipCode}"
        return returnStr
    
    class Meta:
        verbose_name = "Shipping Info"
        verbose_name_plural = "Shipping Info"
# ~~~~~


# ~~~~~ Order Model ~~~~~
class Order(models.Model):
    """Model representing the Order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sellers = models.ManyToManyField(Seller)

    items = models.ManyToManyField(Product, through='OrderItem')

    dateCreated = models.DateTimeField(auto_now_add=True)

    dateShipped = models.DateField(null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, help_text='Select the Customer.')

    shippingID = models.ForeignKey(ShippingInfo, on_delete=models.CASCADE, null=True, help_text='Select the Shipping Info.')

    # ~~~~~ Shipping Status
    orderPlaced, packaging, shipped, = '01', '02', '03'
    inTransit, outForDelivery, delayed, = '04', '05', '06'
    delivered = '07'

    statusChoices = [
        (orderPlaced, 'Order Placed'), (packaging,
                                        'Packaging'), (shipped, 'Shipped'),
        (inTransit,   'In Transit'), (outForDelivery,
                                      'Out for Delivery'), (delayed, 'Delayed'),
        (delivered,   'Delivered '),
    ]

    # This may need to be models.IntegerField since the codes are 01-07
    status = models.CharField(
        max_length=2,
        choices=statusChoices,
        default=orderPlaced,
        help_text="Shipping Status",
    )
    # ~~~~~

    subTotal = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def getTotal(self):
        return self.subTotal

    def __str__(self):
        """String for representing the Model object."""
        return str(self.id)

    def get_absolute_url(self):
        """Returns the url to access a particular location instance."""
        return reverse('order-detail', args=[str(self.id)])
# ~~~~~


# ~~~~~ Order Item Model ~~~~~
class OrderItem(models.Model):
    """Model representing a specific Item in an Order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=0)

    returnQuantity = models.PositiveIntegerField(default=0)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def get_absolute_url(self):
        """Returns the url to access a particular order item instance."""
        return reverse('return', args=[str(self.order.id), str(self.product.id)])

    def return_available(self):
        if (self.returnQuantity >= self.quantity):
            return False
        else:
            return True

    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.quantity}x {self.product} in {self.order}'
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
# ~~~~~


# ~~~~~ ActiveOrders Model ~~~~~
class ActiveOrders(models.Model):
    """Model representing the Active Orders."""
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.order)
    
    class Meta:
        verbose_name = "Active Order"
        verbose_name_plural = "Active Orders"
# ~~~~~


# ~~~~~ Order History Model ~~~~~
class OrderHistory(models.Model):
    """Model representing the Order Details."""
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.order)
    
    class Meta:
        verbose_name = "Order History"
        verbose_name_plural = "Order History"
# ~~~~~


# ~~~~~ Shopping Cart Model ~~~~~
class ShoppingCart(models.Model):
    """Model representing the Shopping Cart."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    items = models.ManyToManyField(Product, through='CartItem')

    def get_total_price(self):
        total = sum(cart_item.total_price()
                    for cart_item in self.cartitem_set.all())
        return total

    def add_item(self, product, quantity=1):
        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(shoppingCart=self, product=product)

        if created:
            # If the item is newly created, set the quantity
            cart_item.quantity = quantity
        else:
            # If the item already exists, update the quantity
            cart_item.quantity += quantity

        cart_item.save()

    def remove_item(self, product):
        cart_item = self.cartitem_set.filter(product=product).first()
        if cart_item.quantity == 1:
            cart_item.delete()
        elif cart_item.quantity > 1:
            cart_item.quantity -= 1

            cart_item.save()

    def __str__(self):
        """String for representing the Model object."""
        return str(self.id)
    
    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
# ~~~~~


# ~~~~~ Cart Item Model ~~~~~
class CartItem(models.Model):
    """Model representing a specific Item in a Shopping Cart."""
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    dateAdded = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return (self.quantity * self.product.price)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.quantity}x {self.product} in {self.shoppingCart}'
# ~~~~~

from django.db import models
from django.urls import reverse
import uuid
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.

# ~~~~~ User Model ~~~~~
class User(models.Model):
    """Model representing the User."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.id
# ~~~~~



# ~~~~~ Admin Model ~~~~~
class Admin(models.Model):
    """Model representing the Admin."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    def __str__(self):
        """String for representing the Model object."""
        return self.user.id
# ~~~~~



# ~~~~~ Customer Model ~~~~~
class Customer(models.Model):
    """Model representing the Customer."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    def __str__(self):
        """String for representing the Model object."""
        return self.user.id
# ~~~~~



# ~~~~~ Seller Model ~~~~~
class Seller(models.Model):
    """Model representing the Seller."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    def __str__(self):
        """String for representing the Model object."""
        return self.user.id
# ~~~~~



# ~~~~~ Order Details Model ~~~~~
class OrderDetails(models.Model):
    """Model representing the Order Details."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # productID: int

    # productName: string

    # quantity: int

    # unitCost: float

    # subTotal: float

    def __str__(self):
        """String for representing the Model object."""
        return self.id
# ~~~~~



# ~~~~~ Shipping Info Model ~~~~~
class ShippingInfo(models.Model):
    """Model representing the Shipping Info."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    streetNumber = models.IntegerField(max_length=16, default='', help_text='Street Number')

    streetName = models.CharField(max_length=64, default='', help_text='Street Name')

    city = models.CharField(max_length=64, default='', help_text='City')

    # ~~~~~ Location State
    Alabama       , Alaska        , Arizona        = 'AL', 'AK', 'AZ'
    Arkansas      , California    , Colorado       = 'AR', 'CA', 'CO'
    Connecticut   , Delaware      , Florida        = 'CT', 'DE', 'FL'
    Georgia       , Hawaii        , Idaho          = 'GA', 'HI', 'ID'
    Illinois      , Indiana       , Iowa           = 'IL', 'IN', 'IA'
    Kansas        , Kentucky      , Louisiana      = 'KS', 'KY', 'LA'
    Maine         , Maryland      , Massachusetts  = 'ME', 'MD', 'MA'
    Michigan      , Minnesota     , Mississippi    = 'MI', 'MN', 'MS'
    Missouri      , Montana       , Nebraska       = 'MO', 'MT', 'NE'
    Nevada        , New_Hampshire , New_Jersey     = 'NV', 'NH', 'NJ'
    New_Mexico    , New_York      , North_Carolina = 'NM', 'NY', 'NC'
    North_Dakota  , Ohio          , Oklahoma       = 'OR', 'PA', 'RI'
    Oregon        , Pennsylvania  , Rhode_Island   = 'OR', 'PA', 'RI'
    South_Carolina, South_Dakota  , Tennessee      = 'SC', 'SD', 'TN'
    Texas         , Utah          , Vermont        = 'TX', 'UT', 'VT'
    Virginia      , Washington    , West_Virginia  = 'VA', 'WA', 'WV'
    Wisconsin     , Wyoming                        = 'WI', 'WY'

    stateChoices = [
        (Alabama       , 'Alabama'       ), (Alaska       , 'Alaska'       ), (Arizona       , 'Arizona       '),
        (Arkansas      , 'Arkansas'      ), (California   , 'California'   ), (Colorado      , 'Colorado      '),
        (Connecticut   , 'Connecticut'   ), (Delaware     , 'Delaware'     ), (Florida       , 'Florida       '),
        (Georgia       , 'Georgia'       ), (Hawaii       , 'Hawaii'       ), (Idaho         , 'Idaho         '),
        (Illinois      , 'Illinois'      ), (Indiana      , 'Indiana'      ), (Iowa          , 'Iowa          '),
        (Kansas        , 'Kansas'        ), (Kentucky     , 'Kentucky'     ), (Louisiana     , 'Louisiana     '),
        (Maine         , 'Maine'         ), (Maryland     , 'Maryland'     ), (Massachusetts , 'Massachusetts '),
        (Michigan      , 'Michigan'      ), (Minnesota    , 'Minnesota'    ), (Mississippi   , 'Mississippi   '),
        (Missouri      , 'Missouri'      ), (Montana      , 'Montana'      ), (Nebraska      , 'Nebraska      '),
        (Nevada        , 'Nevada'        ), (New_Hampshire, 'New Hampshire'), (New_Jersey    , 'New Jersey    '),
        (New_Mexico    , 'New Mexico'    ), (New_York     , 'New York'     ), (North_Carolina, 'North Carolina'),
        (North_Dakota  , 'North Dakota'  ), (Ohio         , 'Ohio'         ), (Oklahoma      , 'Oklahoma      '),
        (Oregon        , 'Oregon'        ), (Pennsylvania , 'Pennsylvania' ), (Rhode_Island  , 'Rhode Island  '),
        (South_Carolina, 'South Carolina'), (South_Dakota , 'South Dakota' ), (Tennessee     , 'Tennessee     '),
        (Texas         , 'Texas'         ), (Utah         , 'Utah'         ), (Vermont       , 'Vermont       '),
        (Virginia      , 'Virginia'      ), (Washington   , 'Washington'   ), (West_Virginia , 'West Virginia '),
        (Wisconsin     , 'Wisconsin'     ), (Wyoming      , 'Wyoming'      )
    ]

    state = models.CharField(
        max_length=2,
        choices=stateChoices,
        default=Alabama,
        help_text="State",
    )
    # ~~~~~

    zipCode = models.IntegerField(max_length=5, default='', help_text='Zip Code')

    # shippingType: string

    # shippingCost: float

    def __str__(self):
        """String for representing the Model object."""
        return self.user.id
# ~~~~~



# ~~~~~ Order Model ~~~~~
class Order(models.Model):
    """Model representing the Order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # dateCreated: date

    # dateShipped: date

    # custerName: string

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, help_text='Select the Customer.')

    # ~~~~~ Shipping Status
    orderPlaced, packaging     , shipped, = '01', '02', '03'
    inTransit  , outForDelivery, delayed, = '04', '05', '06'
    delivered,                            = '07'

    statusChoices = [
        (orderPlaced, 'Order Placed'), (packaging     , 'Packaging'       ), (shipped, 'Shipped'), 
        (inTransit,   'In Transit'  ), (outForDelivery, 'Out for Delivery'), (delayed, 'Delayed'),
        (delivered,   'Delivered '  ),
    ]

    # This may need to be models.IntegerField since the codes are 01-07
    status = models.CharField(
        max_length=2,
        choices=statusChoices,
        default=orderPlaced,
        help_text="Shipping Status",
    )
    # ~~~~~

    shippingID = models.ForeignKey(ShippingInfo, on_delete=models.CASCADE, null=True, help_text='Select the Shipping Info.')

    def __str__(self):
        """String for representing the Model object."""
        return self.id
# ~~~~~



# ~~~~~ Shopping Cart Model ~~~~~
class ShoppingCart(models.Model):
    """Model representing the Shopping Cart."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text='Select the User.')

    # productID: int

    # quantity: int

    # dateAdded: date

    def __str__(self):
        """String for representing the Model object."""
        return self.id
# ~~~~~

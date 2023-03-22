from django.db import models
from django.urls import reverse
import uuid
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.

# ~~~~~ Admin Model ~~~~~
class admin(models.Model):
    """Model representing the Admin."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.id
# ~~~~~



# ~~~~~ Shopping Cart Model ~~~~~
class shoppingCart(models.Model):
    """Model representing the Shopping Cart."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.id
# ~~~~~



# ~~~~~ Customer Model ~~~~~
class customer(models.Model):
    """Model representing the Customer."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.id
# ~~~~~



# ~~~~~ Seller Model ~~~~~
class seller(models.Model):
    """Model representing the Seller."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        """String for representing the Model object."""
        return self.id
# ~~~~~
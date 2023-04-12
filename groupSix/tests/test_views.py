from django.test import TestCase
from django.urls import reverse
from knockoffKing.models import UserModel, Product, Admin, Customer, Seller, OrderDetails, ShippingInfo, Order, ShoppingCart, CartItem


class UserModelViewTest(TestCase):

    def setUp(self):


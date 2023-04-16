from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserModel, Product, Admin, Customer, Seller, ShippingInfo, Order, OrderHistory, ShoppingCart, CartItem
from .urls import urlpatterns


class UserLoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='user@example.com', password='testpass')
        self.usermodel = UserModel.objects.create(user=self.user, email='user@example.com', firstName='John', lastName='Doe')
        self.usermodel.setPass('testpass')
        self.user.save()
        self.usermodel.save()


    def test_customer_login_logout(self):
        customer = Customer.objects.create(user=self.usermodel)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get('/customer/')
        self.assertNotEqual(response.status_code, 200)

    def test_seller_login_logout(self):


    def test_admin_login_logout(self):
        


    def test_wrong_pass(self):
        response = self.client.login(username='testuser', password='wrongpass')
        self.assertFalse(response)

    def test_user_doesnotexist(self):
        response = self.client.login(username='notauser', password='testpass')
        self.assertFalse(response)


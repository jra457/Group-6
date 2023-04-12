from django.test import TestCase
from knockoffKing.models import UserModel, Product, Admin, Customer, Seller, OrderDetails, ShippingInfo, Order, ShoppingCart, CartItem

class UserModelTest(TestCase):
    def setUp(self):
        self.usermodel = UserModel.objects.create(id=1001, user='Test User', email='test@example.com',
        password='example123', firstName='John', lastName='Smith', joinDate='01/01/23')

    def test_userID(self):
        self.assertEqual(self.usermodel.id, 1001)
    
    def test_user_username(self):
        self.assertEqual(self.usermodel.user, 'Test User')

    def test_user_email(self):
        self.assertEqual(self.usermodel.email, 'test@example.com')

    def test_user_password(self):
        self.assertEqual(self.usermodel.password, 'example123')

    def test_user_firstName(self):
        self.assertEqual(self.usermodel.firstName, 'John')

    def test_user_lastName(self):
        self.assertEqual(self.usermodel.lastName, 'Smith')

    def test_user_joinDate(self):
        self.assertEqual(self.usermodel.joinDate, '01/01/23')

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from .models import UserModel, Product, Admin, Customer, Seller, ShippingInfo, Order, OrderItem, OrderHistory, ShoppingCart, CartItem
from .urls import urlpatterns
from django.core.files.uploadedfile import SimpleUploadedFile


class UserLoginTest(TestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            username='testcustomer', password='testpass')
        self.seller = User.objects.create_user(
            username='testseller', password='testpass')
        self.admin = User.objects.create_user(
            username='testadmin', password='testpass')

    def test_buyer_login(self):
        response = self.client.login(
            username='testcustomer', password='testpass')
        self.assertTrue(response)

    def test_seller_login(self):
        response = self.client.login(
            username='testseller', password='testpass')
        self.assertTrue(response)

    def test_admin_login(self):
        response = self.client.login(username='testadmin', password='testpass')
        self.assertTrue(response)

    def test_invalid_login(self):
        response = self.client.login(username='invalid', password='testpass')
        self.assertFalse(response)

    def test_logout(self):
        self.client.login(username='testbuyer', password='testpass')
        response = self.client.logout()
        self.assertIsNone(response)


class SellerTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(
            username='seller_test', email='seller@test.com', password='testpassword')
        user_model = UserModel.objects.create(
            user=user, email=user.email, firstName='Seller', lastName='Test')
        self.seller = Seller.objects.create(user=user_model, name='Test Shop')

    def test_add_product(self):
        product = Product.objects.create(
            name='Test Product', description='Test Description', price=10.0, quantity=10, seller=self.seller)
        self.assertEqual(product.name, 'Test Product')

    def test_remove_product(self):
        product = Product.objects.create(
            name='Test Product', description='Test Description', price=10.0, quantity=10, seller=self.seller)
        Product.objects.all().delete()

    def test_edit_product(self):
        product = Product.objects.create(
            name='Test Product', description='Test Description', price=10.0, quantity=10, seller=self.seller)
        product.price = 11.0
        product.save()

        self.assertEqual(product.price, 11.0)

    def test_sell_product(self):
        product = Product.objects.create(
            name='Test Product', description='Test Description', price=10.0, quantity=10, seller=self.seller)
        self.assertEqual(product.quantity, 10)

        product.quantity -= 5
        product.save()

        self.assertEqual(product.quantity, 5)

    def test_receive_payment(self):
        user = User.objects.create(
            username='customer_test', email='customer@test.com', password='testpassword')
        user_model = UserModel.objects.create(
            user=user, email=user.email, firstName='Customer', lastName='Test')
        customer = Customer.objects.create(user=user_model)

        order = Order.objects.create(customer=customer)

        product = Product.objects.create(
            name='Test Product', description='Test Description', price=10.0, quantity=10, seller=self.seller)

        order_item = OrderItem.objects.create(
            order=order, product=product, price=product.price, quantity=2)

        self.assertEqual(order_item.total_price(), 20.0)

        shopping_cart = ShoppingCart.objects.create(user=user_model)

        cart_item = CartItem.objects.create(
            shoppingCart=shopping_cart, product=product, quantity=2)

        self.assertEqual(shopping_cart.get_total_price(), 20.0)


class CustomerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.user_model_instance = UserModel.objects.create(
            user=self.user, email='test@example.com', firstName='Test', lastName='User')

    def test_customer_instance_creation(self):
        customer = Customer.objects.create(user=self.user_model_instance)
        self.assertIsInstance(customer, Customer)

    def test_customer_str_representation(self):
        customer = Customer.objects.create(user=self.user_model_instance)
        self.assertEqual(str(customer), self.user_model_instance.email)

    def test_customer_user_model_relationship(self):
        customer = Customer.objects.create(user=self.user_model_instance)
        self.assertEqual(customer.user, self.user_model_instance)

    def test_customer_deletion_on_user_model_deletion(self):
        customer = Customer.objects.create(user=self.user_model_instance)
        self.user_model_instance.delete()
        with self.assertRaises(Customer.DoesNotExist):
            Customer.objects.get(user=self.user_model_instance)

    def test_customer_queryset_ordering(self):
        user1 = User.objects.create_user(
            username='testuser1', password='testpassword')
        user_model_instance1 = UserModel.objects.create(
            user=user1, email='test1@example.com', firstName='Alice', lastName='Smith')

        user2 = User.objects.create_user(
            username='testuser2', password='testpassword')
        user_model_instance2 = UserModel.objects.create(
            user=user2, email='test2@example.com', firstName='Bob', lastName='Johnson')

        customer1 = Customer.objects.create(user=user_model_instance1)
        customer2 = Customer.objects.create(user=user_model_instance2)

        customers = Customer.objects.all()

        self.assertEqual(customers[0], customer1)
        self.assertEqual(customers[1], customer2)


class AdminTestCase(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.client.login(username='admin', password='adminpassword')

        user1 = User.objects.create_user(
            username='testuser1', password='testpassword')
        user_model_instance1 = UserModel.objects.create(
            user=user1, email='test1@example.com', firstName='Alice', lastName='Smith')

        # Create a sample seller user
        self.seller_user = Seller.objects.create(user=user_model_instance1)

        # Create some sample products and a regular user
        self.product1 = Product.objects.create(
            name='Product1', price=100, seller=self.seller_user)
        self.product2 = Product.objects.create(
            name='Product2', price=200, seller=self.seller_user)
        self.regular_user = User.objects.create_user(
            username='user', email='user@example.com', password='userpassword'
        )

    def test_delete_user(self):
        # Delete a regular user
        response = self.client.post(
            f'/admin/auth/user/{self.regular_user.id}/delete/',
            {'post': 'yes'}
        )
        self.assertTrue(response)
        self.assertFalse(User.objects.filter(username='user').exists())

    def test_remove_product(self):
        # Remove a product
        response = self.client.post(
            f'/admin/knockoffKing/product/{self.product1.id}/delete/',
            {'post': 'yes'}
        )
        self.assertTrue(response)
        self.assertFalse(Product.objects.filter(name='Product1').exists())

    def test_create_seller(self):
        # Create a new seller
        response = self.client.get('/admin/knockoffKing/seller/add/')
        self.assertTrue(response)
        form = response.context['adminform'].form
        data = form.initial
        data.update({
            'user': 'a5a87a77-3c7b-4f6f-94a2-1316fafe1aee',
            'name': 'NewSeller',
            'income': 100
        })
        response = self.client.post('/admin/knockoffKing/seller/add/', data)
        self.assertTrue(response)

    def test_create_admin_account(self):
        # Create a new admin account
        new_admin = User.objects.create_superuser(
            username='newadmin',
            email='newadmin@example.com',
            password='newadminpassword'
        )

        self.assertIsNotNone(new_admin)
        self.assertTrue(new_admin.is_superuser)

    def test_view_users_list(self):
        # View the list of users
        response = self.client.get('/admin/auth/user/')
        self.assertTrue(response)
        self.assertContains(response, 'admin')
        self.assertContains(response, 'user')

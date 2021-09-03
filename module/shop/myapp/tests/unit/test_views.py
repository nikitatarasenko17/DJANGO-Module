from myapp.models import Product
from django.test import TestCase, RequestFactory
from myapp.views import Login, Register, ProductPurchaseView
from myapp.models import MyUser, Purchase

class LoginTestCase(TestCase):

    def setUp(self):
        request = RequestFactory().get('/')
        self.view = Login()
        self.view.setup(request)

    def test_login_success_url(self):
        success_url = self.view.get_success_url()
        self.assertEqual('/', success_url)

    def test_get_templates_names(self):
        templates_names = self.view.get_template_names()
        self.assertEqual(['login.html'], templates_names)

    def test_get_incorrect_templates_names(self):
        templates_names = self.view.get_template_names()
        self.assertNotEqual(['login.html', 'logout.html'], templates_names)


class RegisterTestCase(TestCase):

    def setUp(self):
        request = RequestFactory().get('/')
        self.view = Register()
        self.view.setup(request)

    def test_register_success_url(self):
        success_url = self.view.get_success_url()
        self.assertEqual('/', success_url)
        
    def test_get_templates_names(self):
        templates_names = self.view.get_template_names()
        self.assertEqual(['register.html'], templates_names)


class ProductPurchaseTestCase(TestCase):
    def setUp(self):
        self.consumer = MyUser.objects.create_user(username="Ivan", password="1z2x3c", wallet=10000)
        self.product = Product.objects.create(title="iMac", price=1200.000,in_stock=10)
        self.purchase = Purchase.objects.create(consumer=self.consumer, product=self.product)

    def test_purchase_one(self):
        self.assertEqual(1, self.purchase.quantity)

    def test_response_code(self):
        self.assertEqual(Product.objects.get().title, "iMac")


    # def test_purchase_wallet(self):
    #     self.assertEqual(99000, self.consumer.wallet)



    

    # def tearDown(self):
    #     self.view.quit()

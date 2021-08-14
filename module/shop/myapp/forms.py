from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from myapp.models import Product, MyUser, Purchase, Return

class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title',)

class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username',)

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'in_stock')

class ReturnForm(ModelForm):
    class Meta:
        model = Return
        fields = ('ret_product',)

class PurchaseProductForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity']

    





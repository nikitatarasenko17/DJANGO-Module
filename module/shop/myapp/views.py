from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from myapp.forms import RegisterForm, ProductCreateForm, AddProductForm, ReturnForm, PurchaseProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView
from myapp.models import *
from django.urls import reverse_lazy


class ProductListView(ListView):
    model = Product
    paginate_by = 3
    template_name = 'product_list.html'
    login_url = 'login/'
    extra_context = {'buy_form': PurchaseProductForm()}
    

class Login(LoginView):
    next_page = '/'
    template_name = 'login.html'

class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.wallet = 100000
        obj.save()
        return super().form_valid(form=form)

class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'

class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    http_method_names = ['post']
    form_class = ProductCreateForm
    success_url = '/'

class AddProductView(LoginRequiredMixin, CreateView):
    login_url = "login/"
    http_method_names = ['get', 'post']
    form_class = AddProductForm
    template_name = 'add_product.html'
    extra_context = {'add_form': AddProductForm()}
    success_url="/" 

class UpdateProductView(LoginRequiredMixin, UpdateView):
    login_url = "login/"
    template_name = 'update_product.html'
    model = Product
    fields = ['title', 'description', 'price', 'in_stock']
    success_url="/" 

class ProductPurchaseView(LoginRequiredMixin, CreateView):
    login_url = "login/"
    form_class = PurchaseProductForm
    http_method_names = ['post', 'get']
    paginate_by = 3
    success_url='/'

    def form_valid(self, form):
        purchase = form.save(commit=False)
        purchase.consumer = self.request.user
        purchase.product = Product.objects.get(pk=self.kwargs["pk"])
        purchase.save()
        return super().form_valid(form=form)

    
class ProductPurchaseListView(LoginRequiredMixin, ListView):
    login_url = "login/"
    model = Purchase
    template_name = 'purchase_product.html'
          
    def purchase_list(self):
        consumer = self.request.user
        return consumer.product.all()

class ReturnProductView(LoginRequiredMixin, CreateView):
    login_url = "login/"
    http_method_names = ['get', 'post']
    form_class = ReturnForm
    template_name = 'return_product.html'
    extra_context = {'return_form': ReturnForm()}

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form=form)
from django.views.generic.edit import DeleteView
from myapp.forms import RegisterForm, ProductCreateForm, AddProductForm, ReturnForm, PurchaseProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, LoginSuperUserRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView
from myapp.models import Product, Purchase, Return
from django.db import transaction
from django.http import HttpResponseRedirect



class ProductListView(ListView):
    model = Product
    paginate_by = 3
    ordering = ['title']
    template_name = 'product_list.html'
    login_url = '/login/'
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
    template_name = 'product_list.html'
    paginate_by = 3
    success_url='/'

    def form_valid(self, form):
        purchase = form.save(commit=False)
        purchase.consumer = self.request.user
        purchase.product = Product.objects.get(pk=self.request.POST.get('product_id'))
        return super().form_valid(form=form)

    
class ProductPurchaseListView(LoginRequiredMixin, ListView):
    login_url = "login/"
    model = Purchase
    template_name = 'purchase_product.html'
    extra_context = {"form": ReturnForm}
              
    def purchase_list(self):
        consumer = self.request.user
        return consumer.product.all()

class ReturnProductView(LoginRequiredMixin, CreateView):
    login_url = "login/"
    form_class = ReturnForm
    success_url="/product/purchases/"
    
    def form_valid(self, form):
        self.ret_product = Purchase.objects.get(pk=self.request.POST.get('product_id'))
        self.ret_product_ret = form.save(commit=False)
        self.ret_product_ret.ret_product = self.ret_product
        self.ret_product_ret.save()
        return super().form_valid(form=form)

class Confirm(LoginSuperUserRequiredMixin, DeleteView):
    model = Purchase
    success_url = '/product/returns/'

    def delete(self, request, *args, **kwargs):
        obj_product = self.get_object()
        success_url = '/product/returns/'
        item = obj_product.self.product
        consumer = obj_product.consumer
        consumer.wallet += item.price * obj_product.quantity
        item.in_stock += obj_product.quantity
        with transaction.atomic():
            consumer.save()
            item.save()
            obj_product.delete() 
        return HttpResponseRedirect(success_url)           

class Reject(LoginSuperUserRequiredMixin, DeleteView):
    model = Return
    success_url = '/product/returns/'

    def delete(self, request, *args, **kwargs):
        purchase = self.get_object()
        success_url = '/product/returns/'
        product = purchase.purchase
        product.return_status = True
        with transaction.atomic():
            product.save()
            purchase.delete()
        return HttpResponseRedirect(success_url)
            
class ReturnListView(LoginSuperUserRequiredMixin, ListView):
    login_url = "login/"
    model = Return
    template_name = 'return_product.html'
    paginate_by = 3

    def return_list(self):
        consumer = self.request.user
        return consumer.ret_product.all()
           
      
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from myapp.forms import RegisterForm, AddProductForm, ReturnForm, PurchaseProductForm
from myapp.models import Product, Purchase, Return
from django.contrib.auth.mixins import LoginRequiredMixin, LoginSuperUserRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class ProductListView(ListView):
    login_url = '/login/'
    model = Product
    paginate_by = 3
    ordering = ['title']
    template_name = 'product_list.html'
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


class AddProductView(LoginSuperUserRequiredMixin, CreateView):
    login_url = "login/"
    form_class = AddProductForm
    template_name = 'add_product.html'
    extra_context = {'add_form': AddProductForm()}
    success_url="/" 


class UpdateProductView(LoginSuperUserRequiredMixin, UpdateView):
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
    
    def delete(self, request, *args, **kwargs):
        obj_product = self.get_object()
        success_url= reverse_lazy('returns')
        self.product = obj_product.product
        self.consumer = obj_product.consumer
        self.consumer.wallet += self.product.price * obj_product.quantity
        self.product.in_stock += obj_product.quantity
        with transaction.atomic():
            self.consumer.save()
            self.product.save()
            obj_product.delete() 
        return HttpResponseRedirect(success_url)  


class Reject(LoginSuperUserRequiredMixin, DeleteView):
    model = Return
    
    def delete(self, request, *args, **kwargs):
        obj_return = self.get_object()
        success_url= reverse_lazy('returns')
        self.ret_product = obj_return.ret_product
        self.ret_product.return_status = True
        with transaction.atomic():
            self.ret_product.save()
            obj_return.delete()
        return HttpResponseRedirect(success_url)

            
class ReturnListView(LoginRequiredMixin, ListView):
    login_url = "login/"
    model = Return
    template_name = 'return_product.html'
    paginate_by = 3

           
      
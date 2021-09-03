from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *
from myapp.API.resources import AuthorViewSet, BookViewSet, ProductViewSet, PurchaseViewSet, AdminReturnViewSet
from rest_framework.authtoken import views

router = SimpleRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'products', ProductViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'returns', AdminReturnViewSet)


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('login/', Login.as_view(), name = 'login'),
    path('register/', Register.as_view(), name = 'register'),
    path('logout/', Logout.as_view(), name = 'logout'),
    path('product/add_product', AddProductView.as_view(), name = 'add_product'),
    path('product/<int:pk>/update/', UpdateProductView.as_view(), name = 'update_product'),
    path('product/purchase/', ProductPurchaseView.as_view(), name = 'purchase_create'),
    path('product/purchases/', ProductPurchaseListView.as_view(), name = 'purchases'),
    path('product/return/', ReturnProductView.as_view(), name = 'ret_product'),
    path('product/returns/', ReturnListView.as_view(), name = 'returns'),
    path('product/returns/confirm/<int:pk>', Confirm.as_view(), name = 'confirm'),
    path('product/returns/reject/<int:pk>', Reject.as_view(), name = 'reject'),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
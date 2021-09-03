from rest_framework.serializers import Serializer
from myapp.models import MyUser
from django.db.models import query
from django.db.models.base import Model
from django.urls import reverse_lazy
from django.db import transaction
from myapp.API.autentification import TemporaryTokenAuthentication
from rest_framework.viewsets import ModelViewSet
from myapp.API.serializers import AuthorSerializer, BookSerializer, AuthorByBookSerializer, UserSerializer, ProductSerializer, PurchaseSerializer, ReturnListProductSerializer
from myapp.exception import NotAvailableAmount, NotEnoughMoney, NotQuantity
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from myapp.models import Author, Book, Product, Purchase, Return

#HW 38

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer 
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('book_name')
        if name:
            queryset = queryset.filter(writer__title__icontains=name)
        return queryset

    @action(detail=True)
    def get_author_by_book(self, request, pk=None):
        author = self.get_object()
        serializer = AuthorByBookSerializer(author)
        return Response(serializer.data)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 

    def perform_create(self, serializer):
        serializer.save(title = serializer.validated_data.get('title') + "!")

    def get_queryset(self):
        queryset = super().get_queryset()
        age = self.request.query_params.get('author_age')
        try:
            age = int(age)
        except ValueError:
            age = None
        except TypeError:
            age = None
        if age:
            queryset = queryset.filter(author__age__gte=age)
        return queryset

# HW 39

class UserViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

class ProductViewSet(ModelViewSet):
    authentication_classes = [TemporaryTokenAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def list(self, request, *args, **kwargs):
        queryset = Purchase.objects.filter(user=self.request.user)
        serializer = PurchaseSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except NotAvailableAmount:
            raise APIException('No available amount')
        except NotEnoughMoney:
            raise APIException('You dont have enough money')
        except NotQuantity:
            raise APIException('You dont enter the quantity')


class AdminReturnViewSet(ModelViewSet):
    queryset = Return.objects.all()
    serializer_class = ReturnListProductSerializer
    permission_classes = [IsAdminUser]

    # @action(methods=['POST'], detail=True)
    # def confirm(self, request, pk=None, *args, **kwargs):
    #     obj_product = self.get_object()









            

        

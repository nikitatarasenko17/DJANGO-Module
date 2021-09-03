from rest_framework import serializers
from myapp.models import MyUser, Product, Purchase, Author, Book, Return

# HW 37

SEX = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unknown'),
)

ENGLISH = (
    ('A1', 'Beginner'),
    ('A2', 'Elementary'),
    ('B1', 'Pre Intermediate'),
    ('B2', 'Intermediate'),
    ('C1', 'Upper Intermediate'),
    ('C2', 'Advanced'),
)

class RequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    sex = serializers.ChoiceField(choices=SEX)
    english_level = serializers.ChoiceField(choices=ENGLISH)

    def validate(self, data):
        fit = False
        if data.get('sex') == 'M':
            fit = data.get('english_level') in ['B1', 'C1', 'C2'] and int(data.get('age')) >= 20
        elif data.get('sex') == 'F':
            fit = data.get('english_level') in ['B1', 'B2', 'C1', 'C2'] and int(data.get('age')) >= 22
        if not fit:
            raise serializers.ValidationError('You dont match')
        return data

# Module_SHOP

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'in_stock']
        
        def validate(self, data):
            if data['price'] <= 0:
                raise serializers.ValidationError("Price don't specified")
            elif data['in_stock'] <= 0:
                raise serializers.ValidationError("The product is out of stock")
            else:
                return data

class PurchaseSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Purchase
        fields = ['consumer', 'product', 'quantity', 'created']

        def validate(self, data):
            if data['quantity'] <= 0:
                raise serializers.ValidationError("Don't have enough quantity")
            else:
                return data

class PurchaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['consumer', 'product', 'quantity', 'created']

class UserSerializer(serializers.ModelSerializer):
    purchases = PurchaseListSerializer(many=True, source='product')

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'password' 'wallet', 'is_staff', 'purchases']

class CreateReturnProductSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField()

    class Meta:
        model = Return
        fields = ['id', 'ret_product', 'created']

class ReturnListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = ['id', 'ret_product', 'created']


#HW №38
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        

class AuthorByBookSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='book_set')
    class Meta:
        model = Author
        fields = ['name', 'age', 'books']






        
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

class MyUser(AbstractUser):
    wallet = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

class Product(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=3)
    in_stock = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Products'
        
    def __str__(self):
        return self.title

class Purchase(models.Model):
    consumer = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='consumer_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    return_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.consumer.username
    
    def save(self, *args, **kwargs):
        if self.product.in_stock >= self.quantity and self.consumer.wallet >= (self.product.price * self.quantity):
            self.product.in_stock -= self.quantity
            self.consumer.wallet -= self.product.price * self.quantity
            self.consumer.save()
            self.product.save()
            super(Purchase, self).save(*args, **kwargs)
        elif self.quantity > self.product.in_stock:
            raise ValidationError('No available amount')
        elif self.quantity * self.product.price > self.consumer.wallet:
            raise ValidationError('You dont have enough money')
        elif self.quantity == 0:
            raise ValidationError('You dont enter the quantity')

class Return(models.Model):
    ret_product = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='ret_product')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if (timezone.now() - self.ret_product.created).seconds < 180:
            self.ret_product.status = True
            with transaction.atomic():
                self.ret_product.save()
                super(Return, self).save(*args, **kwargs)
        else:
            raise ValidationError('You want to return product so late')

    def __str__(self):
        return str(self.ret_product)
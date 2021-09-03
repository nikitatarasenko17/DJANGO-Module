from django.contrib import admin
from .models import *

admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Return)

#HW №38
admin.site.register(Author)
admin.site.register(Book)


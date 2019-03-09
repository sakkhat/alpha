from django.contrib import admin

from account.models import Account
from .models import Product

# Register your models here.
admin.site.register(Account)
admin.site.register(Product)
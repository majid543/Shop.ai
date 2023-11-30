from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Brand, Product,Cart,Contact,Checkout

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Contact)
admin.site.register(Checkout)
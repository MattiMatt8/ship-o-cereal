from fractions import Fraction
import math
from django.contrib import admin
from django.db import models
from products.models import Product



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','brand','active','stock')
    fields = ['name','brand','description','contents','weight','price', 'category','active','stock','percentage_off','discounted_price']
    readonly_fields = ('id',)
    list_filter = ('brand',)
    list_editable = ('active',)
    search_fields = ('name','id','brand__name')

    def has_delete_permission(self, request, obj=None):
        return False

class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('id','name','percentage_off','discounted_price','new_price')
    fields = ['name','brand','description','contents','weight','price', 'category','active','stock','percentage_off','discounted_price']
    readonly_fields = ('id',)
    list_filter = ('brand',)
    list_editable = ('percentage_off',)
    search_fields = ('name','id','brand__name')

    def has_delete_permission(self, request, obj=None):
        return False

    def new_price(self,obj):
        price = Fraction(obj.price)
        percentage_off = Fraction(obj.percentage_off)
        discount = (percentage_off / 100) * price
        final_price = Fraction(price - discount)
        return float(Fraction(math.floor(final_price*100), 100))



class ProductDiscount(Product):
    class Meta:
        proxy = True



admin.site.register(Product, ProductAdmin)

admin.site.register(ProductDiscount, ProductDiscountAdmin)


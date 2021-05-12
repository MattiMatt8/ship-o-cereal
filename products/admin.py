from django.contrib import admin
from django.db import models
from products.models import Product



class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'brand','active')
    fields = ['name','brand','description','contents','weight','price', 'category','active','stock','percentage_off','discounted_price']
    readonly_fields = ('id',)
    list_filter = ('brand',)
    list_editable = ('active',)
    search_fields = ('name','id','brand__name')

    def has_delete_permission(self, request, obj=None):
        return False

class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'brand','active')
    fields = ['name','brand','description','contents','weight','price', 'category','active','stock','percentage_off','discounted_price']
    readonly_fields = ('id',)
    list_filter = ('brand',)
    list_editable = ('active',)
    search_fields = ('name','id','brand__name')

    def has_delete_permission(self, request, obj=None):
        return False

class ProductDiscount(Product):
    class Meta:
        proxy = True



admin.site.register(Product, ProductAdmin)

admin.site.register(ProductDiscount, ProductDiscountAdmin)


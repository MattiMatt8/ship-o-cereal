import math
from fractions import Fraction
from django.contrib import admin
from products.models import Product, Image


class ProductLabelInlineAdmin(admin.TabularInline):
    """Selection to select labels for a product."""
    model = Product.labels.through

class ImageInlineAdmin(admin.TabularInline):
    """Selection to select images for a product."""
    model = Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','brand','active','stock')
    fields = ('id','name','review_calculated','stock','price','active', 'category','brand','description','info','weight','contents', 'label_info')
    readonly_fields = ('id','info','review_calculated','label_info')
    list_filter = ('brand',)
    list_editable = ('active','stock')
    search_fields = ('name','id','brand__name')
    inlines = (ProductLabelInlineAdmin, ImageInlineAdmin)

    def has_delete_permission(self, request, obj=None):
        return False

    def info(self, obj):
        return "If the product is not cereal please leave weight & contents fields empty."

    def label_info(self, obj):
        return "Each label can only be selected once."


class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'percentage_off', 'price', 'new_price')
    list_display_links = None
    fields = ['name', 'brand', 'description', 'contents', 'weight', 'price', 'category', 'active', 'stock',
              'percentage_off', 'discounted_price']
    readonly_fields = ('id',)
    list_filter = ('brand',)
    list_editable = ('percentage_off',)
    search_fields = ('name', 'id', 'brand__name')

    def has_delete_permission(self, request, obj=None):
        return False

    def new_price(self, obj):
        """Returns and sets the discounted price for a given product object."""

        # If percentage_off exceeds 100, reset the price
        if obj.percentage_off > 100 or obj.percentage_off <= 0:
            obj.percentage_off = 0
            obj.discounted_price = None
            obj.save()

            return obj.price

        # Calculate the discounted price
        price = Fraction(obj.price)
        percentage_off = Fraction(obj.percentage_off)
        discount = (percentage_off / 100) * price
        final_price = Fraction(price - discount)
        new = float(Fraction(math.floor(final_price*100), 100))

        # Save and set the discounted price
        obj.discounted_price = new
        obj.save()

        return new

    def has_add_permission(self, request):
        return False


class ProductDiscount(Product):
    """Proxy model so we can use the Product model
    on two different admin pages."""
    class Meta:
        proxy = True


# admin.site.register(Label, LabelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDiscount, ProductDiscountAdmin)


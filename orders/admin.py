from django.contrib import admin
from django.utils.html import format_html

from orders.models import Order


# TODO: Maybe change read only fields?
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'date', 'status', 'total')
    readonly_fields = (
        'id', 'date', 'user', 'first_name', 'last_name', 'phone_number', 'address_street_name',
        'address_house_number', 'address_city', 'address_zip', 'address_country', 'address_additional_comments',
        'products_total', 'shipping_cost', 'total', 'order_products')
    list_filter = ('status', 'date')
    list_editable = ('status',)
    search_fields = ('id', 'first_name', 'last_name', 'user__username', 'total')

    def has_add_permission(self, request):
        return False

    def full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    def has_delete_permission(self, request, obj=None):
        return False

    # TODO: Check out, maybe skip id?
    # TODO: Maybe fix style, add image?
    def order_products(self, obj):
        """Creates a table with all the order items that are in the order."""
        table = """<table id="result_list">
                      <thead>
                      <tr>
                        <th scope="col">
                          <div class="text"><span>Product ID</span></div>
                          <div class="clear"></div>
                        </th>
                        <th scope="col">
                          <div class="text"><span>Product Name</span></div>
                          <div class="clear"></div>
                        </th>
                        <th scope="col">
                          <div class="text"><span>Quantity</span></div>
                          <div class="clear"></div>
                        </th>
                        <th scope="col">
                          <div class="text"><span>Price</span></div>
                          <div class="clear"></div>
                        </th>
                      </tr>
                      </thead>
                      <tbody>"""
        for order_item in obj.order_items.all():
            table += f"""<tr>
                            <td class="field-id">{order_item.product.id}</td>
                            <td class="field-name">{order_item.product.name}</td>
                            <td class="field-quantity">{order_item.quantity}</td>
                            <td class="field-price">{order_item.price}</td>
                          </tr>"""
        table += "</tbody></table>"
        return format_html(table)


admin.site.register(Order, OrderAdmin)

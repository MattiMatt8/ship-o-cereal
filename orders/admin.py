from django.contrib import admin

from orders.models import Order

class OrderAdmin(admin.ModelAdmin):

    list_display = ('id','full_name','date','status','total')
    readonly_fields = ('id',)
    list_filter = ('status','date')
    list_editable = ('status',)
    search_fields = ('id','first_name','last_name','user__username','total')

    def has_add_permission(self, request):
        return False

    def full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Order,OrderAdmin)
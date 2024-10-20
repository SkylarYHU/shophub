from django.contrib import admin
from .models import * 


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'complete']
    list_filter = ['complete'] 

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
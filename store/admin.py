from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name","user","email"]

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "catagory", "time"]
    search_fields = ["name"]

class OrderAdmin(admin.ModelAdmin):
    list_display =["id","customer"]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "get_total", "date_added",]

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display =["order","address","pincode",'date_added']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['customer','title','date_added']


admin.site.register(Catagory)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Feedback, FeedbackAdmin)

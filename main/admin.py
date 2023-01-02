from django.contrib import admin
from main import models

class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('order','product', 'quantity', 'date_added')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('id','customer','complete','status')

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name','model_name','price')

class AddressAdmin(admin.ModelAdmin):
	list_display = ('order','customer','address')

admin.site.register(models.Category)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.ShippingAddress, AddressAdmin)
from django.contrib import admin
from .models import Order, Product, Staff, ProductOrder

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Staff)
admin.site.register(ProductOrder)
from django.contrib import admin
from .models import Product, Order, OrderItem, CartItem, Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
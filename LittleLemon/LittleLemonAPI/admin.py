from django.contrib import admin
from .models import Category,MenuItem,Cart,Order,OrderItem
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','slug','title')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display=('id','title','price','featured','category')
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=('id','user','menuitem','quantity','unit_price','price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','user','delivery_crew','status','total','date')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=('id','order','menuitem','quantity','unit_price','price')
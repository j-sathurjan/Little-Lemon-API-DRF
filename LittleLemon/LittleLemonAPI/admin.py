from django.contrib import admin
from .models import Category,MenuItem,Cart,Order,OrderItem
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','slug','title')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display=('id','title','price','featured','category')
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Category,MenuItem,Cart,Order,OrderItem
import bleach
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','slug','title']
    def validate(self, attrs):
        attrs['title']=bleach.clean(attrs['title'])
        return super().validate(attrs)
        
class MenuItemSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    category_id=serializers.IntegerField(write_only=True)
    class Meta:
        model=MenuItem
        fields=['id','title','price','featured','category','category_id']
        validators=[
            UniqueTogetherValidator(queryset=MenuItem.objects.all(), fields=['title','price']),
        ]
        
    def validate(self, attrs):
        attrs['title']=bleach.clean(attrs['title'])
        if attrs['price']<0:
            raise serializers.ValidationError("Price should not be less than 0")
        return super().validate(attrs)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','first_name','last_name']
        
class CartSerializer(serializers.ModelSerializer):
    menuitem=MenuItemSerializer(read_only=True)
    menuitem_id=serializers.IntegerField(write_only=True)
    user=UserSerializer(read_only=True)
    user_id=serializers.IntegerField(write_only=True)
    class Meta:
        model=Cart
        fields=['id','menuitem','menuitem_id','quantity','unit_price','price','user','user_id']
    def validate(self, attrs):
        attrs['menuitem']=bleach.clean(attrs['menuitem'])
        if attrs['price']<0 or attrs['unit_price']<0:
            raise serializers.ValidationError("Price should not be less than 0")
        return super().validate(attrs)
    
class OrderSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    user_id=serializers.IntegerField(write_only=True)
    class Meta:
        model=Order
        fields=['id','user','user_id','delivery_crew','status','total','date']
        
class OrderItemSerializer(serializers.ModelSerializer):
    order=OrderSerializer(read_only=True)
    order_id=serializers.IntegerField(write_only=True)
    menuitem=MenuItemSerializer(read_only=True)
    menuitem_id=serializers.IntegerField(write_only=True)
    class Meta:
        model=OrderItem
        fields=['id','order','order_id','menuitem','menuitem_id','quantity','unit_price','price']
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Category,MenuItem
import bleach
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','slug','title']
        
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
        fields=['username','email']
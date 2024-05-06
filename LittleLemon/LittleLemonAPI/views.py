from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User,Group

# Create your views here.
class MenuItemView(generics.ListCreateAPIView,):
    permission_classes=[IsAuthenticated]
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response({'message':"you are not allowed to create."}, status=403)
        
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=MenuItem.objects.all()
    def update(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return super().update(request, *args, **kwargs)
        else:
            return Response({'message':"you are not allowed to update."}, status=403)
        
    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return super().delete(request, *args, **kwargs)
        else:
            return Response({'message':"you are not allowed to delete."}, status=403)
    serializer_class=MenuItemSerializer

@api_view(['GET'])
def ManagerGroupUserView(request):
    queryset=User.objects.all()
    serializer_class=User
    return Response({'users':{queryset}},200)
    
from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer,UserSerializer
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
    
class ManagerGroupUserView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = UserSerializer
    queryset=User.objects.filter(groups__name='Manager')
    
    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return super().list(request, *args, **kwargs)
        else:
            return Response({'message':"you are not allowed to get."}, status=403)
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            group=Group.objects.filter(name='Manager').all()
            try:
                body=request.data['username']
                user=User.objects.get(username=body)
                user.groups.add(1)
                return Response({"message": "User "+ user.username + " has been added to Manager group"},status=201)
            except:
                return Response({"message":"user not found"},status=404)
        else:
            return Response({'message':"you are not allowed to assign."}, status=403)
    
class ManagerGroupSingleUserView(generics.DestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = UserSerializer
    queryset=User.objects.filter(groups__name='Manager')
    
    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            group=Group.objects.filter(name='Manager').all()
            try:
                param=kwargs.get('pk')
                user=User.objects.get(pk=param)
                user.groups.remove(1)
                return Response({"message":"user "+ user.username +" has been removed from Manager group."},status=200)
            except Exception as e:
                return Response({"message":"User Not Found"},status=404)
        else:
            return Response({'message':"you are not allowed to assign groups."}, status=403)

class DeliveryCrewGroupUserView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = UserSerializer
    queryset=User.objects.filter(groups__name='DeliveryCrew')
    
    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return super().list(request, *args, **kwargs)
        else:
            return Response({'message':"you are not allowed to get."}, status=403)
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            group=Group.objects.filter(name='DeliveryCrew').all()
            try:
                body=request.data['username']
                user=User.objects.get(username=body)
                user.groups.add(2)
                return Response({"message": "User "+ user.username + " has been added to Delivery Crew group"},status=201)
            except:
                return Response({"message":"user not found"},status=404)
        else:
            return Response({'message':"you are not allowed to assign."}, status=403)
class DeliveryCrewGroupSingleUserView(generics.DestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = UserSerializer
    queryset=User.objects.filter(groups__name='DeliveryCrew')
    
    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            group=Group.objects.filter(name='DeliveryCrew').all()
            try:
                param=kwargs.get('pk')
                user=User.objects.get(pk=param)
                user.groups.remove(2)
                return Response({"message":"user "+ user.username +" has been removed from Delivery Crew group."},status=200)
            except Exception as e:
                return Response({"message":"User Not Found"},status=404)
        else:
            return Response({'message':"you are not allowed to assign groups."}, status=403)
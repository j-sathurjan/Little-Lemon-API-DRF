from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem,Cart,Order,OrderItem
from .serializers import MenuItemSerializer,UserSerializer,CartSerializer,OrderItemSerializer,OrderSerializer
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User,Group
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.utils.timezone import localtime

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

class CartView(generics.ListCreateAPIView,generics.DestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CartSerializer
    def get_queryset(self):
        loginUser=self.request.user
        return Cart.objects.filter(user=loginUser)
    
    def create(self, request, *args, **kwargs):
        try:
            cart=Cart()
            cart.user=request.user
            cart.unit_price=request.data['unit_price']
            cart.price=request.data['price']
            cart.menuitem=MenuItem(pk=request.data['menuitem_id'])
            cart.quantity=request.data['quantity']
            cart.save()
            return Response({"menuitem":cart.menuitem.pk,"quantity":cart.quantity,"unit_price":cart.unit_price,"price":cart.price},status=201)
        except:
            return Response({"message":"something went wrong."},status=400)
    def delete(self, request, *args, **kwargs):
        loginUser=request.user
        try:
            cartitem=Cart.objects.filter(user=loginUser).all()
            cartitem.delete()
            return Response({"message":"your cart items deleted."},status=200)
        except:
            return Response({"message":"something went wrong."},status=400)
    
class OrderItemView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OrderItemSerializer
    queryset=OrderItem.objects.all()
    
    def list(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            order=Order.objects.all()
            orderItems=OrderItem.objects.filter(order__in=order)
        elif request.user.groups.filter(name='DeliveryCrew').exists():
            order=Order.objects.filter(delivery_crew=request.user)
            orderItems=OrderItem.objects.filter(order__in=order)
        else:
            order=Order.objects.filter(user=request.user)
            orderItems=OrderItem.objects.filter(order__in=order)
        
        serialized_data = self.serializer_class(orderItems, many=True)
        return Response(serialized_data.data,status=200)
        
    def create(self, request, *args, **kwargs):
        loginUser=request.user
        # orderItem.order=order
        # # menuitem=MenuItem.objects.filter(pk=request.data[menuitem])
        # orderItem.menuitem=request.data['menuitem']
        # orderItem.quantity=request.data['quantity']
        # orderItem.unit_price=request.data['unit_price']
        # orderItem.price=request.data['price']
        # orderItem.save()
        cartItems=Cart.objects.filter(user=loginUser)
        if cartItems.exists():
            order=Order()
            order.user=request.user
            order.total=0
            order.date=localtime().date()
            order.save()
            order.refresh_from_db()
            for items in cartItems:
                orderItem=OrderItem()
                orderItem.order=order
                orderItem.menuitem=items.menuitem
                orderItem.quantity=items.quantity
                orderItem.unit_price=items.unit_price
                orderItem.price=items.price
                orderItem.save()
                order.total+=orderItem.price
                order.save()
            cartItems.delete()
        else:
            return Response({"message":"there are no cart items to order."},status=200)
        return Response({"message":"Your order id:"+str(order.pk)+" has been placed."},status=201)
    
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OrderItemSerializer
    queryset=Order.objects.all()
    def get(self, request, *args, **kwargs):
        order=Order.objects.filter(pk=kwargs.get('pk'))
        if order[0].user==request.user:
            orderitems=OrderItem.objects.filter(order__in=order)
            serialized_data = self.serializer_class(orderitems, many=True)
            return Response(serialized_data.data,status=200)
        else:
            return Response({"message":"you are not allowewd to view this order."},status=403)
    def update(self, request, *args, **kwargs):
        orders=Order.objects.filter(pk=kwargs.get('pk'))
        order=orders[0]
        if request.user.groups.filter(name='Manager'):
            try:
                order.delivery_crew=User.objects.get(username=request.data['delivery_crew'])
                order.status=request.data['status']
                order.save()
                return Response({"message":"your order "+str(order.pk)+" has been updated."},status=200)
            except:
                return Response({"message":"something went wrong."},status=400)
        elif request.user.groups.filter(name='DeliveryCrew'):
            if order.delivery_crew==request.user:
                try:
                    order.status=request.data['status']
                    order.save()
                    return Response({"message":"your order status changed to "+str(order.status)},status=200)
                except:
                    return Response({"message":"somthing went wrong."},status=400)
            else:
                return Response({"message":"you are not allowed to change this order status"},status=403)
        else:
            return Response({"message":"your are not allowed to change order "+ str(order.pk)},status=403)
    def destroy(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"message":"you are not allowed to delete."},status=403)
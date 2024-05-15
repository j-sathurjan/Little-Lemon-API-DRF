from django.urls import path
from LittleLemonAPI import views

urlpatterns = [
    path('menu-items',views.MenuItemView.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItemView.as_view()),
    path('groups/manager/users', views.ManagerGroupUserView.as_view()),
    path('groups/manager/users/<int:pk>',views.ManagerGroupSingleUserView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewGroupUserView.as_view()),
    path('groups/delivery-crew/users/<int:pk>',views.DeliveryCrewGroupSingleUserView.as_view()),
    path('cart/menu-items',views.CartView.as_view()),
    path('orders',views.OrderItemView.as_view()),
    path('orders/<int:pk>',views.SingleOrderView.as_view()),
]

from django.urls import path
from LittleLemonAPI import views

urlpatterns = [
    path('menu-items',views.MenuItemView.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItemView.as_view()),
    path('groups/manager/users', views.ManagerGroupUserView, name="")
]

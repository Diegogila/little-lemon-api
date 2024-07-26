from django.urls import path, include
from .views import *




urlpatterns = [
    path('categories/', CategoryView.as_view(),name='categories'),
    path('categories/<int:pk>', SingleCategoryView.as_view(),name='categories-items'),
    path('menu-items/', MenuItemsView.as_view(),name='menuitems'),
    path('menu-items/<int:pk>', SingleMenuItemView.as_view(),name='single-menuitems'),
    path('groups/manager/users', ManagerUsersView.as_view(), name='manager-users'),
    path('groups/manager/users/<int:user_id>', ManagerUserDetailView.as_view(), name='manager-user-detail'),
    path('groups/delivery-crew/users', DeliveryCrewUsersView.as_view(), name='delivery-crew-users'),
    path('groups/delivery-crew/users/<int:user_id>', DeliveryCrewUserDetailView.as_view(), name='delivery-crew-user-detail'),
    path('cart/menu-items',CartView.as_view(),name='cart'),
    path('orders/',OrderView.as_view(),name='orders'),
    path('orders/<int:pk>', SingleOrderView.as_view(),name='single-orders')
]
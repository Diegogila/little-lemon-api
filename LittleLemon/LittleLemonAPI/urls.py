from django.urls import path
from . import views

urlpatterns = [
    path('categories/<int:pk>', views.CategoryView.as_view()),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItemView.as_view() ),
]

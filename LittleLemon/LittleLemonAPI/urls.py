from django.urls import path, include
from .views import *


urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('category/<int:pk>', SingleCategoryView.as_view()),
    path('menu-items/', MenuItemsView.as_view()),
    path('menu-items/<int:pk>', MenuItemsView.as_view()),

]
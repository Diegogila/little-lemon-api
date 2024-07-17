from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MenuItemViewSet, CartViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'carts', CartViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
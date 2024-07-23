from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.utils import IntegrityError


class IsManagerOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists() or request.user.is_staff
        return True
    
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsManagerOrReadOnly()]

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsManagerOrReadOnly()]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsManagerOrReadOnly()]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsManagerOrReadOnly()]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ManagerUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        managers = User.objects.filter(groups__name='Manager')
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id')
            user = get_object_or_404(User, id=user_id)
            group, created = Group.objects.get_or_create(name='Manager')
            user.groups.add(group)
            return Response({'message': 'User added to Manager'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagerUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, name='Manager')
        user.groups.remove(group)
        return Response({'message': 'User removed from Manager'}, status=status.HTTP_200_OK)

class DeliveryCrewUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        delivery_crew = User.objects.filter(groups__name='Delivery Crew')
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id')
            user = get_object_or_404(User, id=user_id)
            group, created = Group.objects.get_or_create(name='Delivery Crew')
            user.groups.add(group)
            return Response({'message': 'User added to Delivery Crew'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeliveryCrewUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, name='Delivery Crew')
        user.groups.remove(group)
        return Response({'message': 'User removed from Delivery Crew'}, status=status.HTTP_200_OK)

class CartView(APIView):
    permission_classes =[IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        menuitem_id = request.data.get('menuitem_id')
        quantity = int(request.data.get('quantity', 1))
        user_id = request.user.id
        menuitem = get_object_or_404(MenuItem,id=menuitem_id)
        unit_price = menuitem.price
        price = unit_price * quantity

        cart, created = Cart.objects.get_or_create(
            user_id=user_id,
            menuitem=menuitem,
            defaults={'quantity': quantity, 'unit_price': unit_price, 'price': price}
        )

        if not created:
            cart.quantity += quantity
            cart.price += price
            cart.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderView(APIView):
    permission_classes =[IsAuthenticated]

    def get(self, request):
        if request.user.groups.filter(name='Manager').exists():
            order_items = Order.objects.all()
            serializer = OrderSerializer(order_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            order_items = Order.objects.filter(user=request.user)
            serializer = OrderSerializer(order_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) 
    
    def post(self,request):
        menuitems = Cart.objects.filter(user=request.user)
        if not menuitems:
            return Response({"message":"Your cart is empty!"})
        user = request.user.id
        total_order = sum([i.price for i in menuitems])
        date = datetime.now().date()
        order_serializer = OrderSerializer(data={'user':user,'total':total_order,'date':date})
        order_id = ""
        if order_serializer.is_valid():
            saved_order = order_serializer.save()
            order_id = saved_order.id
        else:
            return Response(order_serializer.errors)
        for item in menuitems:
            orderitem_serializer = OrderItemSerializer(data={
                'order':order_id,
                'menuitem':item.menuitem.id,
                'quantity':item.quantity,
                'unit_price':item.unit_price,
                'price':item.unit_price})
            if orderitem_serializer.is_valid():
                order_serializer.save()
            else:
                return Response(orderitem_serializer.errors)
        menuitems.delete()

        return Response(order_serializer.data)
        
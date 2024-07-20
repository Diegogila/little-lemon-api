from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
import datetime


class IsManagerOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_authenticated and request.user.groups.filter(name='Managers').exists()
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
        if not request.user.groups.filter(name='Managers').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        managers = User.objects.filter(groups__name='Managers')
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.groups.filter(name='Managers').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id')
            user = get_object_or_404(User, id=user_id)
            group, created = Group.objects.get_or_create(name='Managers')
            user.groups.add(group)
            return Response({'message': 'User added to Managers'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagerUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        if not request.user.groups.filter(name='Managers').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, name='Managers')
        user.groups.remove(group)
        return Response({'message': 'User removed from Managers'}, status=status.HTTP_200_OK)

class DeliveryCrewUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.groups.filter(name='Managers').exists():
            return Response({'message': 'You are not authorized'}, status=status.HTTP_403_FORBIDDEN)
        delivery_crew = User.objects.filter(groups__name='Delivery Crew')
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.groups.filter(name='Managers').exists():
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
        if not request.user.groups.filter(name='Managers').exists():
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

        serializer = CartSerializer(data={
            'user_id':user_id,
            'menuitem_id':menuitem.id,
            'unit_price':unit_price,
            'quantity': quantity,
            'price':price})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class OrderView(APIView):
    permission_classes =[IsAuthenticated]

    def get(self, request):
        order_items = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    def post(self,request):
        menuitems = Cart.objects.filter(user=request.user)
        user = request.user.id
        total_order = sum([i.price for i in menuitems])
        date = datetime.now()



        return Response({'data':str(total_order)})
        
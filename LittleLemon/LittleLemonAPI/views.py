from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

class CategoryView(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SingleCategoryView(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(APIView):
    queryset = MenuItem.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request,pk):
        if pk:
            item = get_object_or_404(MenuItem, pk=pk)
            serializer = MenuItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            items = MenuItem.objects.all()
            serializer = MenuItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message':'You are not authorized'},status=status.HTTP_403_FORBIDDEN)
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def put(self, request, pk):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message':'You are not authorized'},status=status.HTTP_403_FORBIDDEN)
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message':'You are not authorized'},status=status.HTTP_403_FORBIDDEN)
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MenuItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({'message':'You are not authorized'},status=status.HTTP_403_FORBIDDEN)
        try:
            item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CartView(APIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
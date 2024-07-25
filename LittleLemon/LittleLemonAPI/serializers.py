from rest_framework import serializers
from .models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']


class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ['id','user_id','user','menuitem','menuitem_id','quantity','unit_price','price']

    
class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id','order_id','menuitem','quantity','unit_price','price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True,read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True)
    delivery_crew = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id','user','delivery_crew','delivery_crew_id','status','order_items','total','date']
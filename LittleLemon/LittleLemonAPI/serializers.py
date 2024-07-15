from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    model = Category
    fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):


class CartSerializer(serializers.ModelSerializer):


class OrderSerializer(serializers.ModelSerializer):



class OrderItemSerializer(serializers.ModelSerializer):

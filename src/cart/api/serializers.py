from rest_framework import serializers
from cart.domain.entities import Product, CartItem
from cart.domain.aggregates import Cart


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    calories = serializers.IntegerField()
    expiration_date = serializers.DateTimeField()
    price = serializers.FloatField()


class CartItemSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    total_price = serializers.FloatField(read_only=True)


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    items = serializers.DictField(child=CartItemSerializer())
    total = serializers.FloatField(read_only=True)

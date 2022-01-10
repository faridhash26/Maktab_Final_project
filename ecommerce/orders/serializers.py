from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Order , OrderItem
from users.models import CustomUser
from products.models import Product

class OrderItemSeriailizer(serializers.ModelSerializer):
    # product = serializers.IntegerField(source="product.id")
    # product_name= serializers.CharField(source= "product.name")
    class Meta:
        model = OrderItem
        fields=["product" ,"qty" ]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    order_of_orderitem=OrderItemSeriailizer(  many=True)
    customer= serializers.IntegerField(source='customer.id', read_only=True)
    class Meta:
        model=Order
        fields=['id','customer','order_of_orderitem']

    def create(self, validated_data):
        order_items = validated_data.pop('order_of_orderitem')
        order = Order.objects.create(customer=self.context['request'].user)
        for order_item  in order_items:
            OrderItem.objects.create(order=order,**order_item)
        return order

class UpdateOrderItem(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields= ["product" ,"qty" ]

    def create(self, validated_data):
        order = get_object_or_404(Order,id = self.context['view'].kwargs.get('pk'))
        oreder_item = OrderItem.objects.create(order=order,**validated_data)
        prodcut =get_object_or_404(Product, id =oreder_item.product.id)
        if (prodcut.stock - oreder_item.qty) >=0:
            prodcut.stock=prodcut.stock-oreder_item.qty
            prodcut.save()
        return oreder_item


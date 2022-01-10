from django.db.models import fields
from rest_framework import serializers
from .models import Shop
from products.models import Product ,Tag

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields=["id","shop_type" , "name" ,"address" ,"slug"]













class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        try:
            if "from_price" in self.context['request'].query_params:
                data = data.filter(price__gte=self.context['request'].query_params['from_price'])
            if "to_price" in self.context['request'].query_params:
                data = data.filter(price__lte=self.context['request'].query_params['to_price'])
            if "is_stock" in self.context['request'].query_params:
                if self.context['request'].query_params['is_stock'] =="True":
                    data = data.filter(stock__gt=0)
            if "tag" in self.context['request'].query_params:       
                print('tag')
                data = data.filter(tag__title=self.context['request'].query_params['tag'])
        except:
            return super(FilteredListSerializer, self).to_representation(data)

        return super(FilteredListSerializer, self).to_representation(data)






class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields=["title"]




class ProductSerializer(serializers.ModelSerializer):
    tag = ProductSerializer(many=True)
    class Meta:
        list_serializer_class = FilteredListSerializer

        model=Product
        fields=["id" , "name" , "price" , "stock" , "weight" ,"tag"]



class ProductOfShop(serializers.ModelSerializer):
    products = ProductSerializer( source="product_shop",many=True , read_only=True)
    class Meta:
        model=Shop
        fields=["id","shop_type" , "name" ,"products"]
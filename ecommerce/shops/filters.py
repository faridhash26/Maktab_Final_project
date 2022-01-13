from django.db.models import fields
import django_filters
from .models import Shop

class ShopFilter(django_filters.FilterSet):
    class Meta:
        model = Shop
        fields = ['shop_type']

class PruductOfShopFilter(django_filters.FilterSet):
    class Meta:
        model= Shop
        fields=["product_shop__tag" , "product_shop__price"]
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import generics

from shops.filters import ShopFilter,PruductOfShopFilter
from shops.serializers import ShopSerializer,ProductOfShopSeializer, ShopType,ProductOfShopSWaggerSeializer
from shops.models import Shop


class ListOfShopsForCustomer(generics.ListAPIView):
    serializer_class = ShopSerializer
    filterset_class = ShopFilter
    model=Shop

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        return queryset

class TypeOfShops(generics.ListAPIView):
    serializer_class = ShopType
    model=Shop
    def get_queryset(self):
        queryset = self.model.objects.distinct('shop_type')
        return queryset


class ProductOfShop(generics.RetrieveAPIView):
    model=Shop
    serializer_class = ProductOfShopSeializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'shop_slug'
    queryset=Shop.objects.all()

    @swagger_auto_schema(responses={"200": ProductOfShopSWaggerSeializer})
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


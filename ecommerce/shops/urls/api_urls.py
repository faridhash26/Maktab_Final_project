from django.urls import path
from shops.views import api_views as views

urlpatterns = [
    path('listofshops/api/' ,views.ListOfShopsForCustomer.as_view() , name="list_of_shops"),
    path('list/type/shops/' ,views.TypeOfShops.as_view() , name='type_of_shops'),
    path('shop/<slug:shop_slug>/product/',views.ProductOfShop.as_view() , name="product_of_shop"),
]
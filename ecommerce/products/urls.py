from django.urls import path
from .views import ProductsOfShop


app_name = 'products'
urlpatterns = [
    path('list/<slug:slug>/' ,ProductsOfShop.as_view()  ,name="list_product_of_shop" ),
    # path('delete_product/<int:shoptid>/' ,DeleteShop.as_view()  ,name="delete_shop_admin" ),

]
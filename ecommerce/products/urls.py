from django.urls import path
from .views import EditProduct, ProductsOfShop,ConfirmDeleteProduct,DeleteProduct,CreateProduct


app_name = 'products'
urlpatterns = [
    path('list/<slug:slug>/' ,ProductsOfShop.as_view()  ,name="list_product_of_shop" ),
    path('conform_delete_product/<slug:slug>/' ,ConfirmDeleteProduct.as_view()  ,name="conform_delete_Product_admin" ),
    path('delete_product/<slug:slug>/' ,DeleteProduct.as_view()  ,name="delete_Product_admin" ),
    path('edit_product/<slug:slug>/' ,EditProduct.as_view()  ,name="edit_product_admin" ),
    path('new_product/<slug:slug>/' ,CreateProduct.as_view()  ,name="new_product_admin" ),

]
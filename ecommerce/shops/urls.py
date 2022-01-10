from os import name
from django.urls import path
from . import views


app_name = 'shops'
urlpatterns = [
    path('dashboard/' ,views.DashboardView.as_view()  ,name="dashboard_admin" ),
    path('dashboard/conform_delete_shop/<slug:slug>/' ,views.RenderConfirmDeleteShop.as_view()  ,name="confirm_delete_shop_admin" ),
    path('dashboard/delete_shop/<slug:slug>/' ,views.RenderDeleteShop.as_view()  ,name="delete_shop_admin" ),
    path('dashboard/create_shop/' ,views.CreateShop.as_view()  ,name="create_shop" ),
    path('dashboard/edit_shop/<slug:slug>/' ,views.EditShop.as_view()  ,name="edit_shop" ),
    path('listofshops/api/' ,views.ListOfShopsForCustomer.as_view() , name="list_of_shops"),
    path('shop/<slug:shop_slug>/product/',views.ProductOfShop.as_view() , name="product_of_shop"),
]
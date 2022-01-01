from django.urls import path
from .views import DashboardView ,RenderDeleteShop,RenderConfirmDeleteShop ,CreateShop


app_name = 'shops'
urlpatterns = [
    path('dashboard/' ,DashboardView.as_view()  ,name="dashboard_admin" ),
    path('dashboard/conform_delete_shop/<slug:slug>/' ,RenderConfirmDeleteShop.as_view()  ,name="confirm_delete_shop_admin" ),
    path('dashboard/delete_shop/<slug:slug>/' ,RenderDeleteShop.as_view()  ,name="delete_shop_admin" ),
    path('dashboard/create_shop/' ,CreateShop.as_view()  ,name="create_shop" ),


]
from django.urls import path
from .views import DashboardView ,RenderDeleteShop


app_name = 'shops'
urlpatterns = [
    path('dashboard/' ,DashboardView.as_view()  ,name="dashboard_admin" ),
    path('dashboard/conform_delete_shop/<slug:slug>/' ,RenderDeleteShop.as_view()  ,name="delete_shop_admin" ),

]
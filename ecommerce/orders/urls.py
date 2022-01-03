from django.urls import path
from .views import ListOfOrders,ListOfOrderItems

app_name = 'orders'
urlpatterns = [
    path('reports/' ,ListOfOrders.as_view()  ,name="the_orders" ),
    path('reports/order_items/<int:oreder_id>/' ,ListOfOrderItems.as_view()  ,name="order_item_list" ),

]
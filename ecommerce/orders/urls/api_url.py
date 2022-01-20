from django.urls import path
from orders.views import api_view as views

urlpatterns = [
    path('order/' , views.CreateOrderByCustomer.as_view() , name="new_order_api" ),
    path('update/order/<int:pk>/'  ,views.UpdateTheOrderItem.as_view() , name="updating_order_item" ),
    path('delete/order/<int:order_id>/orderitem/<int:orderitem_id>/' ,views.DeleteOrderItem.as_view() , name="delete_order_item" ),
    path('paying/order/<int:order_id>/' , views.Paymentview.as_view() , name="paying_order"),
    path('order/processing/' ,views.ListOfProcessingOrderMethod.as_view() , name="list_processing"),
    path('order/paid/' ,views.ListOfPaid.as_view() ,name="paid_list"),
]
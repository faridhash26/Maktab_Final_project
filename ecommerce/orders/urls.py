from django.urls import path
from .views import ListOfOrders,ListOfOrderItems,ChangeOrderStatus,ConformCancelOrderItem,CancelOrderItem,RenderReportSalesPage,ReportSales
from . import views
app_name = 'orders'
urlpatterns = [
    path('reports/' ,ListOfOrders.as_view()  ,name="the_orders" ),
    path('reports/order_items/<int:oreder_id>/' ,ListOfOrderItems.as_view()  ,name="order_item_list" ),
    path('reports/order_items/change_status/<int:pk>' ,ChangeOrderStatus.as_view()  ,name="change_order_status" ),
    path('delete_order_item/conform/<int:pk>/',ConformCancelOrderItem.as_view() , name="conform_delete_order_item"),
    path('delete_order/<int:orderitem_id>/' ,CancelOrderItem.as_view() , name='delete_oreder_item'),
    path('render/report_orders/' ,RenderReportSalesPage.as_view() , name="render_report_orders"),
    path('report_order/'  , ReportSales.as_view() , name="orders_reports"),
    path('api/order/' , views.CreateOrderByCustomer.as_view() , name="new_order_api" ),
    path('api/update/order/<int:pk>/'  ,views.UpdateTheOrderItem.as_view() , name="updating_order_item" ),
    path('api/delete/order/<int:order_id>/orderitem/<int:orderitem_id>/' ,views.DeleteOrderItem.as_view() , name="delete_order_item" ),
    path('api/paying/order/<int:order_id>/' , views.Paymentview.as_view() , name="paying_order"),
    path('api/order/processing/' ,views.ListOfProcessingOrderMethod.as_view() , name="list_processing"),
    path('api/order/paid/' ,views.ListOfPaid.as_view() ,name="paid_list"),

]
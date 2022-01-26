from django.urls import path
from orders.views import template_view as view

app_name = 'orders'
urlpatterns = [
    path('reports/' ,view.ListOfOrders.as_view()  ,name="the_orders" ),
    path('reports/order_items/<int:oreder_id>/' ,view.ListOfOrderItems.as_view()  ,name="order_item_list" ),
    path('reports/order_items/change_status/<int:pk>' ,view.ChangeOrderStatus.as_view()  ,name="change_order_status" ),
    path('delete_order_item/conform/<int:pk>/',view.ConformCancelOrderItem.as_view() , name="conform_delete_order_item"),
    path('delete_order/<int:orderitem_id>/' ,view.CancelOrderItem.as_view() , name='delete_oreder_item'),
    path('render/report_orders/' ,view.RenderReportSalesPage.as_view() , name="render_report_orders"),
    path('report_order/'  , view.ReportSales.as_view() , name="orders_reports"),
]
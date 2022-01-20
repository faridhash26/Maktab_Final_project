import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.db.models.functions import TruncDate
from django.db.models import Sum,Count,Max
from django.contrib import messages
from django.urls import reverse

from orders.models import Order,OrderItem




class ListOfOrders(LoginRequiredMixin, View):
    """
    list o f orders in admin panel 
    """
    def get(self, request, *args, **kwargs):
        """
        list of all orders
        """
        today = str(datetime.date.today())
        parsed_fromdate=today.split("-")
        from_date=str(datetime.datetime(int(parsed_fromdate[0]) ,int(parsed_fromdate[1]),int(parsed_fromdate[2])).date())
        to_date=str(datetime.datetime(int(parsed_fromdate[0]) ,int(parsed_fromdate[1]),int(parsed_fromdate[2])).date())   

        orderlist = Order.objects.filter(order_of_orderitem__product__shop__author=request.user.id).values(
            'id','createdAt', 'order_of_orderitem__product__shop__name', 'status', 'customer__username').order_by('-createdAt').distinct()

        return render(request, 'adminshop/pages/orders_list.html', {'order_list': orderlist,"from_date":from_date,"to_date":to_date })

    def post(self, request, *args, **kwargs):
        """
        filtering the list of orders
        """
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        status = request.POST.get('option')

        parsed_fromdate=fromdate.split("-")
        parsed_todate=todate.split("-")
        orderlist = Order.objects.filter(order_of_orderitem__product__shop__author=request.user.id )

        if fromdate:
            from_date=datetime.datetime(int(parsed_fromdate[0]) ,int(parsed_fromdate[1]),int(parsed_fromdate[2])).date()
            orderlist = orderlist.filter(createdAt__gte=from_date)

        if  todate:
            to_date=datetime.datetime(int(parsed_todate[0]) ,int(parsed_todate[1]),int(parsed_todate[2])).date()   
            orderlist=orderlist.filter(createdAt__lte=to_date)
        
        if status:
            orderlist=orderlist.filter(status=status )

        orderlist=orderlist.values(
            'id', 'createdAt','order_of_orderitem__product__shop__name', 'status', 'customer__username').order_by('-createdAt').distinct()

        return render(request, 'adminshop/pages/orders_list.html', {'order_list': orderlist ,"from_date":fromdate,"to_date":todate })


class ListOfOrderItems(LoginRequiredMixin, ListView):
    """
    list of order items by each order 
    """
    template_name = "adminshop/pages/order_items.html"

    def get_queryset(self):
        return OrderItem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = get_object_or_404(Order, id=self.kwargs.get('oreder_id'))

        context['order_item_list'] = OrderItem.objects.filter(order=obj ,product__shop__author__id = self.request.user.id).values(
            'product__name', 'qty', 'price', 'product__image' ,'id' )
        return context


class ChangeOrderStatus(LoginRequiredMixin, UpdateView):
    """
    changing the status of order
    """
    template_name = "adminshop/forms/change_shop_status.html"
    model = Order
    success_url =reverse_lazy("orders:the_orders")
    fields = [
        "status",
    ]


class ConformCancelOrderItem(LoginRequiredMixin, DetailView):
    template_name = "adminshop/pages/cancelproduct.html"
    model = OrderItem
    context_object_name="orderitem"


class CancelOrderItem(LoginRequiredMixin ,DeleteView):
    model = OrderItem
    success_url=reverse_lazy("orders:the_orders")
    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(OrderItem , id =kwargs["orderitem_id"]).delete()
        messages.warning(request, f'order item successfuly deleted')
        return redirect(reverse('orders:the_orders')) 
    




from django.db.models import Sum
from django.http import JsonResponse



class RenderReportSalesPage(LoginRequiredMixin ,View):
    model=Order

    def get(self, request, *args, **kwargs):
        listof_orders=[]
        orderlist = Order.objects.filter(order_of_orderitem__product__shop__author=request.user.id ,status="PD").distinct().annotate(the_customer=Count("customer") ).values("customer__username" ,"customer__id", "the_customer" )
        for order in orderlist:
            obj=Order.objects.filter(order_of_orderitem__product__shop__author=request.user.id ,status="PD" , customer = order["customer__id"] ).distinct().aggregate(last_purchase = Max("updated_at") , total_purchase=Sum("totalPrice") , Count_product=Count("order_of_orderitem"))
            listof_orders.append({
                "customer__username":order["customer__username"],
                "count_order":order["the_customer"],
                "last_purchase":obj["last_purchase"],
                "total_purchase":obj["total_purchase"],
                "Count_product":obj["Count_product"]
            })
        return render(request, 'adminshop/pages/reports_sales.html' ,{"reports":listof_orders} )



class ReportSales(LoginRequiredMixin ,View):
    def get(self, request, *args, **kwargs):

        labels = []
        data = []
        obj = Order.objects.annotate(day= TruncDate('updated_at')).values('day').annotate(sales = Sum('totalPrice') , days=Count('day') ).values('sales' ,'day')
        for entry in obj :
            labels.append(entry["day"])
            data.append(entry["sales"])


        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })


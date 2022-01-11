import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import TruncDate
from django.db.models import Sum,Count

from .serializers import OrderSerializer, PaymentShopSerializer,UpdateOrderItem
from products.models import Product
# Create your views here.


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
        from_date=str(datetime.datetime(int(parsed_fromdate[0]) ,int(parsed_fromdate[2]),int(parsed_fromdate[1])).date())
        to_date=str(datetime.datetime(int(parsed_fromdate[0]) ,int(parsed_fromdate[2]),int(parsed_fromdate[1])).date())   

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
        return render(request, 'adminshop/pages/reports_sales.html' )



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





# ===============
# api
# ===============
class CreateOrderByCustomer(generics.CreateAPIView):
    model = Order
    permission_classes = (IsAuthenticated,)
    serializer_class=OrderSerializer



class UpdateTheOrderItem(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=UpdateOrderItem
    model = OrderItem

class DeleteOrderItem(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    model = OrderItem

    def destroy(self, request, *args, **kwargs):

        order_of_item=  get_object_or_404(OrderItem , id =kwargs["orderitem_id"])
        if order_of_item.order.status == 'PS':
            the_product = get_object_or_404(Product ,id= order_of_item.product.id)
            the_product.stock = the_product.stock +order_of_item.qty
            the_product.save()
            order_of_item.delete()

            try:
                order_items_count= OrderItem.objects.filter(order=kwargs["order_id"]).count()
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            if order_items_count==0:
                Order.objects.get(id =kwargs["order_id"]).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response( {"error":"you can just delete item when status is processing!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

from django.db.models import Sum
from decimal import *


class Paymentview(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    model=Order
    queryset=Order.objects.all()
    lookup_field="id"
    lookup_url_kwarg="order_id"
    serializer_class=PaymentShopSerializer

    def put(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(pk = kwargs["order_id"])
        except:
            return Response(  status=status.HTTP_404_NOT_FOUND)

        total_price =  OrderItem.objects.filter(order=order.id).aggregate(Sum('price'))       
        if order.status  == "PS":
            order.status = 'PD'
            if order.taxPrice:
                order.totalPrice = total_price["price__sum"]+order.taxPrice
            else:
                order.totalPrice = total_price["price__sum"]
            order.save()
            
            return self.update(request, *args, **kwargs)
        return Response(  {"error" :"you dont have permision to payment !"},status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ListOfProcessingOrderMethod(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=PaymentShopSerializer
    queryset = Order.objects.filter(status="PS")
    model=Order


class ListOfPaid(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=PaymentShopSerializer
    queryset = Order.objects.filter(status="PD")
    model=Order
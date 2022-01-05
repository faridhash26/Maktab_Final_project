from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.utils.dateparse import parse_date
import datetime

from .models import Order, OrderItem

# Create your views here.


class ListOfOrders(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        today = str(datetime.date.today())
        parsed_fromdate=today.split("-")
        from_date=str(datetime.datetime(int(parsed_fromdate[0]) ,int(parsed_fromdate[2]),int(parsed_fromdate[1])).date())
        to_date=str(datetime.datetime(int(parsed_fromdate[0]) ,int(parsed_fromdate[2]),int(parsed_fromdate[1])).date())   

        orderlist = Order.objects.filter(order_of_orderitem__product__shop__author=request.user.id).values(
            'id','createdAt', 'order_of_orderitem__product__shop__name', 'status', 'customer__username').order_by('createdAt')

        return render(request, 'adminshop/pages/orders_list.html', {'order_list': orderlist,"from_date":from_date,"to_date":to_date })

    def post(self, request, *args, **kwargs):
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        status = request.POST.get('option')

        parsed_fromdate=fromdate.split("-")
        parsed_todate=todate.split("-")

        from_date=datetime.datetime(int(parsed_fromdate[0]) ,int(parsed_fromdate[1]),int(parsed_fromdate[2])).date()
        to_date=datetime.datetime(int(parsed_todate[0]) ,int(parsed_todate[1]),int(parsed_todate[2])).date()   
        
        orderlist = Order.objects.filter(order_of_orderitem__product__shop__author=request.user.id,status=status ,createdAt__gte=from_date,createdAt__lte=to_date ).values(
            'id', 'createdAt','order_of_orderitem__product__shop__name', 'status', 'customer__username').order_by('createdAt')

        return render(request, 'adminshop/pages/orders_list.html', {'order_list': orderlist ,"from_date":fromdate,"to_date":todate })


class ListOfOrderItems(LoginRequiredMixin, ListView):
    template_name = "adminshop/pages/order_items.html"

    def get_queryset(self):
        return OrderItem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = get_object_or_404(Order, id=self.kwargs.get('oreder_id'))

        context['order_item_list'] = OrderItem.objects.filter(order=obj).values(
            'product__name', 'qty', 'price', 'product__image')
        return context

# class ChangeOrderStatus (LoginRequiredMixin,updateview):
#     pass
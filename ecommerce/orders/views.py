from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from .models import Order, OrderItem

# Create your views here.


class ListOfOrders(LoginRequiredMixin, ListView):
    template_name = "adminshop/pages/orders_list.html"

    def get_queryset(self):
        return Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_list'] = Order.objects.filter(order_of_orderitem__product__shop__author=self.request.user.id).values(
            'id','order_of_orderitem__product__shop__name', 'status', 'customer__username').order_by('createdAt')
        return context


class ListOfOrderItems(LoginRequiredMixin, ListView):
    template_name = "adminshop/pages/order_items.html"

    def get_queryset(self):
        return OrderItem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj= get_object_or_404(Order,id = self.kwargs.get('oreder_id'))

        context['order_item_list'] = OrderItem.objects.filter(order=obj).values(
            'product__name','qty', 'price' , 'product__image')
        return context

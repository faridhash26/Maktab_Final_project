from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product
from shops.models import Shop
# Create your views here.

class ProductsOfShop(LoginRequiredMixin, ListView):
    template_name = "adminshop/pages/productslist.html"


    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_name']= Shop.objects.get(slug=self.kwargs['slug'])
        context['product_list'] = Product.objects.filter(shop__slug= self.kwargs['slug'] )

        return context
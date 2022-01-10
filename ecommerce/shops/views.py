from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from django.views.generic import UpdateView ,DetailView,FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from rest_framework import generics
from rest_framework.response import Response

from .serializers import ShopSerializer,ProductOfShop, ShopType
from .filters import ShopFilter,PruductOfShopFilter
from .forms import CreateShopForm
from .models import Shop
from django.views.generic.edit import CreateView

# Create your views here.


class DashboardView(LoginRequiredMixin, ListView):
    """
    the first page of dashboard in panel admin 
    showing the list of shops for user
    """
    template_name = "adminshop/pages/shopslist.html"

    def get_queryset(self):
        return Shop.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.objects.filter(author= self.request.user.id , is_delete=False)
        # context['shop_list'] = Shop.objects.all()
        # print( 'the user ', self.request.user)
        return context

class RenderConfirmDeleteShop(LoginRequiredMixin,DetailView):
    """
    showing conform pasge for deleting shop
    """
    model=Shop
    template_name = "adminshop/pages/conform_deleteshop.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop_detail"] =get_object_or_404(Shop,slug=self.kwargs['slug'] )
        return context

class RenderDeleteShop(LoginRequiredMixin,UpdateView):
    """
    deleting shop
    """
    model=Shop
    def get(self, request, *args, **kwargs):
        object = get_object_or_404(Shop,slug=self.kwargs['slug'])
        if object:
            object.is_delete=True
            object.save()
            return redirect(reverse('shops:dashboard_admin'))


class CreateShop(LoginRequiredMixin,View):
    """
    createing the new shop
    """
    form_class = CreateShopForm
    template_name="adminshop/forms/create_shop.html"
    
    def get(self, request):
        form = CreateShopForm()
        return render(request, 'adminshop/forms/create_shop.html',{'form': form})

    def post(self, request):
        obj = Shop.objects.filter(is_active=False ,author=request.user).count()
        if obj>0:
            messages.warning(request, f'you have an unaccepted shop.  this shop must be activated then you can create new shop !')
            return redirect(reverse('shops:dashboard_admin'))
        form = CreateShopForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect(reverse('shops:dashboard_admin'))


class EditShop(LoginRequiredMixin,UpdateView):
    """
    edting the shop info 
    """
    model = Shop    
    form_class=CreateShopForm
    template_name="adminshop/forms/edit_shop.html"
    success_url ="/shop/dashboard/"



class ListOfShopsForCustomer(generics.ListAPIView):
    serializer_class = ShopSerializer
    filterset_class = ShopFilter
    model=Shop

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        return queryset

class TypeOfShops(generics.ListAPIView):
    serializer_class = ShopType
    model=Shop
    def get_queryset(self):
        queryset = self.model.objects.distinct('shop_type')
        return queryset


class ProductOfShop(generics.RetrieveAPIView):
    model=Shop
    serializer_class = ProductOfShop
    lookup_field = 'slug'
    lookup_url_kwarg = 'shop_slug'
    queryset=Shop.objects.all()


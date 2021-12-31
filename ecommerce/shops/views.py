from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic import UpdateView ,DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import Shop

# Create your views here.


class DashboardView(LoginRequiredMixin, ListView):
    template_name = "adminshop/pages/shopslist.html"

    def get_queryset(self):
        return Shop.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.objects.filter(author= self.request.user.id , is_delete=False)
        # context['shop_list'] = Shop.objects.all()
        # print( 'the user ', self.request.user)
        return context

class RenderDeleteShop(LoginRequiredMixin,DetailView):
    model=Shop
    template_name = "adminshop/pages/conform_deleteshop.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop_detail"] =get_object_or_404(Shop,slug=self.kwargs['slug'] )
        return context

from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView ,DetailView,DeleteView
from django.urls import reverse

from .forms import CreateProductForm

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
        context['product_list'] = Product.objects.filter(shop__slug= self.kwargs['slug']  )

        return context



class ConfirmDeleteProduct(LoginRequiredMixin,DetailView):
    model=Product
    template_name = "adminshop/pages/conform_delete_product.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_detail"] =get_object_or_404(Product,slug=self.kwargs['slug'] )
        return context

class DeleteProduct(LoginRequiredMixin,DeleteView):
    model=Product
    success_url ="shops:dashboard_admin"
    def get(self, request, *args, **kwargs):
        get_object_or_404(Product,slug=self.kwargs['slug']).delete()
        return redirect(reverse('shops:dashboard_admin')) 


class EditProduct(LoginRequiredMixin,UpdateView):
    model = Product    
    form_class=CreateProductForm
    template_name="adminshop/forms/edit_product.html"
    success_url ="/shop/dashboard/"

class CreateProduct(LoginRequiredMixin,CreateView):
    model = Product
    form_class=CreateProductForm
    template_name="adminshop/forms/create_product.html"
    success_url ="/shop/dashboard/"

    def get(self, request, *args, **kwargs):
        print('the kwargs ',kwargs)
        print('***********************************')
        obj = get_object_or_404(Shop ,slug=kwargs["slug"])
        form = CreateProductForm()
        return render(request, 'adminshop/forms/create_product.html',{'form': form , 'shop_slug':obj})

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Shop ,slug=kwargs["slug"])

        form = CreateProductForm(request.POST)
        if form.is_valid():
            form.instance.shop = obj
            form.save()
            return redirect(reverse('products:list_product_of_shop',kwargs={'slug': obj.slug}))
  
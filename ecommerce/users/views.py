from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView, View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from .models import CustomUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.


class LoginView(View):
    template_name='adminshop/forms/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('users:dashboard_admin'))

        return render(request, 'adminshop/forms/login.html')

    def post(self,request):
        theuser=get_object_or_404(CustomUser , username=request.POST.get('username') )
        print('the user type',theuser.user_type)
        if theuser:
            if theuser.user_type == 'SL':
                user = authenticate(username=request.POST.get('username'), password=request.POST.get('pass'))
                if user is not None:
                    login(request, user)
                    return redirect(reverse('users:dashboard_admin'))
            
        print(request.POST.get('username'))
        print(request.POST.get('pass'))
        
        return render(request, 'adminshop/forms/login.html')


class RegisterView(View):
    pass


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('users:login_suplier'))



class DashboardView(LoginRequiredMixin,TemplateView):
    template_name="adminshop/base.html"





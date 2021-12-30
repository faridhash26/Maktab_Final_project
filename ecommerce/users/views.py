from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse


# Create your views here.
class LoginView(View):
    template_name='adminshop/forms/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            #return redirect(reverse('users:login_dashboard'))
            return HttpResponse('dashbord')

        return render(request, 'adminshop/forms/login.html')

    def post(self,request):
        print(request.POST.get('username'))
        print(request.POST.get('pass'))
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('pass'))
        if user is not None:
            login(request, user)
            return HttpResponse('hi user')
        return render(request, 'adminshop/forms/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('users:login_suplier'))


from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .forms import RegisterForm, UpdateProfileUserForm
from .models import CustomUser
from django.views.generic.edit import CreateView, UpdateView

# Create your views here.


class LoginView(View):
    """
    rendering the login page and user can login 
    """

    template_name = 'adminshop/forms/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('shops:dashboard_admin'))

        return render(request, 'adminshop/forms/login.html')

    def post(self, request):
        try:
            theuser = get_object_or_404(
            CustomUser, username=request.POST.get('username'))
        except:
            messages.warning(request, f'User or password is wrong !')
            theuser=''
            
        
        if theuser:
            if theuser.user_type == 'SL':
                user = authenticate(username=request.POST.get(
                    'username'), password=request.POST.get('pass'))
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome {user}')
                    return redirect(reverse('shops:dashboard_admin'))
                else:
                    messages.warning(request, f'User or password is wrong !')
                    return redirect(reverse('users:login_suplier'))
            else:
                messages.warning(request, f'Just supliers can login ')
                return redirect(reverse('users:login_suplier'))
        else:
        
            return redirect(reverse('users:login_suplier'))


class RegisterView(CreateView):
    """
    
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('shops:dashboard_admin'))
        return render(request, 'adminshop/forms/register.html')

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password2']==form.cleaned_data['password']:
                user = CustomUser.objects.create_user(form.cleaned_data['email'],form.cleaned_data['password'],username=form.cleaned_data['username'] ,phone=form.cleaned_data['phone'],user_type="SL")
                messages.success(request, f'Successfuly registerd')
                return redirect(reverse('users:login_suplier'))
            else:
                messages.warning(request, f'Passwords is wrong!')        
                return redirect(reverse('users:register_admin'))

        messages.warning(request, f'The fields is wrong')        
        return redirect(reverse('users:register_admin'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('users:login_suplier'))


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = "adminshop/pages/admin_profile.html"
   

class UpdateUserProfile(LoginRequiredMixin,UpdateView):
    template_name="adminshop/forms/update_profile_admin.html"
    success_url =reverse_lazy("users:admin_profile")
    form_class=UpdateProfileUserForm
    model= CustomUser

    def get_object(self, queryset=None):
        return self.request.user
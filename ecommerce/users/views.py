from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import generics,permissions
from .serializers import  UserSerializer,UserSerializerProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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

# =====================
# api
# =====================


class RegisterAPI(generics.CreateAPIView):
    model = CustomUser
    
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        if request.data["password"] == request.data["password2"]:
            serializer = self.get_serializer(data=request.data)
            isvalid =serializer.is_valid(raise_exception=True)
            if isvalid:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response({"Success": "user successfuly registered."}, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"message": "your field is worng."}, status=status.HTTP_400_BAD_REQUEST )

    

class LoginCustomer(APIView):
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]

    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
             return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)


        user = authenticate(username=request.data.get(
                    'username'), password=request.data.get('password'))
        if user is not None and user.user_type=="CT":
            refresh = RefreshToken.for_user(user)

            return Response({'msg': 'Login Success','access':str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutApiView(APIView):
    def get(self, request):
        logout(request)

        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)




class ProfileCustomerApi(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)    
    serializer_class = UserSerializerProfile
    lookup_field = 'id'
    
    def get_object(self):
        return  get_object_or_404(CustomUser, id=self.kwargs["id"])

  



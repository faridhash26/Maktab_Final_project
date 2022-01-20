from django.urls import path
from users.users_views import api_view as views

app_name = 'users_api'
urlpatterns = [
    path('register/' ,views.RegisterAPI.as_view() , name='register_api' ),
    path('login/',views.LoginCustomer.as_view(),name='login_api'),
    path('profile/' ,views.ProfileCustomerApi.as_view() , name="profile_api_view"),
    path('activate/phone/', views.ActivateUserPhone.as_view() ,name="activate_user"),
    path('generate_otp/' , views.GenerateOtpForLogin.as_view() , name="generate_otp_login"),
    path('otp_login/' , views.LoginWithOtp.as_view() , name="login_with_otp")
]
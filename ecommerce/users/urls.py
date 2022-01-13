from django.urls import path
from . import views
app_name = 'users'

urlpatterns = [
        path('', views.LoginView.as_view(), name='login_suplier'),
        path('register/' ,views.RegisterView.as_view()  ,name="register_admin" ),
        path('logout/' ,views.LogoutView.as_view()  ,name="logout_admin" ),
        path('userprofile/' ,views.UserProfile.as_view()  ,name="admin_profile" ),
        path('userprofile/update/' ,views.UpdateUserProfile.as_view()  ,name="update_admin_profile" ),
        path('register/api/' ,views.RegisterAPI.as_view() , name='register_api' ),
        path('login/api/',views.LoginCustomer.as_view(),name='login_api'),
        path('profile/api/' ,views.ProfileCustomerApi.as_view() , name="profile_api_view"),
]
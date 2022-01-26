from django.urls import path
from users.users_views import template_views as views

app_name = 'users'
urlpatterns = [
        path('', views.LoginView.as_view(), name='login_suplier'),
        path('register/' ,views.RegisterView.as_view()  ,name="register_admin" ),
        path('logout/' ,views.LogoutView.as_view()  ,name="logout_admin" ),
        path('userprofile/' ,views.UserProfile.as_view()  ,name="admin_profile" ),
        path('userprofile/update/' ,views.UpdateUserProfile.as_view()  ,name="update_admin_profile" ),   
]
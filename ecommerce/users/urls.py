from django.urls import path
from .views import LoginView,LogoutView ,RegisterView ,UserProfile,UpdateUserProfile

app_name = 'users'
urlpatterns = [
        path('', LoginView.as_view(), name='login_suplier'),
        path('register/' ,RegisterView.as_view()  ,name="register_admin" ),
        path('logout/' ,LogoutView.as_view()  ,name="logout_admin" ),
        path('userprofile/' ,UserProfile.as_view()  ,name="admin_profile" ),
        path('userprofile/update/' ,UpdateUserProfile.as_view()  ,name="update_admin_profile" )


]
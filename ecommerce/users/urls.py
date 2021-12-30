from django.urls import path
from .views import LoginView,LogoutView
app_name = 'users'
urlpatterns = [
        path('', LoginView.as_view(), name='login_suplier'),
        path('logout/' ,LogoutView.as_view()  ,name="logout_admin" )
]
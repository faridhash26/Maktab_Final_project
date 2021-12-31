from django.urls import path
from .views import LoginView,LogoutView ,RegisterView ,DashboardView

app_name = 'users'
urlpatterns = [
        path('', LoginView.as_view(), name='login_suplier'),
        path('logout/' ,LogoutView.as_view()  ,name="logout_admin" ),
        path('register/' ,RegisterView.as_view()  ,name="register_admin" ),
        path('dashboard/' ,DashboardView.as_view()  ,name="dashboard_admin" ),
        path('redirect/' ,DashboardView.as_view()  ,name="redirect_admin" )
]
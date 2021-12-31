from django.urls import path
from .views import DashboardView


app_name = 'shops'
urlpatterns = [
    path('dashboard/' ,DashboardView.as_view()  ,name="dashboard_admin" ),

]
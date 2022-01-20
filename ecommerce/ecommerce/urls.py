"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
    path('', include('users.urls.template_urls')),
    path('user/v1/api/', include('users.urls.api_url')),
    path('blog/', include('post.urls')),
    path('shop/', include('shops.urls.template_urls')),
    path('shop/v1/api/' ,  include('shops.urls.api_urls')),
    path('product/', include('products.urls')),
    path('order/', include('orders.urls.template_url')),
    path('order/v1/api/', include('orders.urls.api_url')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

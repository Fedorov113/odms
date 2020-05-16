"""odms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

REACT_ROUTES = [
    'source',
    'login',
    'study'
]

urlpatterns = [
    
   
    path('admin/', admin.site.urls),
    path('api/mgms/', include(('mg_manager.api.urls', 'mgms'), namespace='mgms')),
    url(r'^silk/', include('silk.urls', namespace='silk')),
    path('api/auth/', include('accounts.urls')),
     path('', TemplateView.as_view(template_name='index.html')),
    url(r'^%s?' % '|'.join(REACT_ROUTES), TemplateView.as_view(template_name='index.html')),
    # url(r'^', TemplateView.as_view(template_name='index.html')),

    # re_path('app/.*', TemplateView.as_view(template_name='index.html')),
]

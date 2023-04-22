"""needful_things URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('index.html', views.home, name='home'),
    path('', views.home, name='home'),
    path('product/<str:product_id>/<str:name>', views.product, name='product'),
    path('user/<str:username>', views.user, name='user'),
    path('login.html', views.login, name='login'),
    path('login-action.html', views.login_action, name='login_action'),
    path('logout.html', views.logout, name='logout'),
    path('admin.html', views.admin, name='admin'),
    path('delete_user/<str:username>', views.delete_user, name='delete_user'),
    path('delete_product/<str:product_id>', views.delete_product, name='delete_product'),
    path('create_user.html', views.create_user, name='create_user'),
    path('create_product.html', views.create_product, name='create_product'),
]

"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from .views import view, homeview, CustomLoginView, protected, CommentDetail ,commentadd


urlpatterns = [
    path("admin/", admin.site.urls),
    path('xss/', view, name='xss'),
    path('sqlinjection/', view, name='sqlinjection'),
    path('login/', CustomLoginView.as_view(),  name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('comments/add/', commentadd, name='comment-add'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
    path('protected/', protected,  name='protected'),
    path('', homeview, name='index'),
]

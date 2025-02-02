from django.urls import path

from xss.views import xss_view


urlpatterns = [
    path('', xss_view, name='xss_attack')
]

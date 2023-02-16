from django.urls import path

from . import views

urlpatterns = [
    path('register_account', views.account_request, name='account_request'),
    path('', views.index, name='index')
]
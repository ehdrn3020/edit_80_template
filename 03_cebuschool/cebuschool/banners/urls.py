from django.urls import path
from . import views

app_name= 'banners'

urlpatterns = [
    path('', views.index, name='index')
]
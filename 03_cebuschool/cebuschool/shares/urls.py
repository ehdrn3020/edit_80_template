from django.urls import path, include
from . import views

app_name= 'shares'

urlpatterns = [
    path('chating', views.chating, name='chating'),
]
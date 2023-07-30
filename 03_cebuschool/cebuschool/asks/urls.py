from django.urls import path, include
from . import views

app_name= 'asks'

urlpatterns = [
    path('', views.index, name='index'),
    path('show', views.show, name='show'),
    path('create', views.create, name='create'),
    path('edit', views.edit, name='edit'),
    path('delete', views.index, name='delete'),
]
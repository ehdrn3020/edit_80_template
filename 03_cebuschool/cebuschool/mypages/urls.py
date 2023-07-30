from django.urls import path
from . import views

app_name= 'mypages'

urlpatterns = [
    # Big Menu
    path('', views.index, name='index'),
    # path('userinfo', views.userinfo, name='userinfo'),
    path('userinfo/<str:name>', views.userinfo, name='userinfo'),
    path('active/<str:name>', views.active, name='active'),
    
]
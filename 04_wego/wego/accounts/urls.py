from django.urls import path, include
from . import views

app_name= 'accounts'

urlpatterns = [
    # Login
    path('login/', views.login, name='login'),
    path('login/email', views.login_email, name='login_email'),

    # path('login/social/google', socials.SocialAccountAdapter.save_user, name='social_login'),

    # Logout
    path('logout', views.logout, name='logout'),

    # Register
    path('register/index', views.register_index, name='register_index'),
    path('register/create', views.register_create, name='register_create'),
    path('register/send', views.register_send, name='register_send'),
    path('activate/<str:uid64>/<str:token>', views.activate, name='activate'),
    path('register/confirm', views.register_confirm, name='register_confirm'),

    # Find Password and ID
    path('find', views.find, name='find')
]

from django.urls import path
from . import views

app_name = 'msgboxs'

urlpatterns = [
    # 알림함
    path('index/<str:tag>', views.index, name='index'),
    path('show/<int:user_id>', views.show, name='show'),
    path('show/<int:user_id>/<int:chat_id>', views.show, name='show'),
    path('show/<int:user_id>/<int:chat_id>/<int:after_chat>', views.show, name='show'),
    path('search', views.search, name='search'),
    path('create', views.create, name='create'),
    path('delete/<int:room_id>', views.delete, name='delete'),
    path('save/<int:room_id>', views.save, name='save'),

]

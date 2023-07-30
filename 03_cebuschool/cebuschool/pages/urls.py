from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # 메인페이지
    path('', views.index, name='index'),
    # 알림함
    path('messageboxs', views.messagebox_index, name='messageboxs_index'),
    path('messageboxs/show', views.messagebox_show, name='messageboxs_show'),
    path('messageboxs_search', views.messageboxs_search, name='messageboxs_search')
]
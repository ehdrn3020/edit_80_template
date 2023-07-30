from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('index', views.index, name='index'),
    path('index/<str:tag>', views.index, name='index'),
    path('create', views.create, name='create'),
    path('delete/<int:store_id>', views.delete, name='delete'),
    # 글쓰기 이미지 임시 업로드
    path('summernote_tmp', views.summernote_tmp, name='summernote_tmp'),
    # view넘버 증가
    path('views', views.views, name='views'),

]

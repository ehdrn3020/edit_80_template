from django.urls import path, include
from . import views

app_name= 'gallerys'

urlpatterns = [
    path('index', views.index, name='index'),
    path('index/<str:tag>', views.index, name='index'),
    # 스크롤 내릴시 데이터
    path('scroll_page', views.scroll_page, name='scroll_page'),
    path('show/<int:gallery_id>', views.show, name='show'),
    path('show/<int:gallery_id>/<int:comment_id>', views.show, name='show'),
    # 좋아요 클릭
    path('add_like', views.add_like, name='add_like'),
    path('add_unlike', views.add_unlike, name='add_unlike'),
    # 댓글 좋아요
    path('c_add_like', views.c_add_like, name='c_add_like'),
    path('c_add_unlike', views.c_add_unlike, name='c_add_unlike'),
    path('create', views.create, name='create'),
    path('create/<str:tag>', views.create, name='create'),  
    # 글쓰기 이미지 임시 업로드
    path('summernote_tmp', views.summernote_tmp, name='summernote_tmp'),
    # 이미지 회전
    path('img_rotate', views.img_rotate, name='img_rotate'),
    path('edit/<int:gallery_id>', views.edit, name='edit'),
    path('delete/<int:gallery_id>', views.delete, name='delete'),
]

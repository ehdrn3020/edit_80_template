from django.urls import path, include
from . import views

app_name= 'communitys'

urlpatterns = [
    path('index', views.index, name='index'),
    path('index/<str:tag>', views.index, name='index'),
    path('show/<int:community_id>', views.show, name='show'),
    path('show/<int:community_id>/<int:comment_id>', views.show, name='show'),
    path('create', views.create, name='create'),
    path('create/<str:tag>', views.create, name='create'),
    path('edit/<int:community_id>', views.edit, name='edit'),
    path('delete/<int:community_id>', views.delete, name='delete'),
    # 글쓰기 이미지 임시 업로드
    path('summernote_tmp', views.summernote_tmp, name='summernote_tmp'),
    # 좋아요 클릭
    path('add_like', views.add_like, name='add_like'),
    path('add_unlike', views.add_unlike, name='add_unlike'),
    # 댓글 좋아요
    path('c_add_like', views.c_add_like, name='c_add_like'),
    path('c_add_unlike', views.c_add_unlike, name='c_add_unlike'),
]

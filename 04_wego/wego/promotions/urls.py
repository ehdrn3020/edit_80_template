from django.urls import path, include
from . import views

app_name= 'promotions'

urlpatterns = [
    path('index', views.index, name='index'),
    path('index/<str:tag>', views.index, name='index'),
    path('show/<int:promotion_id>', views.show, name='show'),
    path('show/<int:promotion_id>/<int:comment_id>', views.show, name='show'),
    path('create', views.create, name='create'),
    path('create/<str:tag>', views.create, name='create'),
    path('edit/<int:promotion_id>', views.edit, name='edit'),
    path('delete/<int:promotion_id>', views.delete, name='delete'),

    # 미리보기
    path('preview/<int:promotion_id>', views.preview, name='preview'),
    # 미리보기후 작성완료
    path('confirm/<int:promotion_id>', views.confirm, name='confirm'),

    # 글쓰기 이미지 임시 업로드
    path('summernote_tmp', views.summernote_tmp, name='summernote_tmp'),
    # 예약하기 체크
    path('reserve_chk', views.reserve_chk, name='reserve_chk'),
    # 이미지 회전
    path('img_rotate', views.img_rotate, name='img_rotate'),

    # 별점추가
    path('addstar', views.addstar, name='addstar'),
    # 댓글 좋아요
    path('c_add_like', views.c_add_like, name='c_add_like'),
    path('c_add_unlike', views.c_add_unlike, name='c_add_unlike'),
    # 파트너쉽
    path('partnership', views.partnership, name='partnership'),

]

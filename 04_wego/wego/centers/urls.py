from django.urls import path, include
from . import views

app_name= 'centers'

urlpatterns = [
    # 공지사항
    path('index/<str:kind>', views.index, name='index'),
    path('show/<str:kind>/<int:center_id>', views.show, name='show'),
    path('show/<str:kind>/<int:center_id>/<int:comment_id>', views.show, name='show'),
    path('create/<str:kind>', views.create, name='create'),
    path('edit/<str:kind>/<int:center_id>', views.edit, name='edit'),
    path('delete/<str:kind>/<int:center_id>', views.delete, name='delete'),
    # 글쓰기 이미지 임시 업로드
    path('summernote_tmp', views.summernote_tmp, name='summernote_tmp'),
    # 좋아요 클릭
    path('add_like', views.add_like, name='add_like'),
    path('add_unlike', views.add_unlike, name='add_unlike'),

    # 파트너쉽
    path('partnership', views.partnership, name='partnership'),
    # 위고퀴즈 참여
    path('wego_quiz', views.wego_quiz, name='wego_quiz'),
    # 위고룰렛
    path('wego_roulette', views.wego_roulette, name='wego_roulette'),
    path('wego_roulette_create', views.wego_roulette_create, name='wego_roulette_create'),
]

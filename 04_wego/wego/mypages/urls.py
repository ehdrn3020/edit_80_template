from django.urls import path
from . import views

app_name= 'mypages'

urlpatterns = [
    # 등급
    path('', views.index, name='index'),

    # 회원정보
    path('userinfo/<str:name>', views.userinfo, name='userinfo'),
    # 프로필사진 변경
    path('add_profile', views.add_profile, name='add_profile'),
    # 프로필사진 커스텀파일로 변경
    path('add_custom_profile', views.add_custom_profile, name='add_custom_profile'),
    # 비밀번호변경
    path('chg_pwd', views.chg_pwd, name='chg_pwd'),
    # 정보변경
    path('chg_info', views.chg_info, name='chg_info'),

    # 활동
    path('active/<str:name>', views.active, name='active'),


]

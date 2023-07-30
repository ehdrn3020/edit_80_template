from django.urls import path, include
from . import views

app_name= 'comments'

urlpatterns = [
    # 후기
    path('create_after', views.create_after, name='create_after'),
    path('create_after_re', views.create_after_re, name='create_after_re'),
    path('delete_after', views.delete_after, name='delete_after'),

    # 질답
    path('create_ask', views.create_ask, name='create_ask'),
    path('create_ask_re', views.create_ask_re, name='create_ask_re'),
    path('delete_ask', views.delete_ask, name='delete_ask'),

    # 정보공유
    path('create_info', views.create_info, name='create_info'),
    path('create_info_re', views.create_info_re, name='create_info_re'),
    path('delete_info', views.delete_info, name='delete_info'),

    # 커뮤니티
    path('create_community', views.create_community, name='create_community'),
    path('create_community_re', views.create_community_re, name='create_community_re'),
    path('delete_community', views.delete_community, name='delete_community'),

    # 여행코스
    path('create_course', views.create_course, name='create_course'),
    path('create_course_re', views.create_course_re, name='create_course_re'),
    path('delete_course', views.delete_course, name='delete_course'),

    # 실시간세부
    path('create_gallery', views.create_gallery, name='create_gallery'),
    # path('create_gallery_re', views.create_gallery_re, name='create_gallery_re'),
    path('delete_gallery', views.delete_gallery, name='delete_gallery'),

    # 여행사홍보
    path('create_promotion', views.create_promotion, name='create_promotion'),
    path('create_promotion_re', views.create_promotion_re, name='create_promotion_re'),
    path('delete_promotion', views.delete_promotion, name='delete_promotion'),

    # 위고센터
    path('create_center', views.create_center, name='create_center'),
    path('create_center_re', views.create_center_re, name='create_center_re'),
    path('delete_center', views.delete_center, name='delete_center'),

]

from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    # 스쿨퀴즈 참여
    path('school_quiz', views.school_quiz, name='school_quiz'),
    # 룰렛
    path('school_roulette', views.school_roulette, name='school_roulette'),
    path('school_roulette_create', views.school_roulette_create, name='school_roulette_create'),
    # path('school_roulette_update', views.school_roulette_update, name='school_roulette_update'),
     
]
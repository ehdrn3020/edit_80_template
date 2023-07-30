from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'pages'

urlpatterns = [
    # 메인페이지
    path('', views.index, name='index'),
    # 스크랩
    path('addscrap', views.addscrap, name='addscrap'),
    # 알림
    path('alarm_url', views.alarm_url, name='alarm_url'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type='text/plain')),
]

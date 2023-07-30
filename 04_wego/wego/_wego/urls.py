from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import ( handler400, handler404, handler500 )

handler404 = "pages.errors.error400"
handler404 = "pages.errors.error404"
handler500 = "pages.errors.error500"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('banners/', include('banners.urls')),
    path('accounts/', include('accounts.urls')),
    path('social/', include('allauth.urls')),
    path('mypages/', include('mypages.urls')),
    path('afters/', include('afters.urls')),
    path('comments/', include('comments.urls')),
    path('asks/', include('asks.urls')),
    path('infos/', include('infos.urls')),
    path('communitys/', include('communitys.urls')),
    path('courses/', include('courses.urls')),
    path('promotions/', include('promotions.urls')),
    path('gallerys/', include('gallerys.urls')),
    path('stores/', include('stores.urls')),
    path('msgboxs/', include('msgboxs.urls')),
    path('centers/', include('centers.urls')),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

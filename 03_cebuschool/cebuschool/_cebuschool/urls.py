from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('banners/', include('banners.urls')),
    path('accounts/', include('accounts.urls')),
    path('social/', include('allauth.urls')),
    path('mypages/', include('mypages.urls')),
    path('afters/', include('afters.urls')),
    path('asks/', include('asks.urls')),
    path('shares/', include('shares.urls')),
    path('promotions/', include('promotions.urls')),
    path('gallerys/', include('gallerys.urls')),
    path('stores/', include('stores.urls')),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#개발환경 디버그
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
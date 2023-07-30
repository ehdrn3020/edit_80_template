from django.contrib import admin
from .models import Notice, CustomerCenter, WegoQuiz, WegoRoulette

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'board_kind', 'likes', 'views', 'comments', 'is_published', 'upload_date')
    list_display_links = ('title','user')
    list_editable = ('is_published',)
    # list_filter = ('brand_name',)
    search_fields = ('title', 'user__username', 'board_kind')
    list_per_page = 20

class CustomerCenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'board_kind', 'likes', 'views', 'comments', 'secret', 'is_published', 'upload_date')
    list_display_links = ('title','user')
    list_editable = ('secret', 'is_published')
    search_fields = ('title', 'user__username', 'board_kind')
    list_per_page = 20

# Register your models here.
class WegoQuizAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'get_point', 'apply_date')
    list_display_links = ('username', 'title',)
    search_fields = ('username', 'title')
    list_per_page = 20

class WegoRouletteAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'get_point', 'apply_date')
    list_display_links = ('username', 'title',)
    search_fields = ('username', 'title')
    list_per_page = 20
    
admin.site.register(Notice, NoticeAdmin)
admin.site.register(CustomerCenter, CustomerCenterAdmin)
admin.site.register(WegoQuiz, WegoQuizAdmin)
admin.site.register(WegoRoulette, WegoRouletteAdmin)

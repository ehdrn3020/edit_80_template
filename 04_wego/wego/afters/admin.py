from django.contrib import admin
from .models import After

# Register your models here.
class AfterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'attribute', 'board_kind', 'likes', 'views', 'comments', 'main_published', 'best_published', 'is_published', 'upload_date')
    list_display_links = ('title','user')
    list_editable = ('main_published', 'best_published', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('title', 'user__username', 'attribute', 'board_kind')
    list_per_page = 20

admin.site.register(After, AfterAdmin)

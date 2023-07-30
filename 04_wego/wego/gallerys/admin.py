from django.contrib import admin
from .models import Gallery

# Register your models here.
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'short_content', 'attribute', 'board_kind', 'likes', 'views', 'comments', 'main_published','best_published', 'is_published', 'upload_date')
    list_display_links = ('short_content','user')
    list_editable = ('main_published','best_published', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('content', 'user__username', 'attribute', 'board_kind')
    list_per_page = 20

    # 컨텐츠글자 줄여서 보이기
    def short_content(self, post):
        return post.content[:30]

admin.site.register(Gallery, GalleryAdmin)

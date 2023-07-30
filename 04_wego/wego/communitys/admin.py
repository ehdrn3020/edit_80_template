from django.contrib import admin
from .models import Community

# Register your models here.
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'attribute', 'board_kind', 'likes', 'views', 'comments', 'is_published', 'upload_date')
    list_display_links = ('title','user')
    list_editable = ('is_published',)
    # list_filter = ('brand_name',)
    search_fields = ('title', 'user__username', 'attribute', 'board_kind')
    list_per_page = 20

admin.site.register(Community, CommunityAdmin)

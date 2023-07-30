from django.contrib import admin
from .models import Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'attribute', 'board_kind', 'likes', 'views', 'comments', 'best_published', 'is_published', 'upload_date')
    list_display_links = ('title','user')
    list_editable = ('best_published', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('title', 'user__username', 'attribute', 'board_kind')
    list_per_page = 20

admin.site.register(Course, CourseAdmin)

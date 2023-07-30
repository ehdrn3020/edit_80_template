from django.contrib import admin
from .models import Comment_After
from .models import Comment_Ask
from .models import Comment_Community
from .models import Comment_Info
from .models import Comment_Course
from .models import Comment_Gallery
from .models import Comment_Promotion
from .models import Comment_Notice
from .models import Comment_CustomerCenter

# Register your models here.
class Comment_AfterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_table', 'parent_id', 'likes', 'is_declarated', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'comment_table', 'parent_id')
    list_editable = ('is_declarated', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'comment_table__title', 'parent_id__id')
    list_per_page = 20

class Comment_AskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_table', 'parent_id', 'likes', 'is_declarated', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'comment_table', 'parent_id')
    list_editable = ('is_declarated', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'comment_table__title', 'parent_id__id')
    list_per_page = 20

class Comment_CommunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_table', 'parent_id', 'likes', 'is_declarated', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'comment_table', 'parent_id')
    list_editable = ('is_declarated', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'comment_table__title', 'parent_id__id')
    list_per_page = 20

class Comment_InfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_table', 'parent_id', 'likes', 'is_declarated', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'comment_table', 'parent_id')
    list_editable = ('is_declarated', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'comment_table__title', 'parent_id__id')
    list_per_page = 20

class Comment_CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_table', 'parent_id', 'likes', 'is_declarated', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'comment_table', 'parent_id')
    list_editable = ('is_declarated', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'comment_table__title', 'parent_id__id')
    list_per_page = 20

class Comment_GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_table', 'parent_id', 'likes', 'is_declarated', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'comment_table', 'parent_id')
    list_editable = ('is_declarated', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'comment_table__title', 'parent_id__id')
    list_per_page = 20

class Comment_PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_table', 'parent_id', 'star_total', 'is_declarated', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'comment_table', 'parent_id')
    list_editable = ('is_declarated', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'comment_table__title', 'parent_id__id')
    list_per_page = 20

class Comment_NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_table', 'parent_id', 'likes', 'is_declarated', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'comment_table', 'parent_id')
    list_editable = ('is_declarated', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'comment_table__title', 'parent_id__id')
    list_per_page = 20

class Comment_CustomerCenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment_table', 'parent_id', 'likes', 'is_declarated', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'comment_table', 'parent_id')
    list_editable = ('is_declarated', 'is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'comment_table__title', 'parent_id__id')
    list_per_page = 20


admin.site.register(Comment_After, Comment_AfterAdmin)
admin.site.register(Comment_Ask, Comment_AskAdmin)
admin.site.register(Comment_Community, Comment_CommunityAdmin)
admin.site.register(Comment_Info, Comment_InfoAdmin)
admin.site.register(Comment_Course, Comment_CourseAdmin)
admin.site.register(Comment_Gallery, Comment_GalleryAdmin)
admin.site.register(Comment_Promotion, Comment_PromotionAdmin)
admin.site.register(Comment_Notice, Comment_NoticeAdmin)
admin.site.register(Comment_CustomerCenter, Comment_CustomerCenterAdmin)

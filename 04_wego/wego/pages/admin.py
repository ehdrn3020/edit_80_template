from django.contrib import admin
from .models import Point, Exprience, ApiData, AddLike, AddStar, AddScrap, PartnerShip

# Register your models here.
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'point', 'description')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'point')
    list_per_page = 20

class ExprienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'exprience', 'description')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'exprience')
    list_per_page = 20

class ApiDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'data_list', 'recall_min', 'last_call')
    list_display_links = ('id', 'title', 'data_list')
    search_fields = ('title',)
    list_per_page = 20

class AddLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_name', 'content_id','comment_id','content_title', 'is_active', 'upload_date')
    list_display_links = ('id', 'user', 'content_name')
    search_fields = ('user__username', 'content_name')
    list_editable = ('is_active',)
    list_per_page = 20

class AddStarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'score', 'content_name', 'content_id','comment_id','content_title', 'is_active', 'upload_date')
    list_display_links = ('id', 'user', 'content_name')
    search_fields = ('user__username', 'content_name')
    list_editable = ('is_active',)
    list_per_page = 20

class AddScrapAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tag', 'content_type', 'object_id','content_object','is_active', 'upload_date')
    list_display_links = ('id', 'user', 'tag')
    search_fields = ('user__username', 'tag')
    list_editable = ('is_active',)
    list_per_page = 20

class PartnerShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_info', 'is_read', 'upload_date')
    list_display_links = ('id', 'contact_info')
    search_fields = ('id', 'contact_info')
    list_editable = ('is_read',)
    list_per_page = 20

admin.site.register(Point, PointAdmin)
admin.site.register(Exprience, ExprienceAdmin)
admin.site.register(ApiData, ApiDataAdmin)
admin.site.register(AddLike, AddLikeAdmin)
admin.site.register(AddStar, AddStarAdmin)
admin.site.register(PartnerShip, PartnerShipAdmin)
admin.site.register(AddScrap, AddScrapAdmin)

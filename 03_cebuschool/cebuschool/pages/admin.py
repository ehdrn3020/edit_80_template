from django.contrib import admin
from .models import Point, ApiData

# Register your models here.
class PointAdmin(admin.ModelAdmin):
    list_display = ('title', 'point', 'description')
    list_display_links = ('title',)
    search_fields = ('title', 'point')
    list_per_page = 20

class ApiDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'data_list', 'recall_min', 'last_call')
    list_display_links = ('title', 'data_list',)
    search_fields = ('title',)
    list_per_page = 20

admin.site.register(Point, PointAdmin)
admin.site.register(ApiData, ApiDataAdmin)
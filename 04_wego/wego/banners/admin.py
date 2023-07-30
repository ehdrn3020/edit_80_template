from django.contrib import admin
from .models import Banner

# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand_name', 'click_number', 'position_1', 'position_2','is_published', 'upload_date', 'expiration_date')
    list_display_links = ('id', 'title','brand_name')
    # list_filter = ('brand_name',)
    list_editable = ('is_published',)
    search_fields = ('title', 'brand_name')
    list_per_page = 20

admin.site.register(Banner, BannerAdmin)

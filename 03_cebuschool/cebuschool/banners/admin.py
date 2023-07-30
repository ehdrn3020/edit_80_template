from django.contrib import admin
from .models import Banner

# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand_name', 'click_number', 'is_published', 'upload_date', 'expiration_date')
    list_display_links = ('title','brand_name')
    # list_filter = ('brand_name',) 
    list_editable = ('is_published',)
    search_fields = ('title', 'brand_name')
    list_per_page = 20

admin.site.register(Banner, BannerAdmin)
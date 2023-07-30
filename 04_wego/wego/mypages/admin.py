from django.contrib import admin
from .models import Profile_Image

# Register your models here.
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'level', 'price', 'click_number', 'is_published', 'upload_date')
    list_display_links = ('id', 'title')
    # list_filter = ('brand_name',)
    list_editable = ('is_published',)
    search_fields = ('title', 'level')
    list_per_page = 20

admin.site.register(Profile_Image, ProfileImageAdmin)

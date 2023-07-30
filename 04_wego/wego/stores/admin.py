from django.contrib import admin
from .models import Store, Store_Main

# Register your models here.
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'item_name', 'price', 'click_number', 'best_published', 'is_published', 'upload_date')
    list_display_links = ('id', 'title','item_name')
    # list_filter = ('brand_name',)
    list_editable = ('best_published', 'is_published')
    search_fields = ('title', 'item_name')
    list_per_page = 20

class Store_MainAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'click_number', 'is_published', 'upload_date', 'expiration_date')
    list_display_links = ('id', 'title')
    # list_filter = ('brand_name',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_per_page = 20

admin.site.register(Store, StoreAdmin)
admin.site.register(Store_Main, Store_MainAdmin)

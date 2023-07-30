from django.contrib import admin
from .models import Promotion, Option

# Register your models here.
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'brand_name', 'board_kind', 'p_price_min', 'w_price_min', 'star_total', 'star_participate', 'views', 'best_published', 'sale_published', 'is_checked', 'is_published', 'upload_date')
    list_display_links = ('user','brand_name','board_kind')
    list_editable = ('best_published', 'sale_published', 'is_checked','is_published')
    # list_filter = ('brand_name',)
    search_fields = ('user__username', 'brand_name', 'board_kind')
    list_per_page = 20

class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'is_published', 'upload_date')
    list_display_links = ('title','content')
    list_editable = ('is_published',)
    # list_filter = ('brand_name',)
    search_fields = ('title', 'content')
    list_per_page = 20

admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Option, OptionAdmin)

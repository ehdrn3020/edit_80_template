from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_active', 'email', 'social_login', 'level')
    list_display_links = ('id','username')
    # list_filter = ('username',)
    list_editable = ('is_active',)
    search_fields = ('username', 'email')
    list_per_page = 20

admin.site.register(User, UserAdmin)

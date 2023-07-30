from django.contrib import admin
from .models import SchoolQuiz
from .models import SchoolRoulette

# Register your models here.
class SchoolQuizAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'get_point', 'apply_date')
    list_display_links = ('username', 'title',)
    search_fields = ('username', 'title')
    list_per_page = 20

class SchoolRouletteAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'get_point', 'apply_date')
    list_display_links = ('username', 'title',)
    search_fields = ('username', 'title')
    list_per_page = 20

admin.site.register(SchoolQuiz, SchoolQuizAdmin)
admin.site.register(SchoolRoulette, SchoolRouletteAdmin)

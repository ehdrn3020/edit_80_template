from django.contrib import admin
from .models import Msgbox, SaveMsgbox, Alarm_Addcommentlike


class Alarm_AddcommentlikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'likefrom', 'comment_user', 'act_type', 'content_id', 'comment_id', 'comment_table', 'checkitout','is_published', 'upload_date')
    list_display_links = ('id', 'likefrom', 'comment_user', 'comment_table', 'content_id', 'checkitout')
    list_editable = ('is_published',)
    list_per_page = 20

class MsgboxAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'send_user', 'from_user', 'is_checked', 'is_active', 'upload_date')
    list_display_links = ('id', 'chat_id')
    search_fields = ('id','chat_id','send_user__username','from_user__username')
    list_editable = ('is_active',)
    list_per_page = 20

class SaveMsgboxAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'msgbox', 'is_published', 'upload_date')
    list_display_links = ('id', 'user', 'msgbox')
    search_fields = ('id','user__username', 'msgbox__send_user__username')
    list_editable = ('is_published',)
    list_per_page = 20

admin.site.register(Alarm_Addcommentlike, Alarm_AddcommentlikeAdmin)
admin.site.register(Msgbox, MsgboxAdmin)
admin.site.register(SaveMsgbox, SaveMsgboxAdmin)

from django.db import models
from datetime import datetime
from accounts.models import User

# 댓글/좋아요 알람
class Alarm_Addcommentlike(models.Model):
    act_type = models.CharField(max_length=10)
    likefrom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercommentlike', default='1')
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writtenbyuser', blank=True, null=True)
    comment_table = models.CharField(max_length=20, blank=True, null=True)
    comment_id = models.IntegerField(blank=True, null=True)
    board_name = models.CharField(max_length=30, blank=True, null=True)
    board_url = models.CharField(max_length=200, blank=True, null=True)
    content_id = models.IntegerField(blank=True, null=True)
    checkitout = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# 쪽지보내기 모델
class Msgbox(models.Model):
    chat_id = models.CharField(max_length=50)
    send_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_send')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_from')
    content = models.TextField(blank=True)
    is_checked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.send_user.username

# 쪽지보관함
class SaveMsgbox(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    msgbox = models.ForeignKey(Msgbox, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

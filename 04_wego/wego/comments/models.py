from django.db import models
from datetime import datetime
from accounts.models import User
from afters.models import After
from infos.models import Info
from asks.models import Ask
from courses.models import Course
from communitys.models import Community
from gallerys.models import Gallery
from promotions.models import Promotion
from centers.models import Notice, CustomerCenter


# 후기댓글 모델
class Comment_After(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_table = models.ForeignKey(After, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = content = models.TextField()
    likes = models.IntegerField(default=0)
    is_declarated = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# 질답댓글 모델
class Comment_Ask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_table = models.ForeignKey(Ask, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = content = models.TextField()
    likes = models.IntegerField(default=0)
    is_declarated = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# 커뮤니티댓글 모델
class Comment_Community(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_table = models.ForeignKey(Community, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = content = models.TextField()
    likes = models.IntegerField(default=0)
    is_declarated = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# 정보공유댓글 모델
class Comment_Info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_table = models.ForeignKey(Info, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = content = models.TextField()
    likes = models.IntegerField(default=0)
    is_declarated = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# 여행코스댓글 모델
class Comment_Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_table = models.ForeignKey(Course, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = content = models.TextField()
    likes = models.IntegerField(default=0)
    is_declarated = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# 실시간세부댓글 모델
class Comment_Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_table = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = content = models.TextField()
    likes = models.IntegerField(default=0)
    is_declarated = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# 여행사홍보댓글 모델
class Comment_Promotion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_table = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    star_total = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_response = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_price = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_clean = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_service = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_kindness = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_quality = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_location = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    content = content = models.TextField()
    likes = models.IntegerField(default=0)
    is_declarated = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# 공지사항댓글 모델
class Comment_Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_table = models.ForeignKey(Notice, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = content = models.TextField()
    likes = models.IntegerField(default=0)
    is_declarated = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# 고객센터댓글 모델
class Comment_CustomerCenter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_table = models.ForeignKey(CustomerCenter, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = content = models.TextField()
    likes = models.IntegerField(default=0)
    is_declarated = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now)

# Create your models here.
# 글쓴이
# 댓글관련 모델 (Afters)
# 상위댓글모델 ID (Null가능)
# 내용
# 좋아요
# 신고여부
# 이스 퍼블리쉬드
# 업로드날짜

from django.db import models
from datetime import datetime
from banners.models import Banner
from accounts.models import User

class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board_kind = models.CharField(max_length=50)
    attribute = models.CharField(max_length=50, default="NONE")
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    pimg1 = models.CharField(max_length=100)
    pimg2 = models.CharField(max_length=100, blank=True)
    pimg3 = models.CharField(max_length=100, blank=True)
    pimg4 = models.CharField(max_length=100, blank=True)
    pimg5 = models.CharField(max_length=100, blank=True)

    title = models.CharField(max_length=50,default="",blank=True)
    tag = models.CharField(max_length=50, blank=True)
    content = models.TextField(blank=True)
    show_ad = models.ForeignKey(Banner, on_delete=models.CASCADE, default='')

    main_published = models.BooleanField(default=False)
    best_published = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.tag

# 글쓴이
# 게시판선택
# 글 속성 ( 동영상, 단일사진, 다중사진 )
# 좋아요 수
# 조회수
# 댓글 수

# 이미지 1 - 5
# 태그 ( 해쉬태그 )
# 내용

# 메인메뉴여부
# 베스트여부
# 퍼블릭여부
# 글쓴시간

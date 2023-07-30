from django.db import models
from datetime import datetime
from banners.models import Banner
from accounts.models import User

class Community(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board_kind = models.CharField(max_length=50)
    attribute = models.CharField(max_length=50, default="NONE")
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    tag = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    g_map1 = models.CharField(max_length=100)
    g_map2 = models.CharField(max_length=100)
    g_map3 = models.CharField(max_length=100)
    g_map4 = models.CharField(max_length=100)
    g_map5 = models.CharField(max_length=100)
    url_link = models.CharField(max_length=200, blank=True)
    show_ad = models.ForeignKey(Banner, on_delete=models.CASCADE)

    is_imaged = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

# 글쓴이
# 게시판선택
# 글 속성 ( 광고, 공지 )
# 좋아요 수
# 조회수
# 댓글 수

# 태그 ( 해쉬태그 )
# 제목
# 내용 ( summernote )
# 지도 ( map1-5 )
# 관련링크
# 글볼때 광고

# 이미지여부
# 퍼블릭여부
# 글쓴시간

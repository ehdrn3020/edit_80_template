from django.db import models
from datetime import datetime
from banners.models import Banner
from accounts.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Promotion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board_kind = models.CharField(max_length=50)
    attribute = models.CharField(max_length=50, default="NONE")
    avgstar = models.DecimalField(default=0, max_digits=5, decimal_places=4)
    numstar = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    title = models.CharField(max_length=50)
    tag = models.CharField(max_length=50, blank=True)
    content = models.TextField(blank=True)
    g_map1 = models.CharField(max_length=100)
    g_map2 = models.CharField(max_length=100)
    g_map3 = models.CharField(max_length=100)
    g_map4 = models.CharField(max_length=100)
    g_map5 = models.CharField(max_length=100)
    url_link = models.CharField(max_length=200, blank=True)
    show_ad = models.ForeignKey(Banner, on_delete=models.CASCADE)

    is_imaged = models.BooleanField(default=False)
    present_image = models.ImageField(upload_to='promotions/ad/', blank=True)
    best_published = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title



    # def save(self):
    #     resize_img = Image.open(self.present_image)
    #     output = BytesIO()
    #     resize_img.resize((213,198))
    #
	# 	#after modifications, save it to the output
    #     resize_img.save(output, format='JPEG', quality=100)
    #     output.seek(0)
    #
	# 	#change the imagefield value to be the newley modifed image value
    #     self.present_image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.present_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
    #
    #     super(Promotion,self).save()

# 글쓴이
# 게시판선택
# 글 속성 ( 광고, 공지 )
# 글 평점
# 조회수
# 댓글 수

# 제목
# 내용 ( summernote )
# 지도 ( map1-5 )
# 관련링크
# 글볼때 광고

# 글내용 이미지 여부
# 광고시 대표이미지
# 광고여부
# 퍼블릭여부
# 글쓴시간

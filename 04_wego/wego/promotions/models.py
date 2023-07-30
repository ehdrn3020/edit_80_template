from django.db import models
from datetime import datetime
from accounts.models import User
from PIL import Image

class Promotion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=10, blank=True)
    board_kind = models.CharField(max_length=10, blank=True)
    introduction = models.CharField(max_length=60, blank=True)
    tag1 = models.CharField(max_length=10, blank=True, default="신규")
    tag2 = models.CharField(max_length=10, blank=True)
    tag3 = models.CharField(max_length=10, blank=True)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    p_price_min = models.IntegerField(default=0)
    p_price_max = models.IntegerField(default=0)
    kakao_id = models.CharField(max_length=50, blank=True)
    w_price_min = models.IntegerField(default=0)
    w_price_max = models.IntegerField(default=0)
    workday_mon = models.BooleanField(default=False)
    workday_tue = models.BooleanField(default=False)
    workday_wed = models.BooleanField(default=False)
    workday_thur= models.BooleanField(default=False)
    workday_fri = models.BooleanField(default=False)
    workday_sat = models.BooleanField(default=False)
    workday_sun = models.BooleanField(default=False)
    worktime_start = models.CharField(max_length=50, blank=True)
    worktime_finish = models.CharField(max_length=50, blank=True)
    worktime_start_weekend = models.CharField(max_length=50, blank=True)
    worktime_finish_weekend = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    url_link = models.CharField(max_length=100, blank=True)
    url_click = models.IntegerField(default=0)
    # 이미지
    pimg1 = models.CharField(max_length=100, blank=True)
    pimg2 = models.CharField(max_length=100, blank=True)
    pimg3 = models.CharField(max_length=100, blank=True)
    pimg4 = models.CharField(max_length=100, blank=True)
    pimg5 = models.CharField(max_length=100, blank=True)
    pimg6 = models.CharField(max_length=100, blank=True)
    pimg7 = models.CharField(max_length=100, blank=True)
    pimg8 = models.CharField(max_length=100, blank=True)
    pimg9 = models.CharField(max_length=100, blank=True)
    pimg10= models.CharField(max_length=100, blank=True)
    pimg11= models.CharField(max_length=100, blank=True)
    pimg12= models.CharField(max_length=100, blank=True)
    pimg13= models.CharField(max_length=100, blank=True)
    pimg14= models.CharField(max_length=100, blank=True)
    pimg15= models.CharField(max_length=100, blank=True)
    pimg16= models.CharField(max_length=100, blank=True)
    pimg17= models.CharField(max_length=100, blank=True)
    pimg18= models.CharField(max_length=100, blank=True)
    pimg19= models.CharField(max_length=100, blank=True)
    pimg20= models.CharField(max_length=100, blank=True)
    # 대표상품 이미지
    rep_img1= models.CharField(max_length=100, blank=True)
    rep_img2= models.CharField(max_length=100, blank=True)
    rep_img3= models.CharField(max_length=100, blank=True)
    rep_img4= models.CharField(max_length=100, blank=True)
    rep_img5= models.CharField(max_length=100, blank=True)
    # 대표상품 설명글
    rep_txt1= models.CharField(max_length=50, blank=True)
    rep_txt2= models.CharField(max_length=50, blank=True)
    rep_txt3= models.CharField(max_length=50, blank=True)
    rep_txt4= models.CharField(max_length=50, blank=True)
    rep_txt5= models.CharField(max_length=50, blank=True)
    # 편의시설
    opt1 = models.BooleanField(default=False)
    opt2 = models.BooleanField(default=False)
    opt3 = models.BooleanField(default=False)
    opt4 = models.BooleanField(default=False)
    opt5 = models.BooleanField(default=False)
    opt6 = models.BooleanField(default=False)
    opt7 = models.BooleanField(default=False)
    opt8 = models.BooleanField(default=False)
    opt9 = models.BooleanField(default=False)
    opt10 = models.BooleanField(default=False)
    opt11 = models.BooleanField(default=False)
    opt12 = models.BooleanField(default=False)
    opt13 = models.BooleanField(default=False)
    opt14 = models.BooleanField(default=False)
    opt15 = models.BooleanField(default=False)
    opt16 = models.BooleanField(default=False)
    opt18 = models.BooleanField(default=False)
    opt17 = models.BooleanField(default=False)
    opt19 = models.BooleanField(default=False)
    opt20 = models.BooleanField(default=False)
    # 내용
    content = models.TextField(blank=True)
    g_map1 = models.CharField(max_length=100, blank=True)
    g_map2 = models.CharField(max_length=100, blank=True)
    g_map3 = models.CharField(max_length=100, blank=True)
    g_map4 = models.CharField(max_length=100, blank=True)
    g_map5 = models.CharField(max_length=100, blank=True)
    # 리뷰관련 별점
    star_total = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_response = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_price = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_clean = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_service = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_kindness = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_quality = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_location = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    star_participate = models.IntegerField(default=0)

    show_ad = models.CharField(max_length=100, default='여행사홍보')
    best_published = models.BooleanField(default=False)
    sale_published = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

# 편의시설모델
class Option(models.Model):
    title = models.CharField(max_length=50, blank=True)
    icon = models.ImageField(upload_to='promotions/opt_icon/', blank=True)
    content = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(default=datetime.now, blank=True)

# 할인코드 모델

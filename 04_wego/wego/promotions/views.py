import os
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from banners.models import Banner
from django.urls import reverse
from pages.models import AddLike, AddStar, Point, Exprience, PartnerShip
from .models import Promotion, Option
from comments.models import Comment_Promotion
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from pages.views import get_date, uprising_keyword
from django.contrib import messages
from PIL import Image
import re
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from datetime import datetime, timedelta
from msgboxs.models import Alarm_Addcommentlike
from msgboxs.views import getAlarmListNew
from django.db.models import Q

def index(request, tag=None):
    # 배너 데이터
    banners = promotion_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 여행사홍보
    obj = Promotion.objects.order_by('-upload_date').filter(is_published=True)

    board_kind = '전체'
    # 상단태그맵핑 클릭시
    if tag == 'resort':
        board_kind = '리조트'
    elif tag == 'hotel':
        board_kind = '호텔'
    elif tag == 'kor_good':
        board_kind = '교민맛집'
    elif tag == 'local_food':
        board_kind = '로컬맛집'
    elif tag == 'hopping':
        board_kind = '호핑'
    elif tag == 'daytour':
        board_kind = '데이투어'
    elif tag == 'massage':
        board_kind = '마사지샵'
    elif tag == 'fullvilla':
        board_kind = '풀빌라'
    elif tag == 'beauty':
        board_kind = '뷰티샵'
    elif tag == 'diving':
        board_kind = '다이빙샵'
    elif tag == 'sourvenir':
        board_kind = '기념품샵'

    # 검색창
    s_select = request.GET.get('sch_slt')
    s_text = request.GET.get('sch_tx')
    if s_select != None:
        if s_select == '제목':
            obj = obj.filter(introduction__contains=s_text)
        else :
            obj = obj.filter(brand_name__contains=s_text)

    objs = []
    objs.append(obj)
    objs.append(obj.filter(board_kind='리조트'))
    objs.append(obj.filter(board_kind='호텔'))
    objs.append(obj.filter(board_kind='교민맛집'))
    objs.append(obj.filter(board_kind='로컬맛집'))
    objs.append(obj.filter(board_kind='호핑'))
    objs.append(obj.filter(board_kind='데이투어'))
    objs.append(obj.filter(board_kind='마사지샵'))
    objs.append(obj.filter(board_kind='풀빌라'))
    objs.append(obj.filter(board_kind='뷰티샵'))
    objs.append(obj.filter(board_kind='다이빙샵'))
    objs.append(obj.filter(board_kind='기념품샵'))

    # 페이지네이션
    best_list = [] # 베스트글
    sale_list = [] # 할인이벤트글
    promotion_list = [] #날짜순
    staravg_list = [] #평점순
    starparti_list = [] #리뷰많은순
    page_range = []
    page_obj = ''
    for obj in objs:
        # 베스트글 페이징
        best_obj = obj.filter(best_published=True)
        page = request.GET.get('page')
        paginator = Paginator(best_obj, 8)
        best_obj = paginator.get_page(page)
        best_list.append(best_obj)

        # 할인이벤트 페이징
        sale_obj = obj.filter(sale_published=True)
        paginator = Paginator(sale_obj, 8)
        sale_obj = paginator.get_page(page)
        sale_list.append(sale_obj)

        # 날짜순 페이징
        paginator = Paginator(obj, 8)
        date_obj = paginator.get_page(page)
        promotion_list.append(date_obj)

        # 평점순 페이징
        staravg_obj = obj.order_by('-star_total')
        paginator = Paginator(staravg_obj, 8)
        staravg_obj = paginator.get_page(page)
        staravg_list.append(staravg_obj)

        # 리뷰많은순 페이징
        starparti_obj = obj.order_by('-star_participate')
        paginator = Paginator(starparti_obj, 8)
        starparti_obj = paginator.get_page(page)
        starparti_list.append(starparti_obj)

        # 페이지네이션 나타낼 번호 제어 ( 가장긴 오브젝트기준 )
        new_page_range = pagination_range(date_obj, paginator)
        if len(page_range) < len(new_page_range):
            page_range = new_page_range
            page_obj = date_obj

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        's_select':s_select,
        's_text':s_text,
        'best_list':best_list,
        'sale_list':sale_list,
        'promotion_list':promotion_list,
        'staravg_list':staravg_list,
        'starparti_list':starparti_list,
        'board_kind':board_kind,
        'page_range': page_range,
        'page_obj':page_obj,
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'promotions/index.html', context)

def show(request, promotion_id, comment_id=None):
    # 배너 데이터
    banners = promotion_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 게시글 데이터
    promotion = get_object_or_404(Promotion, pk=promotion_id)

    # 이미지
    pimg = []
    pimg.append(promotion.pimg1)
    pimg.append(promotion.pimg2)
    pimg.append(promotion.pimg3)
    pimg.append(promotion.pimg4)
    pimg.append(promotion.pimg5)
    pimg.append(promotion.pimg6)
    pimg.append(promotion.pimg7)
    pimg.append(promotion.pimg8)
    pimg.append(promotion.pimg9)
    pimg.append(promotion.pimg10)
    pimg.append(promotion.pimg11)
    pimg.append(promotion.pimg12)
    pimg.append(promotion.pimg13)
    pimg.append(promotion.pimg14)
    pimg.append(promotion.pimg15)
    pimg.append(promotion.pimg16)
    pimg.append(promotion.pimg17)
    pimg.append(promotion.pimg18)
    pimg.append(promotion.pimg19)
    pimg.append(promotion.pimg20)

    # 게시글의 댓글 데이터
    comments = promotion.comment_promotion_set.all().order_by('-upload_date').filter(is_published=True)
    # 페이지네이션
    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    # 페이지네이션 나타낼 번호 제어
    page_range = pagination_range(comments, paginator)

    # 댓글쓸시 포인트
    point = Point.objects.filter(title='여행사홍보댓글').values('point').first()

    # 게시글 조회수 증가
    promotion.views += 1
    promotion.save()
    # 글작성일을 나타낼 때 날짜 or 몇분전으로 나타내기 위한 변수
    time = get_date('nowtime').strftime('%Y-%m-%d:%H')
    new_date = get_date('nowtime').strftime('%Y-%m-%d')
    # 게시글이 댓글 쓴후에 보여질시
    comment_id = comment_id

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'pimg':pimg,
        'content': promotion,
        'content_object': '여행사홍보',
        'comments': comments,
        'point' :point,
        'time': time,
        'new_date': new_date,
        'comment_id': comment_id,
        'page_range':page_range
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'promotions/show.html', context)

@login_required
def create(request, tag=None):
    # 배너 데이터
    banners = promotion_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 옵션
    opts = Option.objects.order_by('id').filter(is_published=True)
    # 글쓸시 포인트
    point = Point.objects.filter(title='여행사홍보작성').values('point').first()
    ex = Exprience.objects.filter(title='여행사홍보작성').values('exprience').first()

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'opts':opts,
        'point': point,
        'board_kind': tag
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    # 글저장할 때
    if request.method == 'POST':
        print(request.POST)
        # 데이터저장
        preview = request.POST['preview']
        user = request.user
        brand_name = request.POST['brand_name']
        board_kind = request.POST['board_kind']
        introduction = request.POST['introduction']
        p_price_min = request.POST['p_price_min']
        p_price_max = request.POST['p_price_max']
        w_price_min = request.POST['w_price_min']
        w_price_max = request.POST['w_price_max']
        kakao_id = request.POST['kakao_id']
        workday = []
        workday.append(request.POST.get('workday_mon'))
        workday.append(request.POST.get('workday_tue'))
        workday.append(request.POST.get('workday_wed'))
        workday.append(request.POST.get('workday_thur'))
        workday.append(request.POST.get('workday_fri'))
        workday.append(request.POST.get('workday_sat'))
        workday.append(request.POST.get('workday_sun'))
        all_workday = request.POST.get('workday_all')
        worktime_start = request.POST['worktime_start']
        worktime_finish = request.POST['worktime_finish']
        worktime_start_weekend = request.POST['worktime_start_weekend']
        worktime_finish_weekend = request.POST['worktime_finish_weekend']
        phone = request.POST['phone']
        address = request.POST['address']
        url_link = request.POST['url_link']
        # 이미지
        pimg = []
        pimg.append(request.POST['pimg1'])
        pimg.append(request.POST['pimg2'])
        pimg.append(request.POST['pimg3'])
        pimg.append(request.POST['pimg4'])
        pimg.append(request.POST['pimg5'])
        pimg.append(request.POST['pimg6'])
        pimg.append(request.POST['pimg7'])
        pimg.append(request.POST['pimg8'])
        pimg.append(request.POST['pimg9'])
        pimg.append(request.POST['pimg10'])
        pimg.append(request.POST['pimg11'])
        pimg.append(request.POST['pimg12'])
        pimg.append(request.POST['pimg13'])
        pimg.append(request.POST['pimg14'])
        pimg.append(request.POST['pimg15'])
        pimg.append(request.POST['pimg16'])
        pimg.append(request.POST['pimg17'])
        pimg.append(request.POST['pimg18'])
        pimg.append(request.POST['pimg19'])
        pimg.append(request.POST['pimg20'])
        # 대표상품 이미지
        rep_img = []
        rep_img.append(request.POST['rep_img1'])
        rep_img.append(request.POST['rep_img2'])
        rep_img.append(request.POST['rep_img3'])
        rep_img.append(request.POST['rep_img4'])
        rep_img.append(request.POST['rep_img5'])
        # 대표상품 설명글
        rep_txt1= request.POST['rep_txt1']
        rep_txt2= request.POST['rep_txt2']
        rep_txt3= request.POST['rep_txt3']
        rep_txt4= request.POST['rep_txt4']
        rep_txt5= request.POST['rep_txt5']
        # 편의시설
        opt = []
        opt.append(request.POST.get('opt1'))
        opt.append(request.POST.get('opt2'))
        opt.append(request.POST.get('opt3'))
        opt.append(request.POST.get('opt4'))
        opt.append(request.POST.get('opt5'))
        opt.append(request.POST.get('opt6'))
        opt.append(request.POST.get('opt7'))
        opt.append(request.POST.get('opt8'))
        opt.append(request.POST.get('opt9'))
        opt.append(request.POST.get('opt10'))
        opt.append(request.POST.get('opt11'))
        opt.append(request.POST.get('opt12'))
        opt.append(request.POST.get('opt13'))
        opt.append(request.POST.get('opt14'))
        opt.append(request.POST.get('opt15'))
        opt.append(request.POST.get('opt16'))
        opt.append(request.POST.get('opt17'))
        opt.append(request.POST.get('opt18'))
        opt.append(request.POST.get('opt19'))
        opt.append(request.POST.get('opt20'))
        content = request.POST['content']
        g_map1 = request.POST['g_map1']
        g_map2 = request.POST['g_map2']
        g_map3 = request.POST['g_map3']
        g_map4 = request.POST['g_map4']
        g_map5 = request.POST['g_map5']

        # 유효성 검사 실패시 기존데이터 저장
        old_data = {'brand_name':brand_name, 'board_kind':board_kind, 'introduction':introduction, 'p_price_min':p_price_min, 'p_price_max':p_price_max,
        'w_price_min':w_price_min, 'w_price_max':w_price_max, 'kakao_id':kakao_id,
        'workday':workday, 'all_workday':all_workday, 'worktime_start':worktime_start, 'worktime_finish':worktime_finish, 'worktime_start_weekend':worktime_start_weekend, 'worktime_finish_weekend':worktime_finish_weekend,
        'phone':phone, 'address':address, 'url_link':url_link, 'pimg':pimg, 'rep_img':rep_img, 'rep_txt1':rep_txt1, 'rep_txt2':rep_txt2, 'rep_txt3':rep_txt3, 'rep_txt4':rep_txt4, 'rep_txt5':rep_txt5,
        'opt':opt, 'content':content, 'g_map1':g_map1, 'g_map2':g_map2, 'g_map3':g_map3, 'g_map4':g_map4, 'g_map5':g_map5
        }
        context['old_data'] = old_data

        # 유효성검사
        val_message = validation(old_data)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            return render(request, 'promotions/create.html', context)

        # 포인트 추가 ( 포인트가 부족하다면 취소 )
        if request.user.point < point['point'] * -1 :
            messages.error(request, "포인트가 부족합니다.")
            return render(request, 'promotions/create.html', context)
        else:
            request.user.point += point['point']
            request.user.exprience += ex['exprience']
            request.user.save()

        # 임시->실제 이미지복사
        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(len(pimg)):
            old_path = pimg[i]
            pimg[i] = pimg[i].replace('temp','promotions')
            os.rename(destination+old_path,destination+pimg[i])
        for i in range(len(rep_img)):
            old_path = rep_img[i]
            rep_img[i] = rep_img[i].replace('temp','promotions')
            os.rename(destination+old_path,destination+rep_img[i])

        # 체크박스데이터 boolean
        for i, ck in enumerate(workday):
            if ck == 'Y':
                workday[i] = True
            else:
                workday[i] = False
        for i, ck in enumerate(opt):
            if ck == 'Y':
                opt[i] = True
            else:
                opt[i] = False

        promotion = Promotion.objects.create(
            user=user, brand_name=brand_name, board_kind=board_kind, introduction=introduction, p_price_min=p_price_min, p_price_max=p_price_max, w_price_min=w_price_min, w_price_max=w_price_max,
            kakao_id=kakao_id, workday_mon=workday[0], workday_tue=workday[1], workday_wed=workday[2], workday_thur=workday[3], workday_fri=workday[4], workday_sat=workday[5], workday_sun=workday[6],
            worktime_start=worktime_start, worktime_finish=worktime_finish, worktime_start_weekend=worktime_start_weekend, worktime_finish_weekend=worktime_finish_weekend, phone=phone, address=address, url_link=url_link,
            pimg1=pimg[0], pimg2=pimg[1], pimg3=pimg[2], pimg4=pimg[3], pimg5=pimg[4], pimg6=pimg[5], pimg7=pimg[6], pimg8=pimg[7], pimg9=pimg[8], pimg10=pimg[9],
            pimg11=pimg[10], pimg12=pimg[11], pimg13=pimg[12], pimg14=pimg[13], pimg15=pimg[14], pimg16=pimg[15], pimg17=pimg[16], pimg18=pimg[17], pimg19=pimg[18], pimg20=pimg[19],
            rep_img1=rep_img[0], rep_img2=rep_img[1], rep_img3=rep_img[2], rep_img4=rep_img[3], rep_img5=rep_img[4], rep_txt1=rep_txt1, rep_txt2=rep_txt2, rep_txt3=rep_txt3, rep_txt4=rep_txt4, rep_txt5=rep_txt5,
            opt1=opt[0], opt2=opt[1], opt3=opt[2], opt4=opt[3], opt5=opt[4], opt6=opt[5], opt7=opt[6], opt8=opt[7], opt9=opt[8], opt10=opt[9],
            opt11=opt[10], opt12=opt[11], opt13=opt[12], opt14=opt[13], opt15=opt[14], opt16=opt[15], opt17=opt[16], opt18=opt[17], opt19=opt[18], opt20=opt[19],
            content=content, g_map1=g_map1, g_map2=g_map2, g_map3=g_map3, g_map4=g_map4, g_map5=g_map5,
        )
        promotion.save()

        # 미리보기인지 작성완료인지 구분
        if preview :
            return redirect(reverse('promotions:preview', args = (promotion.id,)))
        else :
            return redirect('promotions:index')
    else:
        return render(request, 'promotions/create.html', context)

@login_required
def edit(request, promotion_id):
    # 배너 데이터
    banners = promotion_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 수정할 후기데이터
    promotion = get_object_or_404(Promotion, pk=promotion_id)
    # 옵션
    opts = Option.objects.order_by('id').filter(is_published=True)

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'old_data': promotion,
        'opts':opts,
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    # 글저장할 때
    if request.method == 'POST':
        print(request.POST)
        # 데이터저장
        preview = request.POST['preview']
        user = request.user
        if request.user.is_staff == True:
            user = promotion.user
        brand_name = request.POST['brand_name']
        board_kind = request.POST['board_kind']
        introduction = request.POST['introduction']
        p_price_min = request.POST['p_price_min']
        p_price_max = request.POST['p_price_max']
        w_price_min = request.POST['w_price_min']
        w_price_max = request.POST['w_price_max']
        kakao_id = request.POST['kakao_id']
        workday = []
        workday.append(request.POST.get('workday_mon'))
        workday.append(request.POST.get('workday_tue'))
        workday.append(request.POST.get('workday_wed'))
        workday.append(request.POST.get('workday_thur'))
        workday.append(request.POST.get('workday_fri'))
        workday.append(request.POST.get('workday_sat'))
        workday.append(request.POST.get('workday_sun'))
        all_workday = request.POST.get('workday_all')
        worktime_start = request.POST['worktime_start']
        worktime_finish = request.POST['worktime_finish']
        worktime_start_weekend = request.POST['worktime_start_weekend']
        worktime_finish_weekend = request.POST['worktime_finish_weekend']
        phone = request.POST['phone']
        address = request.POST['address']
        url_link = request.POST['url_link']
        # 이미지
        pimg = []
        pimg.append(request.POST['pimg1'])
        pimg.append(request.POST['pimg2'])
        pimg.append(request.POST['pimg3'])
        pimg.append(request.POST['pimg4'])
        pimg.append(request.POST['pimg5'])
        pimg.append(request.POST['pimg6'])
        pimg.append(request.POST['pimg7'])
        pimg.append(request.POST['pimg8'])
        pimg.append(request.POST['pimg9'])
        pimg.append(request.POST['pimg10'])
        pimg.append(request.POST['pimg11'])
        pimg.append(request.POST['pimg12'])
        pimg.append(request.POST['pimg13'])
        pimg.append(request.POST['pimg14'])
        pimg.append(request.POST['pimg15'])
        pimg.append(request.POST['pimg16'])
        pimg.append(request.POST['pimg17'])
        pimg.append(request.POST['pimg18'])
        pimg.append(request.POST['pimg19'])
        pimg.append(request.POST['pimg20'])
        # 대표상품 이미지
        rep_img = []
        rep_img.append(request.POST['rep_img1'])
        rep_img.append(request.POST['rep_img2'])
        rep_img.append(request.POST['rep_img3'])
        rep_img.append(request.POST['rep_img4'])
        rep_img.append(request.POST['rep_img5'])
        # 대표상품 설명글
        rep_txt1= request.POST['rep_txt1']
        rep_txt2= request.POST['rep_txt2']
        rep_txt3= request.POST['rep_txt3']
        rep_txt4= request.POST['rep_txt4']
        rep_txt5= request.POST['rep_txt5']
        # 편의시설
        opt = []
        opt.append(request.POST.get('opt1'))
        opt.append(request.POST.get('opt2'))
        opt.append(request.POST.get('opt3'))
        opt.append(request.POST.get('opt4'))
        opt.append(request.POST.get('opt5'))
        opt.append(request.POST.get('opt6'))
        opt.append(request.POST.get('opt7'))
        opt.append(request.POST.get('opt8'))
        opt.append(request.POST.get('opt9'))
        opt.append(request.POST.get('opt10'))
        opt.append(request.POST.get('opt11'))
        opt.append(request.POST.get('opt12'))
        opt.append(request.POST.get('opt13'))
        opt.append(request.POST.get('opt14'))
        opt.append(request.POST.get('opt15'))
        opt.append(request.POST.get('opt16'))
        opt.append(request.POST.get('opt17'))
        opt.append(request.POST.get('opt18'))
        opt.append(request.POST.get('opt19'))
        opt.append(request.POST.get('opt20'))
        content = request.POST['content']
        g_map1 = request.POST['g_map1']
        g_map2 = request.POST['g_map2']
        g_map3 = request.POST['g_map3']
        g_map4 = request.POST['g_map4']
        g_map5 = request.POST['g_map5']

        # 유효성 검사 실패시 기존데이터 저장
        old_data = {'brand_name':brand_name, 'board_kind':board_kind, 'introduction':introduction, 'p_price_min':p_price_min, 'p_price_max':p_price_max,
        'w_price_min':w_price_min, 'w_price_max':w_price_max, 'kakao_id':kakao_id,
        'workday':workday, 'all_workday':all_workday, 'worktime_start':worktime_start, 'worktime_finish':worktime_finish, 'worktime_start_weekend':worktime_start_weekend, 'worktime_finish_weekend':worktime_finish_weekend,
        'phone':phone, 'address':address, 'url_link':url_link, 'pimg':pimg, 'rep_img':rep_img, 'rep_txt1':rep_txt1, 'rep_txt2':rep_txt2, 'rep_txt3':rep_txt3, 'rep_txt4':rep_txt4, 'rep_txt5':rep_txt5,
        'opt':opt, 'content':content, 'g_map1':g_map1, 'g_map2':g_map2, 'g_map3':g_map3, 'g_map4':g_map4, 'g_map5':g_map5
        }
        context['old_data'] = old_data

        # 유효성검사
        val_message = validation(old_data)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            # return render(request, 'promotions/edit.html', context)
            return redirect(reverse('promotions:edit', args = (promotion_id,)))

        # 임시->실제 이미지복사
        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(len(pimg)):
            old_path = pimg[i]
            pimg[i] = pimg[i].replace('temp','promotions')
            os.rename(destination+old_path,destination+pimg[i])
        for i in range(len(rep_img)):
            old_path = rep_img[i]
            rep_img[i] = rep_img[i].replace('temp','promotions')
            os.rename(destination+old_path,destination+rep_img[i])

        # 체크박스데이터 boolean
        for i, ck in enumerate(workday):
            if ck == 'Y':
                workday[i] = True
            else:
                workday[i] = False
        for i, ck in enumerate(opt):
            if ck == 'Y':
                opt[i] = True
            else:
                opt[i] = False

        promotion.user,promotion.brand_name,promotion.board_kind,promotion.introduction = user, brand_name,board_kind,introduction
        promotion.p_price_min,promotion.p_price_max,promotion.w_price_min,promotion.w_price_max = p_price_min,p_price_max,w_price_min,w_price_max
        promotion.kakao_id,promotion.workday_mon,promotion.workday_tue,promotion.workday_wed,promotion.workday_thur,promotion.workday_fri,promotion.workday_sat,promotion.workday_sun = kakao_id,workday[0],workday[1],workday[2],workday[3],workday[4],workday[5],workday[6]
        promotion.worktime_start,promotion.worktime_finish,promotion.worktime_start_weekend,promotion.worktime_finish_weekend=worktime_start,worktime_finish,worktime_start_weekend,worktime_finish_weekend
        promotion.phone,promotion.address,promotion.url_link=phone,address,url_link
        promotion.pimg1,promotion.pimg2,promotion.pimg3,promotion.pimg4,promotion.pimg5=pimg[0],pimg[1],pimg[2],pimg[3],pimg[4]
        promotion.pimg6,promotion.pimg7,promotion.pimg8,promotion.pimg9,promotion.pimg10=pimg[5],pimg[6],pimg[7],pimg[8],pimg[9]
        promotion.pimg11,promotion.pimg12,promotion.pimg13,promotion.pimg14,promotion.pimg15=pimg[10],pimg[11],pimg[12],pimg[13],pimg[14]
        promotion.pimg16,promotion.pimg17,promotion.pimg18,promotion.pimg19,promotion.pimg20=pimg[15],pimg[16],pimg[17],pimg[18],pimg[19]
        promotion.rep_img1,promotion.rep_img2,promotion.rep_img3,promotion.rep_img4,promotion.rep_img5=rep_img[0],rep_img[1],rep_img[2],rep_img[3],rep_img[4]
        promotion.rep_txt1,promotion.rep_txt2,promotion.rep_txt3,promotion.rep_txt4,promotion.rep_txt5=rep_txt1,rep_txt2,rep_txt3,rep_txt4,rep_txt5
        promotion.opt1,promotion.opt2,promotion.opt3,promotion.opt4,promotion.opt5,promotion.opt6,promotion.opt7,promotion.opt8,promotion.opt9,promotion.opt10=opt[0],opt[1],opt[2],opt[3],opt[4],opt[5],opt[6],opt[7],opt[8],opt[9]
        promotion.opt11,promotion.opt12,promotion.opt13,promotion.opt14,promotion.opt15,promotion.opt16,promotion.opt17,promotion.opt18,promotion.opt19,promotion.opt20=opt[10],opt[11],opt[12],opt[13],opt[14],opt[15],opt[16],opt[17],opt[18],opt[19]
        promotion.content,promotion.g_map1, promotion.g_map2, promotion.g_map3, promotion.g_map4, promotion.g_map5 = content, g_map1, g_map2, g_map3, g_map4, g_map5
        promotion.save()

        # 미리보기인지 작성완료인지 구분
        if preview :
            return redirect(reverse('promotions:preview', args = (promotion.id,)))
        else :
            return redirect('promotions:index')
    else:
        return render(request, 'promotions/edit.html', context)

# 미리보기
@login_required
def preview(request, promotion_id):
    # 배너 데이터
    banners = promotion_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 게시글 데이터
    promotion = get_object_or_404(Promotion, pk=promotion_id)

    # 이미지
    pimg = []
    pimg.append(promotion.pimg1)
    pimg.append(promotion.pimg2)
    pimg.append(promotion.pimg3)
    pimg.append(promotion.pimg4)
    pimg.append(promotion.pimg5)
    pimg.append(promotion.pimg6)
    pimg.append(promotion.pimg7)
    pimg.append(promotion.pimg8)
    pimg.append(promotion.pimg9)
    pimg.append(promotion.pimg10)
    pimg.append(promotion.pimg11)
    pimg.append(promotion.pimg12)
    pimg.append(promotion.pimg13)
    pimg.append(promotion.pimg14)
    pimg.append(promotion.pimg15)
    pimg.append(promotion.pimg16)
    pimg.append(promotion.pimg17)
    pimg.append(promotion.pimg18)
    pimg.append(promotion.pimg19)
    pimg.append(promotion.pimg20)

    time = get_date('nowtime').strftime('%Y-%m-%d:%H')
    new_date = get_date('nowtime').strftime('%Y-%m-%d')

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'pimg':pimg,
        'content': promotion,
        'content_object': '여행사홍보',
        'time': time,
        'new_date': new_date,
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'promotions/preview.html', context)

# 미리보기에서 작성완료시
@login_required
def confirm(request, promotion_id):
    promotion = get_object_or_404(Promotion, pk=promotion_id)
    promotion.is_published = True
    promotion.save()
    return redirect('promotions:index')

# 글삭제시
@login_required
def delete(request, promotion_id):
    promotion = get_object_or_404(Promotion, pk=promotion_id)
    promotion.is_published = False
    promotion.save()
    return redirect('promotions:index')

# 페이지네이션
def pagination_range(promotions, paginator):
    index = promotions.number
    max_index = len(paginator.page_range)

    if index >= 3:
        start_index = index - 3
    else :
        start_index = 0

    if index <= max_index - 2:
        end_index = index + 2
    else :
        end_index = max_index

    page_range = list(paginator.page_range)[start_index:end_index]
    return page_range

# 예약하기 버튼 클릭수 체크
def reserve_chk(request):
    content_id = request.POST['content_id']
    promotion = get_object_or_404(Promotion, pk=content_id)

    #클릭시 숫자증가
    promotion.url_click += 1
    promotion.save()
    # Ajax성공시 링크 Url을 반환
    context = {
        'url': promotion.url_link
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
# 이미지 회전
def img_rotate(request):
    if request.method == 'POST':
        imgurl = request.POST.getlist('arrimg[]')
        destination = settings.MEDIA_ROOT
        for i in imgurl :
            if i:
                afterimg = Image.open(destination+i)
                afterimg = afterimg.rotate(-90,expand=True)
                afterimg.save(destination+i)
        # 전송데이터
        context = {
            'status': 'success',
        }
    else :
        context = {
            'status': 'error'
        }
    return HttpResponse(json.dumps(context), content_type="application/json")

# 파트너쉽
def partnership(request):
    contact_info = request.POST['contact_info']
    content = request.POST['content']
    if len(content) > 499:
        messages.error(request, '내용은 500자 내로 입력해주세요')
        return redirect('promotions:index')

    partnership = PartnerShip.objects.create(
        contact_info=contact_info, content=content
    )
    partnership.save()

    messages.error(request, '감사합니다, 빠른시일내에 회신드리겠습니다.')
    return redirect('promotions:index')

# 별점주기
@login_required
def addstar(request):
    content_id = request.POST['content_id']
    star = request.POST['r_star']
    content_title = request.POST['content_title']

    promotion = get_object_or_404(Promotion, pk=content_id)
    addstar = AddStar.objects.filter(content_name='여행사홍보').filter(user=request.user).filter(content_id=content_id).filter(is_active=True)

    #만약에 참가했었다면 되돌리기 + 알람메세지
    if addstar:
        messages.error(request, '이미 별점평가에 참여하셨습니다.')
        return redirect('promotions:show', promotion_id=content_id)
    # 별점평균
    avg = promotion.avgstar
    num = promotion.numstar
    total = avg * num
    avg = (total+Decimal(star)) / (num+1)

    #content에 저장하기
    promotion.avgstar = avg
    promotion.numstar += 1
    promotion.save()

    #addstar에 추가저장자기
    newstar = AddStar.objects.create(
        user=request.user, score=star, content_name='여행사홍보', content_id=content_id, content_title=content_title
    )
    newstar.save()

    return redirect('promotions:show', promotion_id=content_id)

#댓글좋아요 증가
@login_required
def c_add_like(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']
    content_name = request.POST['content_name']
    content_title = request.POST['content_content'][0:40]
    comment = get_object_or_404(Comment_Promotion, pk=comment_id)

    #클릭시 숫자증가
    comment.likes += 1
    comment.save()

    #좋아요 DB에 데이터추가
    addlike = AddLike.objects.create(
        user=request.user, content_name=content_name, content_id = content_id, comment_id = comment_id, content_title = content_title
    )
    addlike.save()

    # 댓글-좋아요 알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'c_like', likefrom=request.user, comment_user=comment.user, comment_table='여행사홍보댓글',
        board_name='여행사홍보',  board_url='promotions/show/'+str(content_id)+'/'+str(comment_id), content_id = content_id, comment_id = comment_id
    )
    c_alarm.save()

    # Ajax성공시
    context = {
        'message': 'success',
        'comment_id':comment.id,
        'l_num': comment.likes,
        'addlike':addlike.id
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def c_add_unlike(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']

    comment = get_object_or_404(Comment_Promotion, pk=comment_id)
    addLike = AddLike.objects.filter(user=request.user, content_name="여행사홍보댓글", content_id=content_id, comment_id=comment_id).filter(is_active=True).get()

    #클릭시 숫자감소
    comment.likes -= 1
    comment.save()
    #좋아요 is_active False로
    addLike.is_active = False
    addLike.save()

    # Ajax성공시
    context = {
        'message': 'success',
        'comment_id':comment_id,
        'l_num': comment.likes
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
# summernote 이미지 임시저장
def summernote_tmp(request, tag=None):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        # 상품인지 summernote이미지 구분
        tag = request.POST['tag']
        context = {}
        destination = settings.MEDIA_ROOT+'/promotions/temp/'

        # 파일 확장자 체크
        fname ,ext = os.path.splitext(file.name)
        if ext == '.png' or ext == '.jpg' or ext == '.PNG' or ext == '.JPG' or ext == '.JPEG' or ext == '.jpeg':

            #파일이름바꾸기 날짜-유저명.확장자
            nowtime = get_date('nowtime').strftime('%Y%m%d%H%M%S%f')
            user = request.user.username
            filename = nowtime+'_'+user+ext
            file_url = '/media/promotions/temp/'+filename

            # 파일 크기 Resize
            resize_img = Image.open(file)
            # 투명도 확인할수없는 파일 포맷일때
            if resize_img.mode in ("RGBA", "P"):
                resize_img = resize_img.convert("RGB")
            width, height = resize_img.size
            # 세로긴 사진 올리지 못하게
            if tag == 'item_img' and ( height >= (width * 2) or width >= (height * 3) ):
                context = {
                    'status': 'size error'
                }
                return HttpResponse(json.dumps(context), content_type="application/json")

            # 파일크기 줄이기
            if width >= 4000 :
                resize_img = resize_img.resize((int(width/4),int(height/4)))
            elif width >= 2000 :
                resize_img = resize_img.resize((int(width/2),int(height/2)))
            else :
                resize_img = resize_img.resize((width,height))
            # 파일 저장
            resize_img.save(destination+filename)

            # 전송데이터
            context = {
                'status': 'success',
                'img_path': file_url
            }
        else:
            context = {
                'status': 'ext error'
            }
    return HttpResponse(json.dumps(context), content_type="application/json")

#유효성검사
def validation(old_data):
    # 게시판 선택을 하지 않았을시
    print('123123',re.match("^[0-9]*$", old_data['p_price_min']))
    if old_data['brand_name'] == '':
        return '업체명을 작성해주세요.'
    elif old_data['board_kind'] == '':
        return '업종을 선택해주세요.'
    elif old_data['introduction'] == '':
        return '한줄소개를 작성해주세요.'
    elif old_data['p_price_min'] == '' or not re.match("^[0-9]*$", old_data['p_price_min']):
        return '최소가격(페소)은 숫자만 입력가능합니다.'
    elif old_data['p_price_max'] == '' or not re.match("^[0-9]*$", old_data['p_price_max']):
        return '최대가격(페소)은 숫자만 입력가능합니다.'
    elif old_data['w_price_min'] == '' or not re.match("^[0-9]*$", old_data['w_price_min']):
        return '최소예약금(원)은 숫자만 입력가능합니다.'
    elif old_data['w_price_max'] == '' or not re.match("^[0-9]*$", old_data['w_price_max']):
        return '최대예약금(원)은 숫자만 입력가능합니다.'
    # 사진 최소 5장
    # elif old_data['pimg'][0] == '' or old_data['pimg'][1] == '' or old_data['pimg'][2] == '' or old_data['pimg'][3] == '' or old_data['pimg'][4] == '':
    #     return '상품사진을 5장이상 등록해주세요.'
    # # 대표사진 3장
    # elif old_data['rep_img'][0] == '' or old_data['rep_img'][1] == '' or old_data['rep_img'][2] == '':
    #     return '대표상품사진을 3장이상 등록해주세요.'
    # 텍스트
    elif len(old_data['content']) > 500000:
        return '내용의 글자 수를 줄여주세요.'
    # 관련링크
    elif len(old_data['url_link']) > 200:
        return '관련링크의 글자 수를 줄여주세요.'
    else:
        return '유효성검사성공'

# 배너데이터 가져오기
def promotion_banners():
    banners_main = Banner.objects.order_by('position_1').filter(title__contains='메인').filter(is_published=True)
    banner_top = get_object_or_404(banners_main, position_1=0)
    banners_review_right = Banner.objects.order_by('position_1').filter(title__contains='여행사홍보우측').filter(is_published=True)
    # 메뉴배너
    banner_menu = Banner.objects.order_by('position_1').filter(title__contains='메뉴').filter(is_published=True)
    banners = {
        'banner_top': banner_top,
        'banners_review_right': banners_review_right,
        'banner_menu':banner_menu
    }
    return banners

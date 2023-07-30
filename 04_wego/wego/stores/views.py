from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages
from msgboxs.models import Alarm_Addcommentlike
from msgboxs.views import getAlarmListNew
from banners.models import Banner
import os
from pages.models import Point, Exprience
from .models import Store, Store_Main
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import simplejson as json
from django.conf import settings
from pages.views import get_date, uprising_keyword
from PIL import Image
import re
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def index(request, tag='all'):
    # 배너 데이터
    banners = store_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 스토어
    stores = Store.objects.order_by('-upload_date').filter(is_published=True)
    best_stores = Store.objects.order_by('-upload_date').filter(best_published=True).filter(is_published=True)

    # 페이지네이션
    paginator = Paginator(stores, 8)
    page = request.GET.get('page')
    stores = paginator.get_page(page)
    # 페이지네이션 나타낼 번호 제어
    page_range = pagination_range(stores, paginator)

    best_paginator = Paginator(best_stores, 8)
    best_page = request.GET.get('page')
    best_stores = best_paginator.get_page(best_page)
    # 페이지네이션 나타낼 번호 제어
    best_page_range = pagination_range(best_stores, best_paginator)

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'stores': stores,
        'best_stores': best_stores,
        'page_range': page_range,
        'best_page_range': best_page_range,
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'stores/index.html', context)

@csrf_exempt
def create(request):
    # 배너 데이터
    banners = store_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 글쓸시 포인트, 경험치
    point = Point.objects.filter(title='스토어작성').values('point').first()
    ex = Exprience.objects.filter(title='스토어작성').values('exprience').first()

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'point': point,
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    # 글저장할 때
    if request.method == 'POST':
        print(request.POST)
        # 데이터저장
        user = request.user
        title = request.POST['title']
        item_name = request.POST['item_name']
        price = request.POST['price']
        url_link = request.POST['url_link']
        pimg1 = request.POST['pimg1']

        # 유효성 검사 실패시 기존데이터 저장
        old_data = {'title':title ,'item_name':item_name, 'price':price, 'url_link':url_link, 'pimg1':pimg1 }
        context['old_data'] = old_data

        # 유효성검사
        val_message = validation(old_data)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            return render(request, 'stores/create.html', context)

        destination = settings.MEDIA_ROOT.replace("/media", "")
        old_path = pimg1
        pimg1 = pimg1.replace('temp','stores')
        os.rename(destination+old_path,destination+pimg1)

        # 포인트, 경험치 추가
        request.user.point += point['point']
        request.user.exprience += ex['exprience']
        request.user.save()

        store = Store.objects.create(
            user=user, title=title, item_name=item_name, price=price, url_link=url_link, pimg1=pimg1
        )
        store.save()
        return redirect('stores:index')

    else:
        return render(request, 'stores/create.html', context)

@login_required
def delete(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    store.is_published = False
    store.save()
    return redirect('stores:index')

# 페이지네이션
def pagination_range(stores, paginator):
    index = stores.number
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

@csrf_exempt
# summernote 이미지 임시저장
def summernote_tmp(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        destination = settings.MEDIA_ROOT+'/stores/temp/'

        # 파일 확장자 체크
        fname ,ext = os.path.splitext(file.name)
        if ext == '.png' or ext == '.jpg' or ext == '.PNG' or ext == '.JPG' or ext == '.JPEG' or ext == '.jpeg':

            #파일이름바꾸기 날짜-유저명.확장자
            nowtime = get_date('nowtime').strftime('%Y%m%d%H%M%S%f')
            user = request.user.username
            filename = nowtime+'_'+user+ext
            file_url = '/media/stores/temp/'+filename

            # 파일 크기 Resize
            resize_img = Image.open(file)
            # 투명도 확인할수없는 파일 포맷일때
            if resize_img.mode in ("RGBA", "P"):
                resize_img = resize_img.convert("RGB")
            # 파일크기 줄이기
            width, height = resize_img.size
            if width >= 4000 :
                resize_img = resize_img.resize((int(width/10),int(height/10)))
            elif width >= 2000 :
                resize_img = resize_img.resize((int(width/5),int(height/5)))
            elif width >= 500 :
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

def views(request):
    store_id = request.POST['store_id']
    store = get_object_or_404(Store, pk=store_id)
    #클릭시 숫자증가
    store.click_number += 1
    store.save()
    # Ajax성공시 링크 Url을 반환
    context = {
        'url': store.url_link
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

#유효성검사
def validation(old_data):
    if old_data['title'] == '' or len(old_data['title']) > 35:
        return '한줄소개는 1자 이상, 35자 이하로 작성해주세요!'
    elif old_data['item_name']=='' or len(old_data['item_name']) > 10:
        return '상품명은 1자 이상, 10자 이하로 작성해주세요!'
    elif old_data['price']=='' or len(old_data['price']) > 20:
        return '최소상품가격란을 확인해주세요'
    elif not re.match("^[0-9]*$", old_data['price']):
        return '최소상품가격은 숫자만 입력해주세요'
    elif old_data['pimg1']=='':
        return '이미지를 삽입해주세요.'
    elif old_data['url_link']=='' or len(old_data['url_link']) > 200:
        return '사이트링크란을 확인해주세요'
    else:
        return '유효성검사성공'

# 배너데이터 가져오기
def store_banners():
    banners_main = Banner.objects.order_by('position_1').filter(title__contains='메인').filter(is_published=True)
    banner_top = get_object_or_404(banners_main, position_1=0)
    banners_slide_main = Banner.objects.order_by('position_1').filter(title__contains='스토어슬라이드탑').filter(is_published=True)
    banners_slide_side = Banner.objects.order_by('position_1').filter(title__contains='스토어슬라이드사이드').filter(is_published=True)
    banners_store = Banner.objects.order_by('position_1').filter(title__contains='스토어하단').filter(is_published=True)
    # 메뉴배너
    banner_menu = Banner.objects.order_by('position_1').filter(title__contains='메뉴').filter(is_published=True)
    banners = {
        'banner_top': banner_top,
        'banners_slide_main': banners_slide_main,
        'banners_slide_side': banners_slide_side,
        'banners_store':banners_store,
        'banner_menu':banner_menu
    }
    return banners

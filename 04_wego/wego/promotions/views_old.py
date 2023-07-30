import os
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from banners.models import Banner
from pages.models import AddLike, AddStar, Point, Exprience, PartnerShip
from .models import Promotion
from comments.models import Comment_Promotion
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from pages.views import get_date
from django.contrib import messages
from PIL import Image
import re
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from datetime import datetime, timedelta
from msgboxs.models import Alarm_Addcommentlike
from msgboxs.views import getAlarmListNew

def index(request, tag=None):
    # 배너 데이터
    banners = promotion_banners()
    # 여행사홍보
    # promotions_obj = Promotion.objects.order_by('attribute', '-upload_date').filter(is_published=True)
    # bests = Promotion.objects.order_by('avgstar').filter(best_published=True).filter(is_published=True)
    # board_kind = 'all'
    # # 상단태그맵핑 클릭시
    # # if tag == 'best':
    # #     promotions_obj = promotions_obj.filter(best_published=True)
    # #     board_kind = 'best'
    # if tag == 'tour':
    #     promotions_obj = promotions_obj.filter(board_kind='여행사')
    #     board_kind = 'tour'
    # elif tag == 'hopping':
    #     promotions_obj = promotions_obj.filter(board_kind='호핑')
    #     board_kind = 'hopping'
    # elif tag == 'diving':
    #     promotions_obj = promotions_obj.filter(board_kind='다이빙')
    #     board_kind = 'diving'
    # elif tag == 'hotel':
    #     promotions_obj = promotions_obj.filter(board_kind='숙소')
    #     board_kind = 'hotel'
    # elif tag == 'food':
    #     promotions_obj = promotions_obj.filter(board_kind='맛집')
    #     board_kind = 'food'
    # elif tag == 'massageBeauty':
    #     promotions_obj = promotions_obj.filter(board_kind='마사지/뷰티')
    #     board_kind = 'massageBeauty'
    # elif tag == 'etc':
    #     promotions_obj = promotions_obj.filter(board_kind='기타')
    #     board_kind = 'etc'
    # # 파트너쉽일때
    # elif tag == 'partner':
    #     board_kind = 'partner'
    #
    # # 페이지네이션
    # paginator = Paginator(promotions_obj, 5)
    # page = request.GET.get('page')
    # promotions = paginator.get_page(page)
    # # 페이지네이션 나타낼 번호 제어
    # page_range = pagination_range(promotions, paginator)
    #
    # # 글작성일을 나타낼 때 날짜 or 몇분전으로 나타내기 위한 변수
    # time = get_date('nowtime').strftime('%Y-%m-%d:%H')
    # new_date = get_date('nowtime').strftime('%Y-%m-%d')

    context = {
        'banners': banners,
        # 'promotions':promotions,
        # 'bests':bests,
        # 'board_kind':board_kind,
        # 'time':time,
        # 'new_date': new_date,
        # 'page_range': page_range,
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'promotions/index.html', context)

def show(request, promotion_id, comment_id=None):
    # 배너 데이터
    banners = promotion_banners()
    # 게시글 데이터
    promotion = get_object_or_404(Promotion, pk=promotion_id)
    # 게시글의 댓글 데이터
    comments = promotion.comment_promotion_set.all().order_by('upload_date').filter(is_published=True)
    # 게시글의 태그 데이터
    board_kind = promotion.board_kind
    # 댓글쓸시 포인트
    point = Point.objects.filter(title='여행사홍보댓글').values('point').first()

    # 게시글에 대한 회원의 좋아요 여부
    if request.user.id != None:
        addstar = AddStar.objects.filter(content_name='여행사홍보').filter(user=request.user).filter(content_id=promotion_id).filter(is_active=True)
        if addstar.exists():
            addstar = addstar[0]
    else :
        addstar = False

    # 해당 게시글의 댓글들에 대한 회원의 좋아요 여부
    if request.user.id != None:
        c_addlikes = AddLike.objects.filter(user=request.user).filter(content_name='여행사홍보댓글').filter(content_id=promotion_id).filter(is_active=True).values_list('comment_id',flat=True)
        c_addlikes = list(c_addlikes)
    else :
        c_addlikes = False

    # 게시글 조회수 증가
    promotion.views += 1
    promotion.save()
    # 글작성일을 나타낼 때 날짜 or 몇분전으로 나타내기 위한 변수
    time = get_date('nowtime').strftime('%Y-%m-%d:%H')
    new_date = get_date('nowtime').strftime('%Y-%m-%d')
    # 게시글이 댓글 쓴후에 보여질시
    comment_id = comment_id
    # 우측레이아웃데이터
    rights = right_index()

    context = {
        'banners': banners,
        'board_kind':board_kind,
        'content': promotion,
        'content_object': '여행사홍보',
        'addstar': addstar,
        'c_addlikes': c_addlikes,
        'comments': comments,
        'point' :point,
        'pre_page': request.META.get('HTTP_REFERER'),
        'time': time,
        'new_date': new_date,
        'comment_id': comment_id,
        'rights':rights
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'promotions/show.html', context)

@login_required
def create(request, tag=None):
    # 배너 데이터
    banners = promotion_banners()
    # 우측레이아웃데이터
    rights = right_index()
    # 글쓸시 포인트
    point = Point.objects.filter(title='여행사홍보작성').values('point').first()
    ex = Exprience.objects.filter(title='여행사홍보작성').values('exprience').first()

    context = {
        'banners': banners,
        'rights': rights,
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
        user = request.user
        board_kind = request.POST['board_kind']
        title = request.POST['title']
        content = request.POST['content']
        g_map1 = request.POST['g_map1']
        g_map2 = request.POST['g_map2']
        g_map3 = request.POST['g_map3']
        g_map4 = request.POST['g_map4']
        g_map5 = request.POST['g_map5']
        url_link = request.POST['url_link']
        show_ad = Banner.objects.get(title='여행사홍보상세보기배너_1')

        # 유효성 검사 실패시 기존데이터 저장
        old_data = {'title':title, 'content':content, 'g_map1':g_map1, 'g_map2':g_map2,
        'g_map3':g_map3, 'g_map4':g_map4, 'g_map5':g_map5,'url_link':url_link, 'board_kind':board_kind}
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

        # 임시이미지 실제이미지로
        pattern = re.compile ('<img [^>]*src="([^"]+)')
        old_img = pattern.findall(content)
        # Content에 실제 이미지파일로 맵핑 바꾸기
        content = content.replace('/media/promotions/temp/', '/media/promotions/promotions/')
        new_img = pattern.findall(content)

        # 임시->실제 이미지복사
        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(0, len(new_img)):
            os.rename(destination+old_img[i],destination+new_img[i])

        # 이미지여부판단
        is_imaged = False
        if new_img :
            is_imaged = True

        promotion = Promotion.objects.create(
            user=user, board_kind=board_kind, title=title, content=content,
            g_map1=g_map1, g_map2=g_map2, g_map3=g_map3, g_map4=g_map4, g_map5=g_map5,
            url_link=url_link, show_ad=show_ad, is_imaged=is_imaged
        )
        promotion.save()
        return redirect('promotions:index')
    else:
        return render(request, 'promotions/create.html', context)

@login_required
def edit(request, promotion_id):
    # 배너 데이터
    banners = promotion_banners()
    # 수정할 후기데이터
    promotion = get_object_or_404(Promotion, pk=promotion_id)
    # 우측레이아웃데이터
    rights = right_index()

    context = {
        'banners': banners,
        'old_data': promotion,
        'rights': rights
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    # 글수정할 때
    if request.method == 'POST':
        print(request.POST)
        # 데이터저장
        user = request.user
        board_kind = request.POST['board_kind']
        title = request.POST['title']
        content = request.POST['content']
        g_map1 = request.POST['g_map1']
        g_map2 = request.POST['g_map2']
        g_map3 = request.POST['g_map3']
        g_map4 = request.POST['g_map4']
        g_map5 = request.POST['g_map5']
        url_link = request.POST['url_link']

        # 유효성 검사 실패시 기존데이터 저장
        old_data = {'id':promotion.id, 'title':title, 'content':content, 'g_map1':g_map1, 'g_map2':g_map2, 'g_map3':g_map3,
            'g_map4':g_map4, 'g_map5':g_map5, 'url_link':url_link, 'board_kind':board_kind}
        context['old_data'] = old_data

        # 유효성검사
        val_message = validation(old_data)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            return render(request, 'promotions/edit.html', context)

        # 임시이미지 실제이미지로
        pattern = re.compile ('<img [^>]*src="([^"]+)')
        old_img = pattern.findall(content)
        # Content에 실제 이미지파일로 맵핑 바꾸기
        content = content.replace('/media/promotions/temp/', '/media/promotions/promotions/')
        new_img = pattern.findall(content)

        # 임시->실제 이미지복사
        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(0, len(new_img)):
            os.rename(destination+old_img[i],destination+new_img[i])

        # 이미지여부판단
        is_imaged = False
        if new_img :
            is_imaged = True

        promotion.user, promotion.board_kind = user, board_kind
        promotion.title, promotion.content = title, content
        promotion.g_map1, promotion.g_map2, promotion.g_map3, promotion.g_map4, promotion.g_map5 = g_map1, g_map2, g_map3, g_map4, g_map5
        promotion.url_link, promotion.is_imaged = url_link, is_imaged
        promotion.save()
        return redirect('promotions:index')
    else:
        return render(request, 'promotions/edit.html', context)

@login_required
def delete(request, promotion_id):
    promotion = get_object_or_404(Promotion, pk=promotion_id)
    promotion.is_published = False
    promotion.save()
    return redirect('promotions:index')

# 우측 레이아웃관련 데이터
def right_index():
    # 한달동안 가장 많이본
    last_month = datetime.today() - timedelta(days=30)
    right_bests = Promotion.objects.filter(upload_date__gte=last_month).order_by('-views').filter(is_published=True)
    right_news = Promotion.objects.order_by('-upload_date').filter(is_published=True)
    right_comments = Comment_Promotion.objects.order_by('-upload_date').filter(is_published=True)
    rights = {
        'right_bests': right_bests,
        'right_news': right_news,
        'right_comments': right_comments,
    }
    return rights

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
def summernote_tmp(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        destination = settings.MEDIA_ROOT+'/promotions/temp/'

        # 파일 확장자 체크
        fname ,ext = os.path.splitext(file.name)
        if ext == '.png' or ext == '.jpg' or ext == '.PNG' or ext == '.JPG':

            #파일이름바꾸기 날짜-유저명.확장자
            nowtime = get_date('nowtime').strftime('%Y%m%d%H%M%S%f')
            user = request.user.username
            filename = nowtime+'_'+user+ext
            file_url = '/media/promotions/temp/'+filename

            # 파일 크기 Resize
            resize_img = Image.open(file)
            width, height = resize_img.size
            if width > 4000 :
                resize_img = resize_img.resize((int(width/4),int(height/4)))
            elif width > 2000 :
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
    if old_data['board_kind'] == '':
        return '작성할 게시판을 선택해주세요.'
    # 제목
    elif old_data['title'] == '' or len(old_data['title']) > 35:
        return '제목는 0-35글자로 입력해주세요.'
    # 텍스트
    elif len(old_data['content']) > 500000:
        return '내용의 글자 수를 줄여주세요.'
    # 관련링크
    elif len(old_data['url_link']) > 200:
        return '관련링크의 글자 수를 줄여주세요.'
    # 이미지 갯수
    # elif old_data['content'].count("src=\"/media/") > 20:
    #     return '이미지는 최대 20개 업로드가능합니다.'
    else:
        return '유효성검사성공'

# 배너데이터 가져오기
def promotion_banners():
    banners_main = Banner.objects.order_by('position_1').filter(title__contains='메인').filter(is_published=True)
    banner_top = get_object_or_404(banners_main, position_1=0)
    # banners_review_left = Banner.objects.order_by('position_1').filter(title__contains='여행사홍보좌측').filter(is_published=True)
    banners_review_right = Banner.objects.order_by('position_1').filter(title__contains='여행사홍보우측').filter(is_published=True)
    banners = {
        'banner_top': banner_top,
        'banners_review_right': banners_review_right
    }
    return banners

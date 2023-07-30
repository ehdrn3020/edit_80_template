import os
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from banners.models import Banner
from pages.models import AddLike, Point, Exprience, PartnerShip
from .models import Notice, CustomerCenter
from comments.models import Comment_Notice, Comment_CustomerCenter
from django.contrib.auth.decorators import login_required
import simplejson as json
import re
from django.conf import settings
from pages.views import get_date, uprising_keyword
from django.contrib import messages
from PIL import Image
import re
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from datetime import datetime, timedelta
from msgboxs.models import Alarm_Addcommentlike
from msgboxs.views import getAlarmListNew

from .models import WegoQuiz
from .models import WegoRoulette
from random import *


def index(request, kind='notice'):
    # 배너 데이터
    banners = center_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    obj = ''
    board_kind = 'notice'
    # 공지사항
    if kind == 'notice':
        obj = Notice.objects.order_by('-upload_date').filter(is_published=True)
        board_kind = 'notice'
    elif kind == 'customerCenter':
        obj = CustomerCenter.objects.order_by('-upload_date').filter(is_published=True)
        board_kind = 'customerCenter'

    # 검색창
    s_select = request.GET.get('sch_slt')
    s_text = request.GET.get('sch_tx')
    if s_select != None:
        if s_select == '제목':
            obj = obj.filter(title__contains=s_text)
        else :
            obj = obj.filter(user__username__contains=s_text)

    # 페이지네이션
    paginator = Paginator(obj, 20)
    page = request.GET.get('page')
    centers = paginator.get_page(page)
    # 페이지네이션 나타낼 번호 제어
    page_range = pagination_range(centers, paginator)
    # 우측레이아웃데이터
    rights = right_index()

    # 글작성일을 나타낼 때 날짜 or 몇분전으로 나타내기 위한 변수
    time = get_date('nowtime').strftime('%Y-%m-%d:%H')
    new_date = get_date('nowtime').strftime('%Y-%m-%d')

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'centers':centers,
        'board_kind':board_kind,
        's_select':s_select,
        's_text':s_text,
        'time':time,
        'new_date': new_date,
        'page_range': page_range,
        'rights': rights
    }

    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'centers/index.html', context)

def show(request, kind, center_id, comment_id=None):
    # 배너 데이터
    banners = center_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 게시글, 댓글, 댓글쓸시포인트 데이터, 태그데이터
    obj = ''
    comments = ''
    point = ''
    board_kind = ''
    if kind == 'notice' or '공지사항':
        obj = get_object_or_404(Notice, pk=center_id)
        comments = obj.comment_notice_set.all().order_by('upload_date').filter(is_published=True)
        point = Point.objects.filter(title='공지사항댓글').values('point').first()
        board_kind = obj.board_kind # 공지사항
        # 게시글 조회수 증가
        obj.views += 1
        obj.save()
    elif kind == 'customerCenter' or '고객센터':
        obj = get_object_or_404(CustomerCenter, pk=center_id)
        comments = obj.comment_customercenter_set.all().order_by('upload_date').filter(is_published=True)
        point = Point.objects.filter(title='고객센터댓글').values('point').first()
        board_kind = obj.board_kind # 공지사항
        # 게시글 조회수 증가
        obj.views += 1
        obj.save()

    # 게시글에 대한 회원의 좋아요 여부
    if request.user.id != None:
        addlike = AddLike.objects.filter(user=request.user).filter(content_name=board_kind).filter(content_id=center_id).filter(is_active=True)
        if addlike.exists():
            addlike = addlike[0]
    else :
        addlike = AddLike.objects.filter(user=None).filter(content_name=board_kind).filter(content_id=center_id).filter(is_active=True)

    # 글작성일을 나타낼 때 날짜 or 몇분전으로 나타내기 위한 변수
    time = get_date('nowtime').strftime('%Y-%m-%d:%H')
    new_date = get_date('nowtime').strftime('%Y-%m-%d')
    # 게시글이 댓글 쓴후에 보여질시
    comment_id = comment_id
    # 우측레이아웃데이터
    rights = right_index()

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'board_kind':board_kind,
        'content': obj,
        'content_object': board_kind,
        'addlike': addlike,
        'kind': kind,
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

    return render(request, 'centers/show.html', context)

@login_required
def create(request, kind):
    # 배너 데이터
    banners = center_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 우측레이아웃데이터
    rights = right_index()
    # 글쓸시 포인트, 경험치
    point = Point.objects.filter(title='고객센터작성').values('point').first()
    ex = Exprience.objects.filter(title='고객센터작성').values('exprience').first()

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'rights': rights,
        'point': point,
        'board_kind': kind
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
        show_ad = Banner.objects.get(title='위고센터상세보기배너_1')
        url_link = ''
        secret = ''
        old_data = ''
        if kind == 'notice':
            tag = request.POST['tag']
            url_link = request.POST['url_link']
            # 유효성 검사 실패시 기존데이터 저장
            old_data = {'tag':tag, 'title':title, 'content':content, 'url_link':url_link, 'board_kind':board_kind}
        elif kind == 'customerCenter':
            secret = request.POST['secret']
            # 유효성 검사 실패시 기존데이터 저장
            old_data = {'title':title, 'content':content, 'secret':secret, 'board_kind':board_kind}

        context['old_data'] = old_data
        # 유효성검사
        val_message = validation(old_data, board_kind)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            return render(request, 'centers/create.html', context)

        # 임시이미지 실제이미지로
        pattern = re.compile ('<img [^>]*src="([^"]+)')
        old_img = pattern.findall(content)
        # Content에 실제 이미지파일로 맵핑 바꾸기
        content = content.replace('/media/centers/temp/', '/media/centers/centers/')
        new_img = pattern.findall(content)

        # 임시->실제 이미지복사
        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(0, len(new_img)):
            os.rename(destination+old_img[i],destination+new_img[i])

        # 이미지여부판단
        is_imaged = False
        if new_img :
            is_imaged = True

        # 포인트,경험치 추가
        request.user.point += point['point']
        request.user.exprience += ex['exprience']
        request.user.save()

        # 게시글저장
        if board_kind == '공지사항':
            obj = Notice.objects.create(
                user=user, board_kind=board_kind, tag=tag, title=title, content=content,
                url_link=url_link, show_ad=show_ad, is_imaged=is_imaged
            )
            obj.save()
            return redirect('centers:index', 'notice')
        elif board_kind == '고객센터':
            if secret == '비공개':
                secret = True
            else :
                secret = False
            obj = CustomerCenter.objects.create(
                user=user, board_kind=board_kind, title=title, content=content,
                secret=secret, show_ad=show_ad, is_imaged=is_imaged
            )
            obj.save()
            return redirect('centers:index', 'customerCenter')

    # 페이지보여줄때
    else:
        return render(request, 'centers/create.html', context)

@login_required
def edit(request, kind, center_id):
    # 배너 데이터
    banners = center_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 우측레이아웃데이터
    rights = right_index()
    # 수정할 후기데이터
    obj = get_object_or_404(CustomerCenter, pk=center_id)
    if kind == 'notice':
        obj = get_object_or_404(Notice, pk=center_id)

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'old_data': obj,
        'rights': rights,
        'board_kind': kind
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    # 글수정할 때
    if request.method == 'POST':
        print(request.POST)
        # 데이터저장
        user = request.user
        if request.user.is_staff == True:
            user = obj.user
        board_kind = request.POST['board_kind']
        title = request.POST['title']
        content = request.POST['content']
        tag = ''
        url_link = ''
        secret = ''

        if kind == 'notice':
            tag = request.POST['tag']
            url_link = request.POST['url_link']
            # 유효성 검사 실패시 기존데이터 저장
            old_data = {'tag':tag, 'title':title, 'content':content, 'url_link':url_link, 'board_kind':board_kind}
        elif kind == 'customerCenter':
            secret = request.POST['secret']
            # 유효성 검사 실패시 기존데이터 저장
            old_data = {'title':title, 'content':content, 'secret':secret, 'board_kind':board_kind}
        print(secret)
        context['old_data'] = old_data

        # 유효성검사
        val_message = validation(old_data, board_kind)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            return render(request, 'centers/create.html', context)

        # 임시이미지 실제이미지로
        pattern = re.compile ('<img [^>]*src="([^"]+)')
        old_img = pattern.findall(content)
        # Content에 실제 이미지파일로 맵핑 바꾸기
        content = content.replace('/media/centers/temp/', '/media/centers/centers/')
        new_img = pattern.findall(content)

        # 임시->실제 이미지복사
        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(0, len(new_img)):
            os.rename(destination+old_img[i],destination+new_img[i])

        # 이미지여부판단
        is_imaged = False
        if new_img :
            is_imaged = True

        # 게시글저장
        if board_kind == '공지사항':
            obj.user, obj.board_kind, obj.tag, obj.title, obj.content, obj.url_link, obj.is_imaged = user, board_kind, tag, title, content, url_link, is_imaged
            obj.save()
            return redirect('centers:index', 'notice')
        elif board_kind == '고객센터':
            if secret == '비공개':
                secret = True
            else :
                secret = False
            obj.user, obj.board_kind, obj.title, obj.content, obj.secret, obj.is_imaged = user, board_kind, title, content, secret, is_imaged
            obj.save()
            return redirect('centers:index', 'customerCenter')
    else:
        return render(request, 'centers/edit.html', context)

@login_required
def delete(request, kind, center_id):
    if kind == 'notice':
        obj = get_object_or_404(Notice, pk=center_id)
        obj.is_published = False
        obj.save()
        return redirect('centers:index', 'notice')
    elif kind == 'customerCenter':
        obj = get_object_or_404(CustomerCenter, pk=center_id)
        obj.is_published = False
        obj.save()
        return redirect('centers:index', 'customerCenter')

# 우측 레이아웃관련 데이터
def right_index():
    # 한달동안 가장 많이본
    last_month = datetime.today() - timedelta(days=30)
    right_bests = Notice.objects.filter(upload_date__gte=last_month).order_by('-views').filter(is_published=True)
    right_news = Notice.objects.order_by('-upload_date').filter(is_published=True)
    right_comments = Comment_Notice.objects.order_by('-upload_date').filter(is_published=True)
    rights = {
        'right_bests': right_bests,
        'right_news': right_news,
        'right_comments': right_comments,
    }
    return rights

# 페이지네이션
def pagination_range(centers, paginator):
    index = centers.number
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
        destination = settings.MEDIA_ROOT+'/centers/temp/'

        # 파일 확장자 체크
        fname ,ext = os.path.splitext(file.name)
        if ext == '.png' or ext == '.jpg' or ext == '.PNG' or ext == '.JPG':

            #파일이름바꾸기 날짜-유저명.확장자
            nowtime = get_date('nowtime').strftime('%Y%m%d%H%M%S%f')
            user = request.user.username
            filename = nowtime+'_'+user+ext
            file_url = '/media/centers/temp/'+filename

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
def validation(old_data, board_kind):
    # 게시판 선택을 하지 않았을시
    if old_data['board_kind'] == '':
        return '작성할 게시판을 선택해주세요.'
    # 제목
    elif old_data['title'] == '' or len(old_data['title']) > 35:
        return '제목는 0-35글자로 입력해주세요.'
    # 텍스트
    elif len(old_data['content']) > 500000:
        return '내용의 글자 수를 줄여주세요.'
    elif board_kind == '공지사항':
        # 태그
        if len(old_data['tag']) > 40:
            return '관련링크의 글자 수를 줄여주세요.'
        # 관련링크
        elif len(old_data['url_link']) > 200:
            return '관련링크의 글자 수를 줄여주세요.'
        else:
            return '유효성검사성공'
    else:
        return '유효성검사성공'

#좋아요 증가
@login_required
def add_like(request):
    content_name = request.POST['content_name'] # 공지사항
    content_id = request.POST['content_id']
    content_title = request.POST['content_title']
    kind = request.POST['kind'] #notice
    obj = ''
    board_url = ''

    if content_name == '공지사항':
        obj = get_object_or_404(Notice, pk=content_id)
        #클릭시 숫자증가
        obj.likes += 1
        obj.save()
    elif content_name == '고객센터':
        obj = get_object_or_404(CustomerCenter, pk=content_id)
        #클릭시 숫자증가
        obj.likes += 1
        obj.save()

    #좋아요 DB에 데이터추가
    addlike = AddLike.objects.create(
        user=request.user, content_name=content_name, content_id = content_id, content_title = content_title
    )
    addlike.save()

    # 댓글-좋아요 알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'like', likefrom=request.user, comment_user=obj.user, comment_table=content_name,
        board_name=content_name,board_url='centers/show/'+kind+'/'+str(content_id), content_id = content_id
    )
    c_alarm.save()

    # Ajax성공시
    context = {
        'message': 'success',
        'addlike_id':addlike.id,
        'l_num': obj.likes
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def add_unlike(request):
    content_id = request.POST['content_id']
    like_id = request.POST['like_id']
    content_name = request.POST['content_name']

    obj = ''
    if content_name == '공지사항':
        obj = get_object_or_404(Notice, pk=content_id)
        #클릭시 숫자감소
        obj.likes -= 1
        obj.save()
    elif content_name == '고객센터':
        obj = get_object_or_404(CustomerCenter, pk=content_id)
        #클릭시 숫자감소
        obj.likes -= 1
        obj.save()

    #좋아요 is_active False로
    addLike = get_object_or_404(AddLike, pk=like_id)
    addLike.is_active = False
    addLike.save()

    # Ajax성공시
    context = {
        'message': 'success',
        'l_num': obj.likes
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

# 파트너쉽
def partnership(request):
    # 배너 데이터
    banners = center_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    if request.method == 'POST':
        contact_info = request.POST['contact_info']
        content = request.POST['content']
        if len(content) > 499:
            messages.error(request, '내용은 500자 내로 입력해주세요')
            return redirect('centers:partnership')

        partnership = PartnerShip.objects.create(
            contact_info=contact_info, content=content
        )
        partnership.save()

        messages.error(request, '감사합니다, 빠른시일내에 회신드리겠습니다.')
        return redirect('centers:partnership')
    else:
        return render(request, 'centers/partnership.html', context)

# 위고퀴즈 업데이트
def wego_quiz(request):
    user = request.user
    # 로그인 여부 확인
    if user.is_authenticated:
        # 이미 참여했다면 예외처리
        today = get_date('today')
        if WegoQuiz.objects.filter(apply_date__icontains=today).filter(username=user).exists():
            # 메세지를 보낸다
            messages.error(request, '이미 오늘 참가하셨습니다. 내일 다시 도전하세요!')
            return redirect('pages:index')
        # 오늘 처음 참여한다면
        else:
            # 해당 계정에 포인트, 경험치 추가
            p = Point.objects.filter(title='세부퀴즈').values('point').first()
            e = Exprience.objects.filter(title='세부퀴즈').values('exprience').first()
            user.point += p['point']
            user.exprience += e['exprience']
            user.save()
            # 스토어활동 히스토리에 저장
            nowtime = datetime.now()
            WegoQuiz.objects.create(
                username = user.username,
                title = '세부퀴즈',
                get_point = p['point'],
                apply_date= nowtime
            )
            messages.error(request, str(p['point']) + '포인트를 획득하셨습니다.')
            return redirect('pages:index')
    else:
        messages.error(request, '로그인 후 참여하실 수 있습니다!')
        return redirect('pages:index')

# 위고룰렛 URL넘기기
def wego_roulette(request):
    return render(request, 'centers/roulette.html')

# 위고룰렛 생성
def wego_roulette_create(request):
    mode = request.POST['mode']
    # 룰렛변수 선언
    r_point = ['20P', '30P', '50P', '100P', '200P', '다음기회에']
    i = randint(0, 5)
    deg = -1
    message = ""
    p = 0

    if mode == 'create' and request.method == 'POST':
        # 로그인체크
        user = request.user
        if user.is_authenticated:
            # 오늘참여여부 확인
            today = get_date('today')
            if WegoRoulette.objects.filter(apply_date__icontains=today).filter(username=user).exists():
                # 메세지를 보낸다
                message = '오늘 이미 참여하셨습니다. 내일 다시 도전해주세요!'

            # 오늘 처음 참여면 포인트랜덤선택
            else :
                if r_point[i] == '20P':
                    deg = randint(275, 325)
                    p = 20
                    message = '20포인트를 획득하셨습니다.'
                elif r_point[i] == '30P':
                    deg = randint(215, 265)
                    p = 30
                    message = '30포인트를 획득하셨습니다.'
                elif r_point[i] == '50P':
                    deg = randint(155, 205)
                    p = 50
                    message = '50포인트를 획득하셨습니다.'
                elif r_point[i] == '100P':
                    deg = randint(95, 145)
                    p = 100
                    message = '100포인트를 획득하셨습니다.'
                elif r_point[i] == '200P':
                    deg = randint(35, 85)
                    p = 200
                    message = '200포인트를 획득하셨습니다.'
                else :
                    p = 0
                    message = '아쉽지만, 다음기회에ㅠㅠ!'
                    if randint(0,1):
                        deg = randint(0,25)
                    else :
                        deg = randint(335,360)

                # 8-10바퀴 돌림
                deg += 360 * randint(8,10)
                print(p, deg)

                # 해당 계정에 포인트, 경험치 추가
                p = Point.objects.filter(title='세부룰렛_'+str(i+1)).values('point').first()
                e = Exprience.objects.filter(title='세부룰렛').values('exprience').first()
                user.point += p['point']
                user.exprience += e['exprience']
                user.save()

                # 스토어활동 히스토리에 저장
                nowtime = datetime.now()
                WegoRoulette.objects.create(
                    username = user.username,
                    title = '세부룰렛',
                    get_point = p['point'],
                    apply_date= nowtime
                )
        else :
            message = '로그인 후 참여하실 수 있습니다!'
    else :
        message = '잘못된 접근입니다.'

    # Ajax성공시 링크 Url을 반환
    context = {
        'point': r_point[i],
        'degree': deg,
        'message': message,
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

# 배너데이터 가져오기
def center_banners():
    banners_main = Banner.objects.order_by('position_1').filter(title__contains='메인').filter(is_published=True)
    banner_top = get_object_or_404(banners_main, position_1=0)
    banners_review_left = Banner.objects.order_by('position_1').filter(title__contains='위고센터좌측').filter(is_published=True)
    banners_review_right = Banner.objects.order_by('position_1').filter(title__contains='위고센터우측').filter(is_published=True)
    # 쇼핑배너
    from pages.views import shop_banners
    banner_shops = shop_banners()
    # 메뉴배너
    banner_menu = Banner.objects.order_by('position_1').filter(title__contains='메뉴').filter(is_published=True)
    banners = {
        'banner_top': banner_top,
        'banners_review_left': banners_review_left,
        'banners_review_right': banners_review_right,
        'banner_shops':banner_shops,
        'banner_menu':banner_menu
    }
    return banners

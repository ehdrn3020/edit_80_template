import os
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse
from banners.models import Banner
from pages.models import AddLike
from pages.models import Point, Exprience
from .models import Gallery
from comments.models import Comment_Gallery
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import simplejson as json
from django.core import serializers
from django.conf import settings
from pages.views import get_date, uprising_keyword
from django.contrib import messages
from PIL import Image
import re
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from msgboxs.models import Alarm_Addcommentlike
from msgboxs.views import getAlarmListNew

def index(request, tag=None):
    # 배너데이터
    banners = gallery_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'

    # 갤러리
    gallerys_obj = Gallery.objects.order_by('-upload_date').filter(is_published=True)
    gbests = gallerys_obj.order_by('-views').filter(best_published=True).filter(is_published=True)
    board_kind = 'all'
    # 상단태그맵핑 클릭시
    if tag == 'tour':
        gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='여행샷').filter(is_published=True)
        board_kind = 'tour'
    elif tag == 'food':
        gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='음싯샷').filter(is_published=True)
        board_kind = 'food'
    elif tag == 'hotel':
        gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='숙소샷').filter(is_published=True)
        board_kind = 'hotel'
    elif tag == 'shopping':
        gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='쇼핑샷').filter(is_published=True)
        board_kind = 'shopping'
    elif tag == 'airport':
        gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='공항샷').filter(is_published=True)
        board_kind = 'airport'

    context = {
        'banners':banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'gallerys':gallerys_obj,
        'gbests': gbests,
        'board_kind':board_kind,
    }

    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'gallerys/index.html',context)

def show(request, gallery_id, comment_id=None):
    # 배너 데이터
    banners = gallery_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 게시글 데이터
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    # 게시글의 댓글 데이터
    comments = gallery.comment_gallery_set.all().order_by('upload_date').filter(is_published=True)
    # 게시글의 태그 데이터
    board_kind = gallery.board_kind
    # 댓글쓸시 포인트
    point = Point.objects.filter(title='실시간세부댓글').values('point').first()

    # 게시글에 대한 회원의 좋아요 여부
    if request.user.id != None:
        addlike = AddLike.objects.filter(user=request.user).filter(content_name='실시간세부').filter(content_id=gallery_id).filter(is_active=True)
        if addlike.exists():
            addlike = addlike[0]
    else :
        addlike = False
    # 해당 게시글의 댓글들에 대한 회원의 좋아요 여부
    if request.user.id != None:
        c_addlikes = AddLike.objects.filter(user=request.user).filter(content_name='실시간세부댓글').filter(content_id=gallery_id).filter(is_active=True).values_list('comment_id',flat=True)
        c_addlikes = list(c_addlikes)
    else :
        c_addlikes = False

    # 게시글 조회수 증가
    gallery.views += 1
    gallery.save()
    # 글작성일을 나타낼 때 날짜 or 몇분전으로 나타내기 위한 변수
    time = get_date('nowtime').strftime('%Y-%m-%d:%H')
    new_date = get_date('nowtime').strftime('%Y-%m-%d')

    # 게시글이 댓글 쓴후에 보여질시
    comment_id = comment_id

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'board_kind':board_kind,
        'content': gallery,
        'content_object': '실시간세부',
        'addlike': addlike,
        'c_addlikes': c_addlikes,
        'comments': comments,
        'point': point,
        'pre_page': request.META.get('HTTP_REFERER'),
        'time': time,
        'new_date': new_date,
        'comment_id': comment_id,
    }

    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'gallerys/show.html', context)

@login_required
def create(request, tag=None):
    # 배너 데이터
    banners = gallery_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 글쓸시 포인트, 경험치
    point = Point.objects.filter(title='실시간세부작성').values('point').first()
    ex = Exprience.objects.filter(title='실시간세부작성').values('exprience').first()

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'point': point,
        'board_kind': tag
    }
    # 글저장할 때
    if request.method == 'POST':
        print(request.POST)
        # 데이터저장
        user = request.user
        board_kind = request.POST['board_kind']
        pimg = []
        pimg.append(request.POST['pimg1'])
        pimg.append(request.POST['pimg2'])
        pimg.append(request.POST['pimg3'])
        pimg.append(request.POST['pimg4'])
        pimg.append(request.POST['pimg5'])
        tag = request.POST['tag']
        content = request.POST['content']
        show_ad = Banner.objects.get(title='실시간세부상세보기배너_1')

        # 유효성 검사 실패시 기존데이터 저장
        old_data = {'board_kind':board_kind ,'tag':tag, 'content':content, 'pimg1':pimg[0] }
        context['old_data'] = old_data

        # 유효성검사
        val_message = validation(old_data)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            return render(request, 'gallerys/create.html', context)
        # 임시사진 옮기기
        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(0, 5):
            if pimg[i]!='':
                old_path = pimg[i]
                pimg[i] = pimg[i].replace('temp','gallerys')
                os.rename(destination+old_path,destination+pimg[i])

        # 단일인지 다중이미지인지
        if(pimg[1]=='') :
            attribute = '단일'
        else :
            attribute = '다중'

        # 포인트, 경험치 추가
        request.user.point += point['point']
        request.user.exprience += ex['exprience']
        request.user.save()

        gallery = Gallery.objects.create(
            user=user, board_kind=board_kind, tag=tag, content=content, attribute=attribute,
            pimg1=pimg[0], pimg2=pimg[1], pimg3=pimg[2], pimg4=pimg[3], pimg5=pimg[4], show_ad=show_ad
        )
        gallery.save()
        return redirect('gallerys:index')

    # 페이지보여줄때
    else:
        return render(request, 'gallerys/create.html', context)

@login_required
def edit(request, gallery_id):
    # 배너 데이터
    banners = gallery_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 수정할 갤러리데이터
    gallery = get_object_or_404(Gallery, pk=gallery_id)

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'old_data': gallery,
    }

    # 글수정할 때
    if request.method == 'POST':
        print(request.POST)
        # 데이터저장
        user = request.user
        if request.user.is_staff == True:
            user = gallery.user
        board_kind = request.POST['board_kind']
        pimg = []
        pimg.append(request.POST['pimg1'])
        pimg.append(request.POST['pimg2'])
        pimg.append(request.POST['pimg3'])
        pimg.append(request.POST['pimg4'])
        pimg.append(request.POST['pimg5'])
        tag = request.POST['tag']
        content = request.POST['content']

        # 유효성 검사 실패시 기존데이터 저장
        old_data = {'board_kind':board_kind ,'tag':tag, 'content':content, 'pimg1':pimg[0] }
        context['old_data'] = old_data

        # 유효성검사
        val_message = validation(old_data)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            # return render(request, 'gallerys/edit.html', context)
            return redirect(reverse('gallerys:edit', args = (gallery_id,)))

        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(0, 5):
            if pimg[i]!='':
                old_path = pimg[i]
                pimg[i] = pimg[i].replace('temp','gallerys')
                os.rename(destination+old_path,destination+pimg[i])

        # 단일인지 다중이미지인지
        if(pimg[1]=='') :
            attribute = '단일'
        else :
            attribute = '다중'

        # 저장
        gallery.board_kind = board_kind
        gallery.tag, gallery.content, gallery.attribute = tag, content, attribute
        gallery.pimg1, gallery.pimg2, gallery.pimg3, gallery.pimg4, gallery.pimg5, = pimg[0], pimg[1], pimg[2], pimg[3], pimg[4]
        gallery.save()

        return redirect('gallerys:index')
    else:
        return render(request, 'gallerys/edit.html', context)

def delete(request, gallery_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)
    gallery.is_published = False
    gallery.save()
    return redirect('gallerys:index')

@csrf_exempt
def scroll_page(request):
    if request.method == 'POST':
        page = request.POST['page']
        board_kind = request.POST['board_kind']

        # 갤러리
        gallerys_obj = Gallery.objects.order_by('-upload_date').filter(is_published=True)
        # 상단태그맵핑 클릭시
        if board_kind == 'tour':
            gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='여행샷').filter(is_published=True)
        elif board_kind == 'food':
            gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='음싯샷').filter(is_published=True)
        elif board_kind == 'hotel':
            gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='숙소샷').filter(is_published=True)
        elif board_kind == 'shopping':
            gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='쇼핑샷').filter(is_published=True)
        elif board_kind == 'airport':
            gallerys_obj = gallerys_obj.order_by('-upload_date').filter(board_kind='공항샷').filter(is_published=True)

        # 페이지네이션
        paginator = Paginator(gallerys_obj, 18)
        gallerys = ''
        # 페이지범위를 넘는지 확인
        if int(page) <= paginator.num_pages:
            gallerys = paginator.get_page(page)
        gallerys = serializers.serialize('json', gallerys)

        context = {
            'status': 'success',
            'a_gallerys': gallerys
        }
    else:
        context = {
            'status': 'ext error'
        }
    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
# summernote 이미지 임시저장
def summernote_tmp(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        destination = settings.MEDIA_ROOT+'/gallerys/temp/'

        # 파일 확장자 체크
        fname ,ext = os.path.splitext(file.name)
        if ext == '.png' or ext == '.jpg' or ext == '.PNG' or ext == '.JPG':

            #파일이름바꾸기 날짜-유저명.확장자
            nowtime = get_date('nowtime').strftime('%Y%m%d%H%M%S%f')
            user = request.user.username
            filename = nowtime+'_'+user+ext
            file_url = '/media/gallerys/temp/'+filename

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

            # 파일정사각형으로 자르기
            width, height = resize_img.size
            core = 0
            # 세로 가로 뭐가 긴지
            if width > height:
                start = (width-height)/2
                resize_img = resize_img.crop((start, 0, start+height, height))
            else:
                start = (height-width)/2
                resize_img = resize_img.crop((0, start, width, start+width))

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

@csrf_exempt
# 이미지 회전
def img_rotate(request):
    if request.method == 'POST':
        index = request.POST['index']
        imgurl = []
        imgurl.append(request.POST['imgurl1'])
        imgurl.append(request.POST['imgurl2'])
        imgurl.append(request.POST['imgurl3'])
        imgurl.append(request.POST['imgurl4'])
        imgurl.append(request.POST['imgurl5'])
        destination = settings.MEDIA_ROOT

        # 모두회전일경우
        if index == '0' :
            for i in range(0, 5):
                if imgurl[i] != '' :
                    # 이미지 회전
                    afterimg = Image.open(destination+imgurl[i])
                    afterimg = afterimg.rotate(-90)
                    # 파일저장
                    afterimg.save(destination+imgurl[i])
        # 한 이미지 회전일 경우
        else :
            i = int(index)-1
            afterimg = Image.open(destination+imgurl[i])
            afterimg = afterimg.rotate(-90)
            afterimg.save(destination+imgurl[i])

        # imgurl = destination.replace(settings.MEDIA_ROOT, '')
        # 전송데이터
        context = {
            'status': 'success',
            'index': index,
        }
    else :
        context = {
            'status': 'ext error'
        }
    return HttpResponse(json.dumps(context), content_type="application/json")

#좋아요 증가
@login_required
def add_like(request):
    content_name = request.POST['content_name']
    content_id = request.POST['content_id']
    content_title = request.POST['content_content'][0:40]
    gallery = get_object_or_404(Gallery, pk=content_id)

    #클릭시 숫자증가
    gallery.likes += 1
    gallery.save()

    #좋아요 DB에 데이터추가
    addlike = AddLike.objects.create(
        user=request.user, content_name=content_name, content_id = content_id, content_title = content_title
    )
    addlike.save()

    # 좋아요 알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'like', likefrom=request.user, comment_user=gallery.user, comment_table='실시간세부',
        board_name='실시간세부',board_url='gallerys/show/'+str(content_id), content_id = content_id
    )
    c_alarm.save()

    # Ajax성공시
    context = {
        'message': 'success',
        'addlike_id':addlike.id,
        'l_num': gallery.likes
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def add_unlike(request):
    content_id = request.POST['content_id']
    like_id = request.POST['like_id']

    gallery = get_object_or_404(Gallery, pk=content_id)
    addLike = get_object_or_404(AddLike, pk=like_id)

    #클릭시 숫자감소
    gallery.likes -= 1
    gallery.save()
    #좋아요 is_active False로
    addLike.is_active = False
    addLike.save()

    # Ajax성공시
    context = {
        'message': 'success',
        'l_num': gallery.likes
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

#댓글좋아요 증가
@login_required
def c_add_like(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']
    content_name = request.POST['content_name']
    content_title = request.POST['content_content'][0:40]
    comment = get_object_or_404(Comment_Gallery, pk=comment_id)

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
        act_type = 'c_like', likefrom=request.user, comment_user=comment.user, comment_table='실시간세부댓글',
        board_name='실시간세부',  board_url='gallerys/show/'+str(content_id)+'/'+str(comment_id), content_id = content_id, comment_id = comment_id
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

    comment = get_object_or_404(Comment_Gallery, pk=comment_id)
    addLike = AddLike.objects.filter(user=request.user, content_name="실시간세부댓글", content_id=content_id,comment_id=comment_id).filter(is_active=True).get()

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

#유효성검사
def validation(old_data):
    # 게시판 선택을 하지 않았을시
    if old_data['board_kind'] == '':
        return '작성할 게시판을 선택해주세요.'
    # 이미지를 삽입 안했을시
    elif old_data['pimg1']=='':
        return '이미지를 삽입해주세요.'
    # 텍스트
    elif len(old_data['content']) > 500000:
        return '내용의 글자 수를 줄여주세요.'
    else:
        return '유효성검사성공'

# 배너데이터 가져오기
def gallery_banners():
    banners_gallery_top = Banner.objects.order_by('position_1').filter(title__contains='실시간세부상단').filter(is_published=True)
    banners_main = Banner.objects.order_by('position_1').filter(title__contains='메인').filter(is_published=True)
    banner_top = get_object_or_404(banners_main, position_1=0)
    # 메뉴배너
    banner_menu = Banner.objects.order_by('position_1').filter(title__contains='메뉴').filter(is_published=True)
    banners = {
        'banner_top': banner_top,
        'banners_gallery_top': banners_gallery_top,
        'banner_menu':banner_menu
    }
    return banners

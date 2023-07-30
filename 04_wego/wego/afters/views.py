import os
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from banners.models import Banner
from pages.models import AddLike
from pages.models import Point, Exprience
from .models import After
from comments.models import Comment_After
from django.contrib.auth.decorators import login_required
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from pages.views import get_date, uprising_keyword
from django.contrib import messages
from PIL import Image
import re
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from msgboxs.models import Alarm_Addcommentlike
from msgboxs.views import getAlarmListNew

def index(request, tag=None):
    # 배너 데이터
    banners = after_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 이용후기
    afters_obj = After.objects.order_by('attribute', '-upload_date').filter(is_published=True)
    board_kind = 'all'
    # 상단태그맵핑 클릭시
    if tag == 'best':
        afters_obj = afters_obj.filter(best_published=True)
        board_kind = 'best'
    elif tag == 'tour':
        afters_obj = afters_obj.filter(board_kind='여행')
        board_kind = 'tour'
    elif tag == 'hotel':
        afters_obj = afters_obj.filter(board_kind='숙소')
        board_kind = 'hotel'
    elif tag == 'food':
        afters_obj = afters_obj.filter(board_kind='맛집')
        board_kind = 'food'
    elif tag == 'massage':
        afters_obj = afters_obj.filter(board_kind='마사지')
        board_kind = 'massage'
    elif tag == 'beauty':
        afters_obj = afters_obj.filter(board_kind='뷰티')
        board_kind = 'beauty'
    elif tag == 'etc':
        afters_obj = afters_obj.filter(board_kind='기타')
        board_kind = 'etc'

    # 검색창
    s_select = request.GET.get('sch_slt')
    s_text = request.GET.get('sch_tx')
    if s_select != None:
        if s_select == '제목':
            afters_obj = afters_obj.filter(title__contains=s_text)
        else :
            afters_obj = afters_obj.filter(user__username__contains=s_text)

    # 페이지네이션
    paginator = Paginator(afters_obj, 10)
    page = request.GET.get('page')
    afters = paginator.get_page(page)
    # 페이지네이션 나타낼 번호 제어
    page_range = pagination_range(afters, paginator)
    # 우측레이아웃데이터
    rights = right_index()

    # 글작성일을 나타낼 때 날짜 or 몇분전으로 나타내기 위한 변수
    time = get_date('nowtime').strftime('%Y-%m-%d:%H')
    new_date = get_date('nowtime').strftime('%Y-%m-%d')

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'afters':afters,
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

    return render(request, 'afters/index.html', context)

# 우측 레이아웃관련 데이터
def right_index():
    right_bests = After.objects.filter(best_published=True).order_by('-upload_date').filter(is_published=True)
    right_news = After.objects.order_by('-upload_date').filter(is_published=True)
    right_comments = Comment_After.objects.order_by('-upload_date').filter(is_published=True)
    rights = {
        'right_bests': right_bests,
        'right_news': right_news,
        'right_comments': right_comments,
    }
    return rights

# 페이지네이션
def pagination_range(afters, paginator):
    index = afters.number
    max_index = len(paginator.page_range)

    # if index > max_index - 2:
    #     start_index = 9
    # el
    if index >= 3:
        start_index = index - 3
    else :
        start_index = 0

    # if index < 3 :
    #     end_index = 5 - start_index
    # el
    if index <= max_index - 2:
        end_index = index + 2
    else :
        end_index = max_index
    # print('index:',index)
    # print('start_index:',start_index)
    # print('end_index:',end_index)
    # print('max_index:',max_index)

    page_range = list(paginator.page_range)[start_index:end_index]
    return page_range

def show(request, after_id, comment_id=None):
    # 배너 데이터
    banners = after_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 게시글 데이터
    after = get_object_or_404(After, pk=after_id)
    # 게시글의 댓글 데이터
    comments = after.comment_after_set.all().order_by('upload_date').filter(is_published=True)
    # 게시글의 태그 데이터
    board_kind = after.board_kind
    # 댓글쓸시 포인트
    point = Point.objects.filter(title='후기댓글').values('point').first()

    # 게시글에 대한 회원의 좋아요 여부
    if request.user.id != None:
        addlike = AddLike.objects.filter(user=request.user).filter(content_name='후기').filter(content_id=after_id).filter(is_active=True)
        if addlike.exists():
            addlike = addlike[0]
    else :
        addlike = AddLike.objects.filter(user=None).filter(content_name='후기').filter(content_id=after_id).filter(is_active=True)
    # 해당 게시글의 댓글들에 대한 회원의 좋아요 여부
    if request.user.id != None:
        c_addlikes = AddLike.objects.filter(user=request.user).filter(content_name='후기댓글').filter(content_id=after_id).filter(is_active=True).values_list('comment_id',flat=True)
        c_addlikes = list(c_addlikes)
    else :
        c_addlikes = False

    # 게시글 조회수 증가
    after.views += 1
    after.save()
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
        'content': after,
        'content_object': '여행후기',
        'addlike': addlike,
        'c_addlikes': c_addlikes,
        'comments': comments,
        'point': point,
        'pre_page': request.META.get('HTTP_REFERER'),
        'time': time,
        'new_date': new_date,
        'comment_id': comment_id,
        'rights':rights
    }

    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'afters/show.html', context)

#좋아요 증가
@login_required
def add_like(request):
    content_name = request.POST['content_name']
    content_id = request.POST['content_id']
    content_title = request.POST['content_title']
    after = get_object_or_404(After, pk=content_id)

    #클릭시 숫자증가
    after.likes += 1
    after.save()

    #좋아요 DB에 데이터추가
    addlike = AddLike.objects.create(
        user=request.user, content_name=content_name, content_id = content_id, content_title = content_title
    )
    addlike.save()

    # 댓글-좋아요 알람생성
    c_alarm = Alarm_Addcommentlike.objects.create(
        act_type = 'like', likefrom=request.user, comment_user=after.user, comment_table='후기',
        board_name='후기',  board_url='afters/show/'+str(content_id), content_id = content_id,
    )
    c_alarm.save()

    # Ajax성공시
    context = {
        'message': 'success',
        'addlike_id':addlike.id,
        'l_num': after.likes
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required
def add_unlike(request):
    content_id = request.POST['content_id']
    like_id = request.POST['like_id']

    after = get_object_or_404(After, pk=content_id)
    addLike = get_object_or_404(AddLike, pk=like_id)

    #클릭시 숫자감소
    after.likes -= 1
    after.save()
    #좋아요 is_active False로
    addLike.is_active = False
    addLike.save()

    # Ajax성공시
    context = {
        'message': 'success',
        'l_num': after.likes
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

#댓글좋아요 증가
@login_required
def c_add_like(request):
    content_id = request.POST['content_id']
    comment_id = request.POST['comment_id']
    content_name = request.POST['content_name']
    content_title = request.POST['content_content'][0:40]
    comment = get_object_or_404(Comment_After, pk=comment_id)

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
        act_type = 'c_like', likefrom=request.user, comment_user=comment.user, comment_table='후기댓글',
        board_name='후기',  board_url='afters/show/'+str(content_id)+'/'+str(comment_id), content_id = content_id, comment_id = comment_id
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

    comment = get_object_or_404(Comment_After, pk=comment_id)
    addLike = AddLike.objects.filter(user=request.user, content_name="후기댓글", content_id=content_id, comment_id=comment_id).filter(is_active=True).get()

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

@login_required
def create(request, tag=None):
    # 배너 데이터
    banners = after_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 우측레이아웃데이터
    rights = right_index()
    # 글쓸시 포인트, 경험치
    point = Point.objects.filter(title='후기작성').values('point').first()
    ex = Exprience.objects.filter(title='후기작성').values('exprience').first()

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
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
        index_image = ['NONE','NONE','NONE','NONE','NONE']
        tag = request.POST['tag']
        title = request.POST['title']
        content = request.POST['content']
        g_map1 = request.POST['g_map1']
        g_map2 = request.POST['g_map2']
        g_map3 = request.POST['g_map3']
        g_map4 = request.POST['g_map4']
        g_map5 = request.POST['g_map5']
        url_link = request.POST['url_link']
        show_ad = Banner.objects.get(title='후기상세보기배너_1')
        print(len(content))
        # 유효성 검사 실패시 기존데이터 저장
        old_data = {'tag':tag, 'title':title, 'content':content, 'g_map1':g_map1, 'g_map2':g_map2, 'g_map3':g_map3,
            'g_map4':g_map4, 'g_map5':g_map5, 'url_link':url_link, 'board_kind':board_kind}
        context['old_data'] = old_data

        # 유효성검사
        val_message = validation(old_data)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            return render(request, 'afters/create.html', context)

        # 임시이미지 실제이미지로
        pattern = re.compile ('<img [^>]*src="([^"]+)')
        old_img = pattern.findall(content)
        # Content에 실제 이미지파일로 맵핑 바꾸기
        content = content.replace('/media/afters/temp/', '/media/afters/afters/')
        new_img = pattern.findall(content)

        # 임시->실제 이미지복사
        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(0, len(new_img)):
            os.rename(destination+old_img[i],destination+new_img[i])

        # 대표이미지 5개 저장
        for i in range(0, len(new_img)):
            if i > 4:
                pass
            else :
                index_image[i] = new_img[i]

        # 인덱스페이지 내용 조금 보여주기 위해 한글만추출
        content_tmp = content
        pattern = re.compile('[^ ㄱ-ㅣ가-힣]+')
        p_tag = pattern.sub('', content_tmp)
        index_content = ''
        for i in range(0, len(p_tag)):
            index_content+=p_tag[i]
        # 글자수 유효성
        index_content = index_content[0:199]

        # 포인트, 경험치 추가
        request.user.point += point['point']
        request.user.exprience += ex['exprience']
        request.user.save()

        after = After.objects.create(
            user=user, board_kind=board_kind,
            index_image1 = index_image[0], index_image2 = index_image[1], index_image3 = index_image[2], index_image4 = index_image[3], index_image5 = index_image[4],
            index_content=index_content, tag=tag, title=title, content=content, g_map1=g_map1, g_map2=g_map2, g_map3=g_map3, g_map4=g_map4, g_map5=g_map5,
            url_link=url_link, show_ad=show_ad
        )
        after.save()
        return redirect('afters:index')

    # 페이지보여줄때
    else:
        return render(request, 'afters/create.html', context)

@login_required
def edit(request, after_id):
    # 배너 데이터
    banners = after_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 수정할 후기데이터
    after = get_object_or_404(After, pk=after_id)
    # 우측레이아웃데이터
    rights = right_index()

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'old_data': after,
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
        if request.user.is_staff == True:
            user = after.user
        board_kind = request.POST['board_kind']
        index_image = ['NONE','NONE','NONE','NONE','NONE']
        tag = request.POST['tag']
        title = request.POST['title']
        content = request.POST['content']
        g_map1 = request.POST['g_map1']
        g_map2 = request.POST['g_map2']
        g_map3 = request.POST['g_map3']
        g_map4 = request.POST['g_map4']
        g_map5 = request.POST['g_map5']
        url_link = request.POST['url_link']

        # 유효성 검사 실패시 기존데이터 저장
        old_data = {'id':after.id,'tag':tag, 'title':title, 'content':content, 'g_map1':g_map1, 'g_map2':g_map2, 'g_map3':g_map3,
            'g_map4':g_map4, 'g_map5':g_map5, 'url_link':url_link, 'board_kind':board_kind}
        context['old_data'] = old_data

        # 유효성검사
        val_message = validation(old_data)
        if val_message != '유효성검사성공':
            messages.error(request, val_message)
            return render(request, 'afters/edit.html', context)

        # 임시이미지 실제이미지로
        pattern = re.compile ('<img [^>]*src="([^"]+)')
        old_img = pattern.findall(content)
        # Content에 실제 이미지파일로 맵핑 바꾸기
        content = content.replace('/media/afters/temp/', '/media/afters/afters/')
        new_img = pattern.findall(content)

        # 임시->실제 이미지복사
        destination = settings.MEDIA_ROOT.replace("/media", "")
        for i in range(0, len(new_img)):
            os.rename(destination+old_img[i],destination+new_img[i])

        # 대표이미지 5개 저장
        for i in range(0, len(new_img)):
            if i > 4:
                pass
            else :
                index_image[i] = new_img[i]

        # 인덱스페이지 내용 조금 보여주기 위해 한글만추출
        content_tmp = content
        pattern = re.compile ('[^ ㄱ-ㅣ가-힣]+')
        p_tag = pattern.sub('', content_tmp)
        index_content = ''
        for i in range(0, len(p_tag)):
            index_content+=p_tag[i]
        # 글자수 유효성
        index_content = index_content[0:199]

        after.user, after.board_kind = user, board_kind
        after.index_image1, after.index_image2, after.index_image3, after.index_image4, after.index_image5 = index_image[0], index_image[1], index_image[2], index_image[3], index_image[4]
        after.index_content, after.tag, after.title, after.content = index_content, tag, title, content
        after.g_map1, after.g_map2, after.g_map3, after.g_map4, after.g_map5 = g_map1, g_map2, g_map3, g_map4, g_map5
        after.url_link = url_link
        after.save()
        return redirect('afters:index')
    else:
        return render(request, 'afters/edit.html', context)

@csrf_exempt
# summernote 이미지 임시저장
def summernote_tmp(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        destination = settings.MEDIA_ROOT+'/afters/temp/'

        # 파일 확장자 체크
        fname ,ext = os.path.splitext(file.name)
        if ext == '.png' or ext == '.jpg' or ext == '.PNG' or ext == '.JPG':

            #파일이름바꾸기 날짜-유저명.확장자
            nowtime = get_date('nowtime').strftime('%Y%m%d%H%M%S%f')
            user = request.user.username
            filename = nowtime+'_'+user+ext
            file_url = '/media/afters/temp/'+filename

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
    elif old_data['title'] == '' or len(old_data['title']) > 40:
        return '제목는 0-40글자로 입력해주세요.'
    # 텍스트
    elif len(old_data['content']) > 1000000:
        return '내용의 글자 수를 줄여주세요.'
    # 관련링크
    elif len(old_data['url_link']) > 200:
        return '관련링크의 글자 수를 줄여주세요.'
    # 이미지 갯수
    # elif old_data['content'].count("src=\"/media/") > 30:
    #     return '이미지는 최대 20개 업로드가능합니다.'
    else:
        return '유효성검사성공'

# 데이터삭제
@login_required
def delete(request, after_id):
    after = get_object_or_404(After, pk=after_id)
    after.is_published = False
    after.save()
    return redirect('afters:index')

# 배너데이터 가져오기
def after_banners():
    banners_main = Banner.objects.order_by('position_1').filter(title__contains='메인').filter(is_published=True)
    banner_top = get_object_or_404(banners_main, position_1=0)
    banners_review_left = Banner.objects.order_by('position_1').filter(title__contains='후기좌측').filter(is_published=True)
    banners_review_right = Banner.objects.order_by('position_1').filter(title__contains='후기우측').filter(is_published=True)
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

import os
from django.shortcuts import render, get_object_or_404, redirect
import simplejson as json
from django.contrib.auth.decorators import login_required
from accounts.models import User
from banners.models import Banner
from .models import Profile_Image
from afters.models import After
from asks.models import Ask
from infos.models import Info
from communitys.models import Community
from courses.models import Course
from gallerys.models import Gallery
from promotions.models import Promotion
from centers.models import Notice, CustomerCenter
from comments.models import Comment_After,Comment_Ask,Comment_Community,Comment_Info,Comment_Course,Comment_Gallery,Comment_Promotion
from pages.models import AddScrap, AddLike
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from pages.views import get_date, uprising_keyword
from django.conf import settings
from PIL import Image
from msgboxs.views import getAlarmListNew

# 메인 마이페이지
@login_required
def index(request):
    #배너
    banners = mypage_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 랭킹
    rank = getRank(request)

    context = {
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'rank':rank['rank'],
        'p':rank['p'],
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'mypages/index.html', context)

# 회원정보
@login_required
def userinfo(request, name):
    #배너
    banners = mypage_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    #프로필
    profiles = Profile_Image.objects.filter(title__contains='기본').filter(is_published=True)
    #관리자프로필
    admin_profiles = Profile_Image.objects.filter(title__contains='관리자').filter(is_published=True)
    # 랭킹
    rank = getRank(request)

    context = {
        'name':name,
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'rank':rank['rank'],
        'p':rank['p'],
        'profiles':profiles,
        'admin_profiles':admin_profiles,
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'mypages/userinfo.html', context)

# 활동
@login_required
def active(request, name):
    user = get_object_or_404(User, pk=request.user.id)
    #배너
    banners = mypage_banners()
    #급상승키워드
    upkeyword = uprising_keyword()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 랭킹
    rank = getRank(request)

    # 게시글
    boards = getMyWrite(request)
    # 페이지네이션
    paginator = Paginator(boards, 15)
    page = request.GET.get('page')
    boards_page = paginator.get_page(page)
    # 페이지네이션 나타낼 번호 제어
    boards_page_range = pagination_range(boards_page, paginator)

    #댓글
    comments = getMyComment(request)
    # 페이지네이션
    paginator = Paginator(comments, 15)
    page = request.GET.get('page')
    comments_page = paginator.get_page(page)
    # 페이지네이션 나타낼 번호 제어
    comments_page_range = pagination_range(comments_page, paginator)

    #스크랩
    scraps = user.addscrap_set.order_by('-upload_date').filter(is_active=True)
    # 페이지네이션
    paginator = Paginator(scraps, 15)
    page = request.GET.get('page')
    scraps_page = paginator.get_page(page)
    # 페이지네이션 나타낼 번호 제어
    scraps_page_range = pagination_range(scraps_page, paginator)

    #좋아요
    # likes = user.addlike_set.order_by('-upload_date').filter(is_active=True).values_list('id','content_name','content_id','comment_id','content_title','upload_date')

    context = {
        'name':name,
        'banners': banners,
        'upkeyword':upkeyword,
        'rigth_date':rigth_date,
        'rank':rank['rank'],
        'p':rank['p'],
        'boards':boards,
        'board_len':boards.count(),
        'boards_page':boards_page,
        'boards_page_range': boards_page_range,
        'comments':comments,
        'comment_len':comments.count(),
        'comments_page':comments_page,
        'comments_page_range': comments_page_range,
        'scraps':scraps,
        'scrap_len':scraps.count(),
        'scraps_page':scraps_page,
        'scraps_page_range': scraps_page_range,
        # 'likes':likes,
        # 'likes_len':likes.count(),
    }
    #알림 추출
    context1 = getAlarmListNew(request)
    context.update(context1)

    return render(request, 'mypages/active.html', context)

# 내가쓸글 가져오기
@login_required
def getMyWrite(request):
    user = get_object_or_404(User, pk=request.user.id)
    # 게시글
    after = user.after_set.all().filter(is_published=True).values('id','title','board_kind','comments','views','show_ad__title','upload_date')
    ask = user.ask_set.all().filter(is_published=True).values('id','title','board_kind','comments','views','show_ad__title','upload_date')
    info = user.info_set.all().filter(is_published=True).values('id','title','board_kind','comments','views','show_ad__title','upload_date')
    community = user.community_set.all().filter(is_published=True).values('id','title','board_kind','comments','views','show_ad__title','upload_date')
    course = user.course_set.all().filter(is_published=True).values('id','title','board_kind','comments','views','show_ad__title','upload_date')
    gallery = user.gallery_set.all().filter(is_published=True).values('id','tag','board_kind','comments','views','show_ad__title','upload_date')
    promotion = user.promotion_set.all().filter(is_published=True).values('id','introduction','board_kind','comments','views','show_ad','upload_date')
    notice = user.notice_set.all().filter(is_published=True).values('id','title','board_kind','comments','views','show_ad__title','upload_date')
    customerCenter = user.customercenter_set.all().filter(is_published=True).values('id','title','board_kind','comments','views','show_ad__title','upload_date')

    boards = after.union(ask,info,community,course,gallery,promotion,notice,customerCenter)
    return boards.order_by('-upload_date')

# 내가쓴 댓글 가져오기
@login_required
def getMyComment(request):
    user = get_object_or_404(User, pk=request.user.id)
    comment_after = user.comment_after_set.all().filter(is_published=True).values('id','comment_table__id','comment_table__show_ad__title','comment_table__board_kind','content','likes','upload_date')
    comment_ask = user.comment_ask_set.all().filter(is_published=True).values('id','comment_table__id','comment_table__show_ad__title','comment_table__board_kind','content','likes','upload_date')
    comment_info = user.comment_info_set.all().filter(is_published=True).values('id','comment_table__id','comment_table__show_ad__title','comment_table__board_kind','content','likes','upload_date')
    comment_community = user.comment_community_set.all().filter(is_published=True).values('id','comment_table__id','comment_table__show_ad__title','comment_table__board_kind','content','likes','upload_date')
    comment_course = user.comment_course_set.all().filter(is_published=True).values('id','comment_table__id','comment_table__show_ad__title','comment_table__board_kind','content','likes','upload_date')
    comment_gallery = user.comment_gallery_set.all().filter(is_published=True).values('id','comment_table__id','comment_table__show_ad__title','comment_table__board_kind','content','likes','upload_date')
    comment_notice = user.comment_notice_set.all().filter(is_published=True).values('id','comment_table__id','comment_table__show_ad__title','comment_table__board_kind','content','likes','upload_date')
    comment_customerCenter = user.comment_customercenter_set.all().filter(is_published=True).values('id','comment_table__id','comment_table__show_ad__title','comment_table__board_kind','content','likes','upload_date')

    comments = comment_after.union(comment_ask,comment_info,comment_community,comment_course,comment_gallery,comment_notice,comment_customerCenter)
    return comments.order_by('-upload_date')

#랭킹
def getRank(request):
    user = get_object_or_404(User, pk=request.user.id)
    rank = User.objects.filter(level__gte=user.level).filter(exprience__gte=user.exprience).count()
    all_user = User.objects.all().count()
    p = round((rank/all_user) * 100, 2)
    data = {'rank':rank, 'p':p}
    return data

#프로필사진 변경
@login_required
def add_profile(request):
    if request.method == "POST":
        profile = request.POST['profile']

        # 프로필을 선택하지 않았을시
        if profile is '':
            messages.error(request, '프로필사진을 선택해주세요.')
            return redirect('mypages:userinfo', name='index')

        # 저장
        user = get_object_or_404(User, pk=request.user.id)
        user.profile_image = profile
        user.save()

        # 바꾼 프로필사진 선택여부 +1
        profile_image = Profile_Image.objects.filter(photo=profile.replace('/media/','')).filter(is_published=True).get()
        profile_image.click_number += 1
        profile_image.save()

        messages.error(request, '프로필사진이 변경되었습니다.')
        return redirect('mypages:userinfo', name='index')
    else:
        messages.error(request, '로그인 후 이용해주세요')
        return redirect('mypages:userinfo', name='index')

#프로필사진 커스텀사진으로 변경
@login_required
def add_custom_profile(request):
    if request.method == 'POST' and request.FILES['custom_upload']:
        file = request.FILES['custom_upload']
        destination = settings.MEDIA_ROOT+'/accounts/profiles/'

        # 파일 확장자 체크
        fname ,ext = os.path.splitext(file.name)
        if ext == '.png' or ext == '.jpg' or ext == '.PNG' or ext == '.JPG':
            #파일이름바꾸기 날짜-유저명.확장자
            nowtime = get_date('nowtime').strftime('%Y%m%d%H%M%S%f')
            user = request.user.username
            filename = nowtime+'_'+user+ext
            file_url = '/media/accounts/profiles/'+filename

            # 파일 크기 Resize
            resize_img = Image.open(file)
            width, height = resize_img.size
            if width > 4000 :
                messages.error(request, '선택된 파일크기가 너무 큽니다.')
                return redirect('mypages:userinfo', name='index')
            elif width > 3000 :
                resize_img = resize_img.resize((int(width/20),int(height/20)))
            elif width > 2000 :
                resize_img = resize_img.resize((int(width/10),int(height/10)))
            elif width > 1000 :
                resize_img = resize_img.resize((int(width/5),int(height/5)))
            elif width > 500 :
                resize_img = resize_img.resize((int(width/4),int(height/4)))
            else :
                resize_img = resize_img.resize((width,height))

            # 파일 저장
            profile = resize_img.save(destination+filename)
            #유저프로필에 저장
            user = get_object_or_404(User, pk=request.user.id)
            user.profile_image = file_url
            user.save()

            messages.error(request, '프로필사진이 변경되었습니다.')
            return redirect('mypages:userinfo', name='index')
        else:
            messages.error(request, '파일확장자를 확인해주세요.(png, jpg)')
            return redirect('mypages:userinfo', name='index')
    else:
        messages.error(request, '프로필사진이 선택되지 않았습니다.')
        return redirect('mypages:userinfo', name='index')

#비밀번호 변경
@login_required
def chg_pwd(request):
    if request.method == "POST":
        print(request.POST)
        pwd = request.POST.get('pwd')
        newpwd = request.POST['newpwd']
        newpwdck = request.POST['newpwdck']
        user = User.objects.get(id=request.user.id)

        # 비밀번호 유효성검사
        if len(newpwd) < 6 or len(newpwd) > 20 :
            messages.error(request, '암호는 6글자이상 20글자이하로 정해주세요')
            return redirect('mypages:userinfo', name='pwd')
        # 기존 유저와 비밀번호가 일치하는지
        if check_password(pwd, user.password) is not True:
            messages.error(request, '기존암호와 일치하지 않습니다.')
            return redirect('mypages:userinfo', name='pwd')
        # 비밀번호와 확인이 일치하는지
        if newpwd != newpwdck :
            messages.error(request, '새 암호와 암호확인 내용이 일치하지 않습니다.')
            return redirect('mypages:userinfo', name='pwd')

        #비밀번호저장
        user.set_password(newpwd)
        user.save()

        messages.error(request, '비밀번호가 변경되었습니다. 다시 로그인해주세요')
        return render(request, 'accounts/login_email.html')
    else:
        context = {'name':'index'}
        messages.error(request, '로그인 후 이용해주세요')
        return redirect('mypages:userinfo', name='index')

#정보및연락처 변경
@login_required
def chg_info(request):
    if request.method == "POST":
        phone = request.POST['phone']
        kakaotalk = request.POST['kakaotalk']
        user = User.objects.get(id=request.user.id)

        # 연락처 유효성검사
        if len(phone) > 11 :
            messages.error(request, '핸드폰번호를 확인해주세요')
            return redirect('mypages:userinfo', name='edit')
        # 카카오톡정보 유효성검사
        if len(kakaotalk) > 30 :
            messages.error(request, '카카오톡ID를 확인해주세요')
            return redirect('mypages:userinfo', name='edit')

        # 최신화 저장
        user.phone = phone
        user.kakaotalk = kakaotalk
        user.save()

        messages.error(request, '정보및연락처가 변경되었습니다.')
        return redirect('mypages:userinfo', name='index')
    else:
        context = {'name':'index'}
        messages.error(request, '로그인 후 이용해주세요')
        return redirect('mypages:userinfo', name='index')

# 페이지네이션
def pagination_range(content, paginator):
    index = content.number
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

# 배너데이터 가져오기
def mypage_banners():
    banners_main = Banner.objects.order_by('position_1').filter(title__contains='메인').filter(is_published=True)
    banner_top = get_object_or_404(banners_main, position_1=0)
    # 메뉴배너
    banner_menu = Banner.objects.order_by('position_1').filter(title__contains='메뉴').filter(is_published=True)
    banners = {
        'banner_top': banner_top,
        'banner_menu':banner_menu
    }
    return banners

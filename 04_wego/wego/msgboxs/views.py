from django.shortcuts import get_object_or_404, render, redirect, HttpResponse, HttpResponseRedirect
from accounts.models import User
from .models import Msgbox, SaveMsgbox, Alarm_Addcommentlike
from django.contrib import messages
from pages.models import Point, Exprience
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# 알림함 Index 페이지
@login_required
def index(request, tag):
    # rooms = Msgbox.objects.order_by('upload_date').filter(Q(send_user__id=request.user.id) | Q(from_user__id=request.user.id)).filter(is_active=True)
    chat_list = Msgbox.objects.order_by('chat_id','-upload_date').filter(Q(send_user__id=request.user.id) | Q(from_user__id=request.user.id)).filter(is_active=True).distinct('chat_id')
    save_list = SaveMsgbox.objects.order_by('msgbox', '-upload_date').filter(user=request.user).filter(is_published=True).distinct('msgbox')

    context = {
        'tag':tag,
        'chat_list':chat_list,
        'save_list':save_list,
    }
    # 알림
    alarm = getAlarmListNew(request)
    context.update(alarm)

    return render(request, 'msgboxs/index.html', context)

# 알림추출
def getAlarmListNew(request):
    user = request.user
    cntAlarm = 0
    cntMsg = 0
    getAlarmList = ''
    getNewAlarm = ''
    boards = ''
    comments = ''
    chat_list_n = ''
    cntMsg = ''
    scraps = ''
    if user.id is not None:
        getAlarmList = Alarm_Addcommentlike.objects.order_by('checkitout','-upload_date').filter(comment_user=user).filter(is_published=True)
        getNewAlarm = getAlarmList.filter(checkitout=False)
        cntAlarm = getNewAlarm.count()
        # 게시글
        from mypages.views import getMyWrite
        boards = getMyWrite(request)[0:4]
        #댓글
        from mypages.views import getMyComment
        comments = getMyComment(request)[0:4]
        # 받은 쪽지중 안읽은 것
        chat_list_n = Msgbox.objects.order_by('-upload_date').filter(send_user__id=user.id).filter(is_checked=False).filter(is_active=True)
        cntMsg = chat_list_n.count()
        # 스크랩
        scraps = user.addscrap_set.order_by('-upload_date').filter(is_active=True)[0:4]
    dic = {
        'main_cntAlarm': cntAlarm,
        'main_alarmlist': getNewAlarm,
        'alarmlist':getAlarmList,
        'boards': boards,
        'mycomments': comments,
        'chat_list_n': chat_list_n,
        'cntMsg':cntMsg,
        'scraps':scraps
    }

    return dic

# 알림함 쪽지탭 Show페이지
@login_required
def show(request, user_id, chat_id=None, after_chat=0):
    # 쪽지쓸시 포인트
    point = Point.objects.filter(title='쪽지작성').values('point').first()
    send_user = User.objects.get(id=user_id)

    #쪽지인덱스 또는 글쓰고난뒤
    if chat_id :
        # 채팅방내역검색
        rooms = Msgbox.objects.order_by('upload_date').filter(chat_id=chat_id).filter(is_active=True)
        # 읽음으로표시
        for room in rooms :
            if room.send_user == request.user:
                room.is_checked = True
                room.save()

    #검색 또는 쪽지보내기로 바로 들어올때
    elif user_id :
        # 자기아이디 클릭시
        if user_id == request.user.id :
            messages.error(request, '내 자신에게 쪽지를 보내수없어요!')
            return redirect('msgboxs:search')

        # 채팅내역검색 없으면 채팅방ID를 만듬
        rooms = Msgbox.objects.order_by('upload_date').filter(Q(send_user__id=user_id, from_user__id=request.user.id) | Q(send_user__id=request.user.id, from_user__id=user_id)).filter(is_active=True)
        if rooms :
            chat_id = rooms.first().chat_id
        else :
            # 기존채팅방이없을시 채팅번호생성
            from pages.views import get_date
            chat_id = get_date('nowtime').strftime('%Y%m%d%H%M%S%f')

    context = {
        'send_user': send_user,
        'point':point,
        'rooms':rooms,
        'chat_id':chat_id,
        'after_chat': after_chat
    }
    return render(request, 'msgboxs/show.html', context)

# 알림함 사람검색 페이지
@login_required
def search(request):
    search = request.GET.get('search_value')
    # 검색창작성시
    if search != None:
        #검색창에 아무것도 입력않을시
        # if search != '':
            search_users = User.objects.filter(username__contains=search).filter(is_active=True)
            user_count = search_users.count()

            # 페이지네이션
            paginator = Paginator(search_users, 5)
            page = request.GET.get('page')
            search_users = paginator.get_page(page)
            # 페이지네이션 나타낼 번호 제어
            page_range = pagination_range(search_users, paginator)

            print(search_users)
            context = {
                'search_users': search_users,
                'user_count': user_count,
                'page_range': page_range,
            }
            return render(request, 'msgboxs/search.html', context)
        # else :
            # return render(request, 'messageboxs/search.html')
    else:
        return render(request, 'msgboxs/search.html')

# 쪽지발송시 페이지
@login_required
def create(request):
    content = request.POST['content']
    send_user_id = request.POST['send_user']
    chat_id = request.POST['chat_id']

    # 쪽지글자수 유효성검사
    if len(content) > 300 :
        messages.error(request, '쪽지내용은 300자 내로 작성해주세요.')
        return redirect('msgboxs:search')

    send_user = User.objects.get(id=send_user_id)
    # 메세지방생성
    msgbox = Msgbox.objects.create(
        chat_id=chat_id, send_user=send_user, from_user = request.user, content = content
    )
    msgbox.save()

    # 쪽지보낼시 포인트차감, 경험치추가
    point = Point.objects.filter(title='쪽지작성').values('point').first()
    ex = Exprience.objects.filter(title='쪽지작성').values('exprience').first()
    request.user.point += point['point']
    request.user.exprience += ex['exprience']
    request.user.save()

    return redirect('msgboxs:show', send_user_id, chat_id, msgbox.id)

# 쪽지삭제
@login_required
def delete(request, room_id):
    print(room_id);
    room = get_object_or_404(Msgbox, pk=room_id)
    room.is_active = False
    room.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# 쪽지저장
@login_required
def save(request, room_id):
    print(room_id);
    room = get_object_or_404(Msgbox, pk=room_id)
    print(room)
    savemsgbox = SaveMsgbox.objects.create(
        user = request.user, msgbox = room
    )
    savemsgbox.save()
    print(savemsgbox)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# 페이지네이션
def pagination_range(contents, paginator):
    index = contents.number
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

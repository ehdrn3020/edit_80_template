from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import SchoolQuiz
from .models import SchoolRoulette
from pages.models import Point
from pages.views import get_date
from random import *
import simplejson as json
import datetime

# 스쿨퀴즈 업데이트
def school_quiz(request):
    user = request.user
    # 로그인 여부 확인
    if user.is_authenticated:            
        # 이미 참여했다면 예외처리
        today = get_date('today')
        if SchoolQuiz.objects.filter(apply_date__icontains=today).filter(username=user).exists():
            # 메세지를 보낸다
            messages.error(request, '이미 오늘 참가하셨습니다. 내일 다시 도전하세요!')
            return redirect('pages:index')
        # 오늘 처음 참여한다면
        else:
            # 해당 계정에 포인트 추가
            p = Point.objects.filter(title='세부퀴즈').values('point').first()
            user.point += p['point']
            user.save()
            # 스토어활동 히스토리에 저장
            nowtime = datetime.datetime.now()
            SchoolQuiz.objects.create(
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


# 스쿨룰렛 URL넘기기
def school_roulette(request):
    return render(request, 'stores/roulette.html')

# 스쿨룰렛 생성
def school_roulette_create(request):
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
            if SchoolRoulette.objects.filter(apply_date__icontains=today).filter(username=user).exists():
                # 메세지를 보낸다
                message = '오늘 이미 참여하셨습니다. 내일 다시 도전해주세요!'

            # 오늘 처음 참여면 포인트랜덤선택
            else :
                if r_point[i] == '20P':
                    deg = randint(35, 85)
                    p = 20
                    message = '20포인트를 획득하셨습니다.'
                elif r_point[i] == '30P':
                    deg = randint(95, 145)
                    p = 30
                    message = '30포인트를 획득하셨습니다.'
                elif r_point[i] == '50P':
                    deg = randint(155, 205)
                    p = 50
                    message = '50포인트를 획득하셨습니다.'
                elif r_point[i] == '100P':
                    deg = randint(215, 265)
                    p = 100
                    message = '100포인트를 획득하셨습니다.'
                elif r_point[i] == '200P':
                    deg = randint(275, 325)
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
                deg += 360 * randint(5,7)

                # 포인트 저장하기
                p = Point.objects.filter(title='세부룰렛_'+str(i+1)).values('point').first()
                user.point += p['point']
                user.save()
                # 스토어활동 히스토리에 저장
                nowtime = datetime.datetime.now()
                SchoolRoulette.objects.create(
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

# 스쿨룰렛 업데이트
# def school_roulette_update(request):
#     mode = request.POST['mode']
#     if mode == 'create' and request.method == 'POST':
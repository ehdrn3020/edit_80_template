from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.http import HttpResponse
from banners.models import Banner
from .models import ApiData, AddScrap
from accounts.models import User
from afters.models import After
from asks.models import Ask
from infos.models import Info
from communitys.models import Community
from courses.models import Course
from gallerys.models import Gallery
from promotions.models import Promotion
from centers.models import Notice, CustomerCenter

from msgboxs.models import Alarm_Addcommentlike
from msgboxs.views import getAlarmListNew

from django.contrib.auth.decorators import login_required
import datetime
from datetime import date, timedelta
import urllib
import json
import random

#메인페이지
def index(request):
    # 배너 데이터
    banners = main_banners()
    # 급상승키워드
    upkeyword = uprising_keyword()
    # 날씨 데이터
    weather = cebu_weather()
    # 환율 데이터
    dollar_rate = cebu_rate()
    # 회화 데이터
    p_language = cebu_language()
    # 우측에 표시되는 날짜
    rigth_date = get_date('today').strftime("%m.%d")+' ('+get_date('weekday')+')'
    # 세부 퀴즈
    quiz = cebu_quiz()

    viewcount = 0 # 조회수 높은 기준
    moreviewcount = 10 # 더 높은 조회수 기준

    #뉴스배너 밑에 정보글
    info_news = Info.objects.order_by('-views').filter(main_published=True).filter(is_published=True)[0:7]

    ##게시판 나열 레이아웃
    #질문답변
    asks = Ask.objects.order_by('-upload_date').filter(views__gte=viewcount).filter(is_published=True)[0:10]
    #정보공유
    infos = Info.objects.order_by('-upload_date').filter(views__gte=viewcount).filter(is_published=True)[0:10]
    #커뮤니티
    communitys = Community.objects.order_by('-upload_date').filter(views__gte=viewcount).filter(is_published=True)[0:10]
    #여행코스
    courses = Course.objects.order_by('-upload_date').filter(views__gte=viewcount).filter(is_published=True)[0:10]

    # 후기
    afters = After.objects.order_by('-upload_date').filter(is_published=True)
    # 오늘의 인기글
    today_afters = afters[0:10]
    # 베스트후기
    best_afters = afters.filter(best_published=True)[0:5]
    # 메인후기
    all_afters = afters.filter(views__gte=viewcount)
    main_afters = afters.filter(main_published=True)[0:4]
    tour_afters = afters.filter(board_kind='여행').filter(views__gte=viewcount)
    main_tour_afters = afters.filter(board_kind='여행').filter(main_published=True)[0:4]
    hotel_afters = afters.filter(board_kind='숙소').filter(views__gte=viewcount)
    main_hotel_afters = afters.filter(board_kind='숙소').filter(main_published=True)[0:4]
    food_afters = afters.filter(board_kind='맛집').filter(views__gte=viewcount)
    main_food_afters = afters.filter(board_kind='맛집').filter(main_published=True)[0:4]
    massage_afters = afters.filter(board_kind='마사지').filter(views__gte=viewcount)
    main_massage_afters = afters.filter(board_kind='마사지').filter(main_published=True)[0:4]
    beauty_afters = afters.filter(board_kind='뷰티').filter(views__gte=viewcount)
    main_beauty_afters = afters.filter(board_kind='뷰티').filter(main_published=True)[0:4]
    etc_afters = afters.filter(board_kind='기타').filter(views__gte=viewcount)
    main_etc_afters = afters.filter(board_kind='기타').filter(main_published=True)[0:4]

    # 실시간세부 (업로드순서대로 나열)
    main_tour_gallerys = Gallery.objects.order_by('-upload_date').filter(board_kind='여행샷').filter(is_published=True)[0:6]
    main_food_gallerys = Gallery.objects.order_by('-upload_date').filter(board_kind='음식샷').filter(is_published=True)[0:6]
    main_hotel_gallerys = Gallery.objects.order_by('-upload_date').filter(board_kind='숙소샷').filter(is_published=True)[0:6]
    main_shopping_gallerys = Gallery.objects.order_by('-upload_date').filter(board_kind='쇼핑샷').filter(is_published=True)[0:6]
    main_airport_gallerys = Gallery.objects.order_by('-upload_date').filter(board_kind='공항샷').filter(is_published=True)[0:6]

    #로그인시 경험치 기준이 넘으면 레벨업
    level_check(request)
    if request.user.id is not None:
        print(request.user.level_icon)

    context = {
        'banners': banners,
        'weather': weather,
        'dollar_rate': dollar_rate,
        'p_language': p_language,
        'upkeyword':upkeyword,
        'rigth_date': rigth_date,
        'quiz': quiz,
        'info_news': info_news,
        'asks':asks,
        'infos':infos,
        'communitys':communitys,
        'courses':courses,
        'moreviewcount':moreviewcount,
        'today_afters':today_afters,
        'best_afters':best_afters,
        'all_afters':all_afters,
        'main_afters':main_afters,
        'tour_afters':tour_afters,
        'main_tour_afters':main_tour_afters,
        'hotel_afters':hotel_afters,
        'main_hotel_afters':main_hotel_afters,
        'food_afters':food_afters,
        'main_food_afters':main_food_afters,
        'massage_afters':massage_afters,
        'main_massage_afters':main_massage_afters,
        'beauty_afters':beauty_afters,
        'main_beauty_afters':main_beauty_afters,
        'etc_afters':etc_afters,
        'main_etc_afters':main_etc_afters,
        'main_tour_gallerys':main_tour_gallerys,
        'main_food_gallerys':main_food_gallerys,
        'main_hotel_gallerys':main_hotel_gallerys,
        'main_shopping_gallerys':main_shopping_gallerys,
        'main_airport_gallerys':main_airport_gallerys,
    }
    # 알림
    if request.user.id is not None:
        alarm = getAlarmListNew(request)
        context.update(alarm)

    return render(request, 'pages/main.html', context)

# 배너데이터 갖고오기
def main_banners():
    # 메인광고판 쿼리셋
    banners_main = Banner.objects.order_by('position_1').filter(title__contains='메인').filter(is_published=True)
    banner_1 = banners_main.order_by('position_2').filter(position_1=1)
    banner_2 = banners_main.order_by('position_2').filter(position_1=2)
    banner_3 = banners_main.order_by('position_2').filter(position_1=3)
    banner_4 = banners_main.order_by('position_2').filter(position_1=4)
    banner_5 = banners_main.order_by('position_2').filter(position_1=5)
    banner_6 = banners_main.order_by('position_2').filter(position_1=6)
    banner_7 = banners_main.order_by('position_2').filter(position_1=7)
    banner_8 = banners_main.order_by('position_2').filter(position_1=8)
    banner_9 = banners_main.order_by('position_2').filter(position_1=9)
    banner_10 = banners_main.order_by('position_2').filter(position_1=10)
    # 메인슬라이드 쿼리셋
    banner_slide = banners_main.order_by('position_2').filter(position_1=11)
    # 메인좌측배너 쿼리셋
    banner_left = banners_main.filter(position_1__range=(12,19))
    # 메인우측배너 쿼리셋
    banner_right = banners_main.filter(position_1__range=(20,29))
    # 탑배너
    banner_top = get_object_or_404(banners_main, position_1=0)
    # 메뉴배너
    banner_menu = Banner.objects.order_by('position_1').filter(title__contains='메뉴').filter(is_published=True)
    # 쇼핑배너
    banner_shops = shop_banners()
    banners = {
        'banner_1': banner_1,
        'banner_2': banner_2,
        'banner_3': banner_3,
        'banner_4': banner_4,
        'banner_5': banner_5,
        'banner_6': banner_6,
        'banner_7': banner_7,
        'banner_8': banner_8,
        'banner_9': banner_9,
        'banner_10': banner_10,
        'banner_slide': banner_slide,
        'banner_left': banner_left,
        'banner_right': banner_right,
        'banner_top': banner_top,
        'banner_shops': banner_shops,
        'banner_menu': banner_menu
    }
    return banners

# 어제/오늘/내일 날짜구하기
def get_date(whatday):
    today = date.today()
    if whatday == 'today':
        return today
    elif whatday == 'yesterday':
        yesterday = today - timedelta(days = 1)
        return yesterday
    # elif whatday == 'tommorow':
    elif whatday == 'weekday':
        weekday = ['월','화','수','목','금','토','일']
        index_week = today.weekday()
        return weekday[index_week]
    elif whatday == 'nowtime':
        now = datetime.datetime.now()
        return now

# 날씨데이터 (1분에 최대60번 API콜)
def cebu_weather():
    # 최신화시간 여부를 파악한다
    apidata_db = ApiData.objects.get(title='메인_날씨')
    recall_min = apidata_db.recall_min
    last_call = apidata_db.last_call
    nowtime = datetime.datetime.now()
    # 변수를 담을 디션너리
    weather = {}

    # 현재시간이 최신화 할 시간보다 크다면(지났다), DB 최신화한다
    if nowtime > last_call + timedelta(minutes=int(recall_min)):
        w_apiurl = 'http://api.openweathermap.org/data/2.5/weather?q=Cebu%20City&APPID=d8fa6f9d491a0de2b3749d3c99de3b93'
        w_url = urllib.request.urlopen(w_apiurl)
        w_apid = w_url.read()
        w_data = json.loads(w_apid)

        # 현재날씨상태
        weather['name'] = 'cebu city'
        main = w_data['weather'][0]['main']
        if main == 'Rain':
            weather['main'] = '비'
            weather['description'] = '세부에 비가와요'
        elif main == 'Mist':
            weather['main'] = '안개'
            weather['description'] = '세부에 안개가 껴요'
        elif main == 'Clear':
            weather['main'] = '맑음'
            weather['description'] = '세부날씨는 맑아요'
        elif main == 'Clouds':
            weather['main'] = '흐림'
            weather['description'] = '세부날씨는 흐려요'
        elif main == 'Thunderstorm':
            weather['main'] = '천둥번개'
            weather['description'] = '세부에 천둥번개쳐요'
        else:
            weather['main'] = main
            weather['description'] = main

        # 현재기온, 최고기온, 최저기온, 습도, 풍속
        weather['temp'] = int(w_data['main']['temp']-273.5)
        weather['temp_max'] = int(w_data['main']['temp_max']-273.5)
        weather['temp_min'] = int(w_data['main']['temp_min']-273.5)
        weather['humidity'] = w_data['main']['humidity']
        weather['wind'] = w_data['wind']['speed']

        # 데이터저장
        apidata_db.data1=weather['name']
        apidata_db.data2=weather['main']
        apidata_db.data3=weather['description']
        apidata_db.data4=weather['temp']
        apidata_db.data5=weather['temp_max']
        apidata_db.data6=weather['temp_min']
        apidata_db.data7=weather['humidity']
        apidata_db.data8=weather['wind']
        apidata_db.last_call=nowtime
        apidata_db.save()

    # 최신화 시간이 안됬을 경우 DB에서 기존데이터 가져옴
    else:
        # 데이터 딕션너리에 저장
        weather['name'] = apidata_db.data1
        weather['main'] = apidata_db.data2
        weather['description'] = apidata_db.data3
        weather['temp'] = int(apidata_db.data4)
        weather['temp_max'] = int(apidata_db.data5)
        weather['temp_min'] = int(apidata_db.data6)
        weather['humidity'] = apidata_db.data7
        weather['wind'] = apidata_db.data8

    return weather

# 환율데이터 (한달에 최대 1000번 API콜)
def cebu_rate():
    # 최신화시간 여부를 파악한다
    apidata_db = ApiData.objects.get(title='메인_환율')
    recall_min = apidata_db.recall_min
    last_call = apidata_db.last_call
    nowtime = datetime.datetime.now()
    # 변수를 담을 디션너리
    dollar_rate = {}

    # 최신화일 경우
    if nowtime > last_call + timedelta(minutes=int(recall_min)):
        # 어제 날짜 구하기
        yesterday = get_date('yesterday')
        # 어제,오늘 환율데이터 가져오기
        r_apiurl='https://openexchangerates.org/api/latest.json?app_id=00e6609c75a2483d8b6463b8825d2601'
        r_url = urllib.request.urlopen(r_apiurl)
        r_apid = r_url.read()
        r_data = json.loads(r_apid)

        r_apiurl_y='https://openexchangerates.org/api/historical/'+str(yesterday)+'.json?app_id=00e6609c75a2483d8b6463b8825d2601'
        r_url_y = urllib.request.urlopen(r_apiurl_y)
        r_apid_y = r_url_y.read()
        r_data_y = json.loads(r_apid_y)

        # 달러->원,달러->페소,전날차이 달러->원, 전날차이 달러->페소 (기준은 달러(USD))
        dollar_rate['krw'] = round(r_data['rates']['KRW'],2)
        dollar_rate['php'] = round(r_data['rates']['PHP'],2)
        # 전날대비 +- 값
        dollar_rate['status_krw'] = str(round(r_data['rates']['KRW'] - r_data_y['rates']['KRW'],2))
        dollar_rate['status_php'] = str(round(r_data['rates']['PHP'] - r_data_y['rates']['PHP'],2))

        # 데이터저장
        apidata_db.data1=dollar_rate['krw']
        apidata_db.data2=dollar_rate['php']
        apidata_db.data3=dollar_rate['status_krw']
        apidata_db.data4=dollar_rate['status_php']
        apidata_db.last_call=nowtime
        apidata_db.save()

    # 최신화가 아닐경우
    else :
        # 데이터 딕션너리에 저장
        dollar_rate['krw'] = float(apidata_db.data1)
        dollar_rate['php'] = float(apidata_db.data2)
        dollar_rate['status_krw'] = float(apidata_db.data3)
        dollar_rate['status_php'] = float(apidata_db.data4)

    return dollar_rate

# 세부회화 (하루에 한번 랜덤으로)
def cebu_language():
    # 최신화여부를 확인한다
    language = ApiData.objects.get(title='메인_회화')
    today = get_date('today')
    # 이미 최신화 됨
    if str(today) in str(language.last_call):
        return language
    # 아직 최신화 안됨
    else :
        # DB데이터 불러온다.
        apidata_db = ApiData.objects.filter(title__icontains='메인_회화')
        random_id = random.randrange(len(apidata_db))
        # 최신화업데이트
        language.data1 = apidata_db[random_id].data1
        language.data2 = apidata_db[random_id].data2
        language.data3 = apidata_db[random_id].data3
        language.last_call = datetime.datetime.now()
        language.save()
        return language

# 세부 퀴즈 (하루에 한번 랜덤으로)
def cebu_quiz():
    # 최신화여부를 확인한다
    quiz = ApiData.objects.get(title='메인_퀴즈')
    today = get_date('today')
    # 이미 최신화 됨
    if str(today) in str(quiz.last_call):
        return quiz
    # 아직 최신화 안됨
    else :
        # DB데이터 불러온다.
        apidata_db = ApiData.objects.filter(title__icontains='메인_퀴즈')
        random_id = random.randrange(len(apidata_db))
        # 최신화업데이트
        quiz.data1 = apidata_db[random_id].data1
        quiz.data2 = apidata_db[random_id].data2
        quiz.data3 = apidata_db[random_id].data3
        quiz.data4 = apidata_db[random_id].data4
        quiz.data5 = apidata_db[random_id].data5
        quiz.data6 = apidata_db[random_id].data6
        quiz.data7 = apidata_db[random_id].data7
        quiz.last_call = datetime.datetime.now()
        quiz.save()
        return quiz

# 실시간검색어
def uprising_keyword():
    keyword = ['막탄한식','투말록폭포','환율좋은곳','팁 얼마나','세부김떡순','세부 스노쿨링','고래상어보는시간','호핑투어옷',
    '모알보알캐녀닝','세부관광','산페드로요새','아얄라몰위치','스쿠버다이빙','제리스그릴','어메이징쇼가격','쇼핑리스트',
    '세부삽겹살','샹그릴라조식','여행자보험','올랑고섬','세부리조트가성비','가족리조트','필리핀가족여행','유심충전법',
    '투어지도','sm몰','제이파크택시비','리조트추천','세부3박','한인마트','보홀오션젯','라라세부','여행지추천','제이파크환전소',
    '세부비행시간','호핑투어섬','맛집추천','배틀트립오슬롭','세부신혼여행','세부전압','택시요금','세부비행기표',
    '세부마지막날','세부스파','입국신고서','막탄에서세부시티','세부막탄스파','7d망고','기념품','카지노위치','픽업드랍','고래상어보는데',
    '막탄공항세','그랜드스파','한국세부시차','세부모자','세부에서보홀','난루수안섬','까사베르데','세부데이트코스','란타우레스토랑',
    '세부퍼시픽','탑스힐전망대','단독호핑','레드크랩위치','세부루프탑추천','샹그릴라리조트','쉬라인가는법','전자담배반입','바이호텔'
    ]
    random_num = [random.randint(0,len(keyword)-1) for i in range(10)]
    result = []
    for i in random_num:
        result.append(keyword[i])
    return result

# 쇼핑 배너
def shop_banners():
    shops1 = Banner.objects.order_by('position_2').filter(position_1=30).filter(is_published=True)
    shops2 = Banner.objects.order_by('position_2').filter(position_1=31).filter(is_published=True)
    shops3 = Banner.objects.order_by('position_2').filter(position_1=32).filter(is_published=True)
    banner_shops = {
        'shops1': shops1,
        'shops2': shops2,
        'shops3': shops3,
    }
    return banner_shops

# 스크랩시 저장
@login_required
def addscrap(request):
    user = request.POST['user']
    tag = request.POST['tag']
    object_id = request.POST['object_id']
    if tag == '여행후기':
        content_object = get_object_or_404(After, pk=object_id)
    elif tag == '질문답변':
        content_object = get_object_or_404(Ask, pk=object_id)
    elif tag == '정보공유':
        content_object = get_object_or_404(Info, pk=object_id)
    elif tag == '커뮤니티':
        content_object = get_object_or_404(Community, pk=object_id)
    elif tag == '여행코스':
        content_object = get_object_or_404(Course, pk=object_id)
    elif tag == '실시간세부':
        content_object = get_object_or_404(Gallery, pk=object_id)
    elif tag == '여행사홍보':
        content_object = get_object_or_404(Promotion, pk=object_id)
    elif tag == '공지사항':
        content_object = get_object_or_404(Notice, pk=object_id)
    elif tag == '고객센터':
        content_object = get_object_or_404(CustomerCenter, pk=object_id)

    addscrap = AddScrap(user=request.user, content_object=content_object, tag=tag)
    addscrap.save()

    context = {
        'status': 'success'
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

# 알람클릭시 처리
@login_required
def alarm_url(request):
    alarm_id = request.POST['alarm_id']
    url = ''
    if alarm_id != '0':
        c_alarm = Alarm_Addcommentlike.objects.get(id=alarm_id)
        # 읽음으로 체크
        c_alarm.checkitout = True
        c_alarm.save()
        url = c_alarm.board_url
        # 해당글이 삭제되었을시
        if c_alarm.comment_table == '후기' or c_alarm.comment_table == '후기댓글':
            obj = After.objects.filter(id=c_alarm.content_id).filter(is_published=True)
            if not obj :
                url = 'deleted'
        elif c_alarm.comment_table == '질문답변' or c_alarm.comment_table == '질답댓글':
            obj = Ask.objects.filter(id=c_alarm.content_id).filter(is_published=True)
            if not obj :
                url = 'deleted'
        elif c_alarm.comment_table == '정보공유' or c_alarm.comment_table == '정보공유댓글':
            obj = Info.objects.filter(id=c_alarm.content_id).filter(is_published=True)
            if not obj :
                url = 'deleted'
        elif c_alarm.comment_table == '커뮤니티' or c_alarm.comment_table == '커뮤니티댓글':
            obj = Community.objects.filter(id=c_alarm.content_id).filter(is_published=True)
            if not obj :
                url = 'deleted'
        elif c_alarm.comment_table == '실시간세부' or c_alarm.comment_table == '실시간세부댓글':
            obj = Gallery.objects.filter(id=c_alarm.content_id).filter(is_published=True)
            if not obj :
                url = 'deleted'
        elif c_alarm.comment_table == '여행사홍보' or c_alarm.comment_table == '여행사홍보댓글':
            obj = Promotion.objects.filter(id=c_alarm.content_id).filter(is_published=True)
            if not obj :
                url = 'deleted'
        elif c_alarm.comment_table == '고객센터' or c_alarm.comment_table == '고객센터댓글':
            obj = CustomerCenter.objects.filter(id=c_alarm.content_id).filter(is_published=True)
            if not obj :
                url = 'deleted'
        elif c_alarm.comment_table == '공지사항' or c_alarm.comment_table == '공지사항댓글':
            obj = Notice.objects.filter(id=c_alarm.content_id).filter(is_published=True)
            if not obj :
                url = 'deleted'
    # 전체읽음표시
    elif alarm_id == '0':
        alarms = Alarm_Addcommentlike.objects.filter(checkitout=False, comment_user=request.user)
        for al in alarms:
            al.checkitout = True
            al.save()
            url = 'redirect'

    context = {
        'url': url
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

# 일정경험치시 레벨업
def level_check(request):
    if request.user.id is not None:
        # 500기준으로 레벨업
        if request.user.exprience >= 500 :
            request.user.level += 1
            request.user.exprience -=500
            # 레벨업시 아이콘바꾸기
            if request.user.level == 2:
                request.user.level_icon = "/media/mypages/levels/level2.png"
            if request.user.level == 3:
                request.user.level_icon = "/media/mypages/levels/level3.png"
            if request.user.level == 4:
                request.user.level_icon = "/media/mypages/levels/level4.png"
            if request.user.level >= 5:
                request.user.level_icon = "/media/mypages/levels/level5.png"
            request.user.save()
        #프로필없을때 기본프로필설정
        if request.user.level_icon == '':
            request.user.level_icon = "/media/mypages/levels/level1.png"
            request.user.save()
    return

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from banners.models import Banner
from .models import ApiData
import datetime
from datetime import date, timedelta
import urllib
import json
import random 
#메인페이지
def index(request):
    
    # 메인광고판 쿼리셋
    banners_main = Banner.objects.order_by('position_1').filter(is_published=True)
    banner_1 = banners_main.order_by('position_2').filter(position_1=1)
    banner_2 = banners_main.order_by('position_2').filter(position_1=2)
    banner_3 = banners_main.order_by('position_2').filter(position_1=3)
    banner_4 = banners_main.order_by('position_2').filter(position_1=4)
    banner_5 = banners_main.order_by('position_2').filter(position_1=5)
    # 메인슬라이드 쿼리셋
    banner_slide = banners_main.order_by('position_2').filter(position_1=10)
    # 메인좌측배너 쿼리셋
    banner_left = banners_main.filter(position_1__range=(11,19))
    # 메인우측배너 쿼리셋
    banner_right = banners_main.filter(position_1__range=(20,29))
    # 탑배너
    banner_top = get_object_or_404(banners_main, position_1=0)

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

    context = {
        'banner_1': banner_1,
        'banner_2': banner_2,
        'banner_3': banner_3,
        'banner_4': banner_4,
        'banner_5': banner_5,
        'banner_slide': banner_slide,
        'banner_left': banner_left,
        'banner_right': banner_right,
        'banner_top': banner_top,
        'weather': weather,
        'dollar_rate': dollar_rate,
        'p_language': p_language,
        'rigth_date': rigth_date,
        'quiz': quiz,
    }
    return render(request, 'pages/main.html', context)

# 알림함 Index 페이지
def messagebox_index(request):
    return render(request, 'messageboxs/index.html')

# 알림함 쪽지탭 Show페이지
def messagebox_show(request):
    return render(request, 'messageboxs/show.html')

# 알림함 사람검색 페이지
def messageboxs_search(request):
    return render(request, 'messageboxs/search.html')

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
        w_apiurl = 'http://api.openweathermap.org/data/2.5/weather?q=Cebu City&APPID=d8fa6f9d491a0de2b3749d3c99de3b93'
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

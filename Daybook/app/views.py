# coding=utf-8
from datetime import datetime
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import pytz

from app.models import Daybooks


def wrong_access():
    msg = '올바르지 않은 접근입니다.'.decode('utf-8')
    return redirect_with_message(msg, '/')


def redirect_with_message(msg, url):
    return HttpResponse('''
            <script>
                alert("''' + msg + '''");
                window.open("''' + url + '''", "_self");
            </script>
            ''')


def index(request):
    # 12/18 삽질
    try:
        username = request.session['username']
    except KeyError:
        username = ''

    if username != '':
        return HttpResponseRedirect('daybook')
    else:
        return render(request, 'index.html')


def get_daybook(request):
    try:
        username = request.session['username']
    except KeyError:
        username = ''

    if username != '':
        # get daybook list
        daybooks = Daybooks.objects.filter(user_id=username)

        today_daybook = None
        daybook_list = []

        # make daybook dictionary
        for daybook in daybooks:
            if daybook.get_time_difference() == 0:
                today_daybook = daybook
            elif daybook.get_time_difference() != 0:
                daybook_list.append(daybook)

        # render
        return render(request, 'daybook.html', {
            'user_id': username,
            'today_daybook': today_daybook,
            'daybook_list': daybook_list
        })
    else:
        msg = '로그인이 필요합니다.'.decode('utf-8')

        return redirect_with_message(msg, '/login')


def write_daybook(request):
    if request.method != 'POST':
        wrong_access()

    user_id = request.POST.get('user_id', '')
    weather = request.POST.get('weather', '')
    title = request.POST.get('title', '')
    content = request.POST.get('content', '')

    msg = ''.decode('utf-8')

    if user_id != '' and weather != '' and title != '' and content != '':
        now = datetime.now()
        date_format = now.strftime('%Y%m%d')
        result = Daybooks.objects.filter(date_format=date_format, user_id=user_id).update(weather=weather, title=title,
                                                                                          date=now, content=content)

        if result == 1:
            msg = '일기를 수정했습니다.'.decode('utf-8')
        elif result == 0:
            Daybooks.objects.create(user_id=user_id, date_format=date_format, date=now, weather=weather, title=title,
                                    content=content)
            msg = '일기를 저장했습니다.'.decode('utf-8')
    else:
        msg = '일기 내용을 채워주세요.'.decode('utf-8')

    return redirect_with_message(msg, '/daybook')


def erase_daybook(request):
    if request.method != 'POST':
        wrong_access()

    username = request.session['username']
    date = request.POST.get('date', '')

    if date is '':
        wrong_access()

    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    item_list = Daybooks.objects.filter(user_id=username)
    now = datetime.now()
    msg = ''
    for item in item_list:
        if item.get_time_difference(now) == 0:
            if item is not None:
                item.delete()
                msg = year + '년 '.decode('utf-8') + month + '월 '.decode('utf-8') + day + '일 일기를 삭제했습니다.'.decode('utf-8')

    if msg == '':
        msg = '삭제 도중 예기치 않은 오류가 발생했습니다.'.decode('utf-8')

    return redirect_with_message(msg, '/daybook')


def signin(request):
    if request.method != 'POST':
        return render(request, 'login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is None:
        msg = '사용자 이름과 비밀번호를 확인해주세요.'.decode('utf-8')
    else:
        if user.is_active:
            request.session['username'] = username
            msg = username + ' 님 반갑습니다.'.decode('utf-8')

            return redirect_with_message(msg, '/daybook')
        else:
            msg = '비활성화 된 사용자입니다.'.decode('utf-8')

    return redirect_with_message(msg, '/login')


def signup(request):
    if request.method != 'POST':
        return render(request, 'register.html')

    username = request.POST['username']
    password = request.POST['password']

    try:
        user = User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        user = User.objects.create_user(username, password=password)
        user.save()

        msg = '회원 가입에 성공하였습니다.'.decode('utf-8')

        return redirect_with_message(msg, '/login')
    else:
        msg = '사용자 이름을 누군가 이미 사용 중입니다.'.decode('utf-8')

        return redirect_with_message(msg, '/register')


def signout(request):
    logout(request)
    try:
        del request.session['username']
    except KeyError:
        pass

    return HttpResponseRedirect('/')
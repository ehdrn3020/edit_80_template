from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.urls import reverse
from accounts.models import User
from pages.models import Point, Exprience
from datetime import date

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from django.core.mail import send_mail
from random import randint

# from django import forms
# from .forms import RegisterModelForm

# 로그인 인덱스 페이지
def login(request):
    return render(request, 'accounts/login.html')

# 홈페이지로 이메일을 통해 로그인
def login_email(request):
    if request.method == 'POST':
        login_email = request.POST['login_email']
        login_pw = request.POST['login_pw']
        context = { 'email': login_email }

        # user_queryset = User.objects.filter(email=login_email).filter(social_login='이메일아이디').exists()
        user = auth.authenticate(username=login_email, password=login_pw)

        ## 유효성검사
        # Check Input Length
        if len(login_email) > 100  or len(login_pw) > 100:
            messages.error(request, '이메일 또는 비밀번호는 100자내로 입력해주세요.')
            return render(request, 'accounts/login_email.html', context)
        # None User
        elif user is None:
            messages.error(request, '아이디 또는 비밀번호가 맞지 않습니다.')
            return render(request, 'accounts/login_email.html', context)
        # Correct User
        else:
            # If First Login In Today, Get Point
            last_login = str(user.last_login)
            today = str(date.today())
            if(today not in last_login):
                p = Point.objects.filter(title='로그인').values('point').first()
                e = Exprience.objects.filter(title='로그인').values('exprience').first()
                user.point += p['point']
                user.exprience += e['exprience']
                user.save()
            # Login
            auth.login(request, user)
            return redirect('pages:index')
    else:
        return render(request, 'accounts/login_email.html')

# Logout
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('pages:index')

# Choice Register Method
def register_index(request):
    return render(request, 'accounts/register_index.html')

# Register
def register_create(request):
    if request.method == 'POST':
        # Get Form Value
        email = request.POST['register_id']
        username = request.POST['username']
        password = request.POST['register_pw']
        password_frm = request.POST['register_pw_frm']
        context = { 'email': email, 'username': username }

        # Check None Value
        if email == '' or username == '' or password == '' or password_frm == '':
            messages.error(request, '빈 항목을 채워주세요.')
            return render(request, 'accounts/register_create.html', context)

        # Check Username Duplicated
        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 사용중인 닉네임입니다.')
            return render(request, 'accounts/register_create.html', context)
        # Check Username Validation
        if not re.match("^[a-zA-Z0-9가-힣_]*$", username):
            messages.error(request, '닉네임에 특수문자는 사용하지 못합니다.')
            return render(request, 'accounts/register_create.html', context)
        # Check Username Length
        elif len(username) < 2 or len(username) > 10 :
            messages.error(request, '닉네임은 2-10글자로 정해주세요.')
            return render(request, 'accounts/register_create.html', context)

        # Check Email Duplicated
        elif User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            messages.error(request, '이미 ' + user.social_login + '(으)로 가입된 이메일입니다.')
            return render(request, 'accounts/register_create.html', context)
        # Check Email Validation
        elif not email_validate( email ):
            messages.error(request, '정확한 이메일 형식으로 입력해주세요.')
            return render(request, 'accounts/register_create.html', context)
        # Check Email Length
        elif len(email) < 5 or len(email) > 100 :
            messages.error(request, '이메일 길이를 확인해주세요.')
            return render(request, 'accounts/register_create.html', context)

        # Check If Passwords Matched
        elif password != password_frm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'accounts/register_create.html', context)
        # Check Passwords Length
        elif len(password) < 6 or len(password) > 20 or len(password_frm) < 6 or len(password_frm) > 20:
            messages.error(request, '비밀번호는 6-20글자로 정해주세요.')
            return render(request, 'accounts/register_create.html', context)

        # All Good
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email,
                is_active=False, social_login="이메일아이디"
            )
            user.save()

            #Send Email for Authentication
            current_site = get_current_site(request)
            mail_subject = '[위고세부] 회원가입 인증메일입니다.'
            mail_to = email
            mail_message = render_to_string('accounts/register_email.html',{
                'name': user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(mail_subject, mail_message, to=[mail_to])
            email.send()
            return render(request, 'accounts/register_send.html')
    else:
        return render(request, 'accounts/register_create.html')

# After Register Check Email Page
def register_send(request):
    return render(request, 'accounts/register_send.html')

# Check Email Input Of Register Form
def email_validate( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

# After Email Check Return Confirm Register
def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=int(uid))
    except(User.DoesNotExist):
        user = None
    try:
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'accounts/register_confirm.html')
        else:
            return render(request, 'accounts/login.html')
    except Exception as e:
        print(e)

# After Email Confirm Notice Page
def register_confirm(request):
    return render(request, 'accounts/register/confirm.html')

# Find Login ID and Password
def find(request):
    if request.method == 'POST':

        login_email = request.POST.get('login_email')
        login_pw = request.POST.get('login_pw_check')

        # Login ID Check
        if login_email is not None:
            context = { 'email': login_email }
            try:
                user = User.objects.filter(email=login_email).get()
                # Already Registerd User
                if user.social_login == '이메일아이디':
                    messages.error(request, '위고세부 회원가입을 통해 가입하셨습니다.')
                    return render(request, 'accounts/find.html', context)
                else:
                    messages.error(request, user.social_login + '로 연동하셨습니다. 소셜로그인으로 로그인하세요.')
                    return render(request, 'accounts/find.html', context)
            # Not Registerd
            except User.DoesNotExist:
                messages.error(request, '일치하는 회원정보가 없습니다.')
                return render(request, 'accounts/find.html', context)

        elif login_pw is not None :
            context = { 'email2': login_pw }
            try:
                user = User.objects.filter(email=login_pw).get()
                # Social Register User
                if user.social_login not in '이메일아이디':
                    print(user.social_login)
                    print(isinstance('이메일아이디', str))
                    messages.error(request, '소셜아이디로 가입한 계정은 비밀번호를 찾을 수 없습니다.')
                    return render(request, 'accounts/find.html', context)
                # Send Changed Password
                else :
                    random = randint(100000, 999999)
                    # Send Email For New Password
                    send_mail(
                        '[위고세부] 임시비밀번호 발급',
                        '위고세부 ' + login_pw + ' 계정의 임시비밀번호는 ' + str(random) + '입니다.',
                        'cebuschool.dg@gmail.com',
                        [login_pw],
                        fail_silently=False
                    )
                    # Update DB New Password
                    user.set_password(random)
                    user.save()
                    return render(request, 'accounts/find_password_confirm.html')

            # Not Registerd
            except User.DoesNotExist:
                messages.error(request, '일치하는 회원정보가 없습니다.')
                return render(request, 'accounts/find.html', context)

    else:
        return render(request, 'accounts/find.html')

# def save_session(request, p1, p2):
#     request.session['email'] = p1
#     request.session['username'] = p2

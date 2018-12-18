import hashlib
import uuid
from re import template

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

# 表单
from django_yunpan import settings
from .forms import RegisterForm, Login, personInfo, changePassword, activateUser, Change_head
# 消息
from django.contrib import messages
# 用户登录，退出管理
from django.contrib.auth import authenticate, login, logout
# 密码加密及验证
from django.contrib.auth.hashers import check_password, make_password
# 登录表
from .models import User, Data_yunpan
# 发送电子邮件
from django.core.mail import send_mail


def index(request, page):
    yunpan_datas = Data_yunpan.objects.all()[:settings.TOTAL_NUM]
    paginator = Paginator(yunpan_datas, settings.PER_NUM)
    currPage = paginator.page(page)
    yunpan_data = currPage.object_list
    data = {
        'paginator': paginator,
        'page': int(page),
        'yunpan_data': yunpan_data,
        'Previous':int(page)-1,
        'Next':int(page)+1,
        'Total_page':settings.TOTAL_NUM/settings.PER_NUM,
    }
    return render(request, 'index.html', context=data)


def index2(request):
    page = 1
    yunpan_datas = Data_yunpan.objects.all()[:200]
    paginator = Paginator(yunpan_datas, 20)
    currPage = paginator.page(page)
    yunpan_data = currPage.object_list
    data = {
        'paginator': paginator,
        'page': int(page),
        'yunpan_data': yunpan_data,
        'Previous':int(page)-1,
        'Next':int(page)+1,
    }
    return render(request, 'index.html', context=data)


# 用户注册
def useregister(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 添加到登录表
            User.objects.create_user(request.POST.get('username'), request.POST.get('email'),
                                     request.POST.get('password'))
            messages.success(request, '注册成功！')
            return redirect(reverse('app:login'))
    data = {
        'title': '注册',
        'form': form
    }
    return render(request, 'Register.html', context=data)


# 激活用户
@login_required()
def useractivate(request):
    if request.method == 'POST':
        username = request.user.username
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            form = activateUser(request.POST)
            if form.is_valid():
                # 生成
                token = createToken()
                request.session[token] = token
                email_html = loader.render_to_string('email/email.html',
                                                     context={'token': token, 'title': '激活用户', 'host': request.get_host,
                                                              'endpoint': 'check_activateMail'})
                toemail = request.POST.get('email')
                send_mail(subject='激活用户', message='change password', from_email='1176378069@qq.com',
                          recipient_list=[toemail],
                          html_message=email_html)
                messages.success(request, '邮件发送成功！请查收')
        else:
            messages.error(request, '用户名不存在或密码错误！')
    data = {
        'username': request.user.username
    }
    form = activateUser(initial=data)
    form.fields['username'].disabled = True
    return render(request, 'owncenter/activate.html', context={'form': form, 'title': '激活用户'})


def check_activateMail(request, token):
    print(token)
    print(request.session.get(token))
    if token == request.session.get(token):
        user = request.user
        if user:
            user.is_sensitize = True
            user.save()
            messages.success(request, '账户激活成功!')
            return redirect(reverse('app:index', kwargs={'page': 1}))
        else:
            messages.error(request, '请先登录！')
            return redirect(reverse('app:login'))

    else:
        messages.error(request, '账户激活失败！')
        return redirect(reverse('app:activate'))


# 用户登录
def userlogin(request):
    if not request.user.username:
        if request.method == 'POST':
            form = Login(request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                input_user = authenticate(request, username=username, password=password)
                if input_user:
                    login(request, input_user)
                    messages.success(request, '登录成功！')
                    return redirect(reverse('app:index', kwargs={'page': 1}))
                else:
                    messages.error(request, '该用户不存在或密码错误!')
        form = Login()
        data = {
            'title': '登录',
            'form': form
        }
        return render(request, 'Login.html', context=data)
    else:
        messages.info(request, '你已经是登录状态')
        return redirect(reverse('app:index', kwargs={'page': 1}))


# 用户退出登录
def userlogout(request):
    logout(request)
    messages.success(request, '退出成功！')
    return redirect(reverse("app:index", kwargs={'page': 1}))


# 查看个人信息
@login_required()
def person_info(request):
    data = {
        'title': '个人信息'
    }
    return render(request, 'owncenter/person_info.html', context=data)


# 修改密码
@login_required
def sendMail(request):
    if request.method == 'POST':
        form = personInfo(request.POST)
        if not form.is_valid():
            # 生成token
            token = createToken()
            request.session[token] = token
            #
            email_html = loader.render_to_string('email/email.html', context={'token': token, 'host': request.get_host,
                                                                              'endpoint': 'checkMail', 'title': '验证邮件'})
            toemail = request.POST.get('email')
            send_mail(subject='修改密码', message='change password', from_email='1176378069@qq.com',
                      recipient_list=[toemail], html_message=email_html)
            messages.success(request, '邮件发送成功！请查收')
    username = request.user.username
    email = request.user.email

    data = {
        'username': username,
        'email': email
    }

    form = personInfo(initial=data)
    form.fields['email'].disabled = False

    data = {
        'title': '1.发送验证邮件',
        'form': form
    }

    return render(request, 'owncenter/send_mail.html', context=data)


@login_required()
def checkMail(request, token):
    print(token)
    print(request.session.get(token))
    if token == request.session.get(token):
        username = request.user.username
        form = changePassword(initial={'username': username})
        messages.success(request, '邮箱验证通过，请输入新密码！')
        data = {
            'title': '2.请修改密码',
            'form': form,
        }
        return render(request, 'owncenter/change_password.html', context=data)
    else:
        messages.error(request, '邮件过期,请重新发送！')
        return redirect(reverse('app:send_mail'))


@login_required
def change_password(request):
    username = request.user.username
    if request.method == 'POST':
        passowrd = request.POST.get('password')
        form = changePassword(request.POST)
        if not authenticate(request, username=username, passowrd=passowrd):
            print(form.is_valid())
            if form.is_valid():
                u = request.user
                u.set_password(passowrd)
                u.save()
                messages.success(request, '密码修改成功，请重新登录')
                # logout(request)
                return redirect(reverse('app:login'))
        else:
            messages.error(request, '不能与原密码一样')
    form = changePassword()
    return render(request, 'owncenter/change_password.html', context={'form': form})


# 生成token
def createToken():
    # 生成token
    md5 = hashlib.md5()
    uuid_ = uuid.uuid4()
    md5.update(str(uuid_).encode('utf8'))
    return md5.hexdigest()


def change_head(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        user = request.user
        user.userhead = file
        user.save()
        messages.success(request, '头像修改成功')

    form = Change_head()
    data = {
        'title': '修改头像',
        'form': form,
    }
    return render(request, 'owncenter/change_head.html', context=data)


def retrieve(request):
    pass


def detail(request, id):
    data = Data_yunpan.objects.filter(pk=id).first()

    return render(request, 'data/detail.html', context={'data': data})

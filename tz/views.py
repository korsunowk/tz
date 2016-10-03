# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, render
from django.contrib import auth
from django.core.mail import send_mail
from .forms import UserCreateForm, AvatarUploadForm, CaptchaForm
from myuser.models import ExtUser
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View
import os


def name(request, args):
    args['name'] = request.user.firstname + " " + request.user.lastname[0]
    return args


class AvatarView(View):
    @staticmethod
    def new_avatar(request):
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            user.delete_avatar()
            user.avatar = request.FILES['image']
            if os.path.basename(user.avatar.name).find('.') == -1:
                user.avatar.name += '.png'
            user.save()
        return redirect('/kabinet/')

    @staticmethod
    def change_avatar(request):
        user = request.user
        user.change_avatar()

        return redirect('/kabinet/')

    @staticmethod
    def delete_avatar(request):
        user = request.user
        user.delete_avatar()
        return redirect('/kabinet/')


class UserView(View):
    @staticmethod
    def login(request):
        args = dict()
        if request.POST:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                args['user'] = request.user
                name(request, args)
                return redirect('/')
            else:
                args['login_error'] = "Net takovih"
                return render(request, 'login.html', args)
        else:
            return render(request, 'login.html', args)

    @staticmethod
    def logout(request):
        auth.logout(request)
        return redirect('/')

    @staticmethod
    def register(request):
        args = dict()
        args['form'] = UserCreateForm()
        args['captcha'] = CaptchaForm()
        if request.POST:
            newuser_form = UserCreateForm(request.POST)
            captcha_form = CaptchaForm(request.POST)
            if captcha_form.is_valid():
                if newuser_form.is_valid():
                    newuser_form.save()
                    newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                                password=newuser_form.cleaned_data['password2'])
                    auth.login(request, newuser)
                    try:
                        send_mail('Регистрация на сайте', 'Вы успешно зарегестрировались на сайте !\n Поздравляем!',
                                  'korsunowk@yandex.ua', [request.POST.get('email', '')])
                        return redirect('/')
                    except Exception as e:
                        print(e)
                        return redirect('/')
                else:
                    args['reg_error'] = 'Error.'
                    args['form'] = newuser_form
            else:
                args['captcha_error'] = 'Error.'
                args['form'] = newuser_form
        return render(request, 'register.html', args)

    @staticmethod
    def kabinet(request):
        args = dict()
        if request.user.is_authenticated():
            name(request, args)
            args['user'] = request.user
            args['upload_form'] = AvatarUploadForm()
            if request.POST:
                user = request.user
                try:
                    ExtUser.objects.get(username=request.POST.get('username', ''))
                except ExtUser.DoesNotExist:
                    user.username = request.POST.get('username', '')
                phone = str(request.POST.get('phone', ''))
                if len(phone) == 10:
                    user.phone = phone
                    user.lastname = request.POST.get('lastname', '')
                    user.firstname = request.POST.get('firstname', '')
                    user.date_of_birth = request.POST.get('date_of_birth', '')
                    user.email = request.POST.get('email', '')
                    user.save()
                    return redirect('/kabinet/')
            return render(request, 'kabinet.html', args)
        else:
            return render_to_response('index.html', args)


class UserEditView(View):
    @staticmethod
    def password_change(request):
        args = dict()
        name(request, args)
        args['user'] = request.user
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                args['errors'] = 'Успешно изменён пароль.'
            else:
                args['errors'] = 'Не удалось изменить пароль. Проверке правильность ввода.'

        return render(request, 'kabinet.html', args)

    @staticmethod
    def delete_user(request):
        args = dict()
        args['user'] = request.user
        name(request, args)
        if request.method == 'POST':
            user = ExtUser.objects.get(username=request.user.username)
            user.suicide()
        return redirect('/')


def index(request):
    args = dict()
    if request.user.is_authenticated():
        args['user'] = request.user
        name(request, args)

    return render_to_response('index.html', args)


class ContactView(View):
    @staticmethod
    def get(request):
        args = dict()
        if request.user.is_authenticated():
            args['user'] = request.user
            name(request, args)
        return render(request, 'contacts.html', args)

    @staticmethod
    def post(request):
        args = dict()
        if request.user.is_authenticated():
            args['user'] = request.user
            name(request, args)
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '') + "\n message from : " + request.POST.get('sender', '')
        sender = 'korsunowk@yandex.ua'
        recipients = ['kaleka132@gmail.com']
        if subject and message and request.POST.get('sender', ''):
            try:
                send_mail(subject, message, sender, recipients)
                args['send_success'] = 'Ваше сообщение успешно отправлено.'
            except Exception as e:
                print(e)
                args['send_error'] = 'Ваше сообщение не удалось отправить.'
        return render(request, 'contacts.html', args)


def vk_callback(request):
    from httplib2 import Http
    import vk
    import json
    import datetime

    resp, content = Http().request(uri='https://oauth.vk.com/access_token?client_id=5649330&'
                                       'client_secret=qZjV2yMgO092tVjKJ2AP&'
                                       'redirect_uri=http://127.0.0.1:8000/vk_callback&'
                                       'code='+request.GET.get('code', ''), method='GET')

    content = json.loads(content.decode('ascii'))
    token = content['access_token']
    user_id = content['user_id']
    email = content['email']
    session = vk.Session(access_token=token)
    new_user_data = vk.API(session=session).users.get(user_ids=user_id, fields=['bdate'])[0]
    new_user = ExtUser.objects.get_or_create(
        username='vk_id: '.__add__(user_id.__str__()),
        email=email,
        firstname=new_user_data['first_name'],
        lastname=new_user_data['last_name'],
        date_of_birth=datetime.datetime.strptime(new_user_data['bdate'].replace('.', '-'), '%d-%m-%Y')
    )

    auth.login(request, new_user[0])
    return redirect('/')

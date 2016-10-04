# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.contrib import auth
from django.core.mail import send_mail
from .forms import UserCreateForm, AvatarUploadForm, CaptchaForm
from myuser.models import ExtUser
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View, CreateView
import facebook
import os


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
                return redirect('/kabinet/')
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
                        return redirect('/kabinet/')
                    except Exception as e:
                        print(e)
                        return redirect('/kabinet/')
                else:
                    args['reg_error'] = 'Error.'
                    args['form'] = newuser_form
            else:
                args['captcha_error'] = 'Error.'
                args['form'] = newuser_form
        return render(request, 'register.html', args)


class UserEditView(View):
    @staticmethod
    def kabinet(request):
        args = dict()
        if request.user.is_authenticated():
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
            return redirect('/')

    @staticmethod
    def password_change(request):
        args = dict()
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
        user = ExtUser.objects.get(username=request.user.username)
        user.suicide()
        return redirect('/')


class ContactView(View):
    args = dict()

    @staticmethod
    def get(request):
        return render(request, 'contacts.html')

    @staticmethod
    def post(request):
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '') + "\n message from : " + request.POST.get('sender', '')
        sender = 'korsunowk@yandex.ua'
        recipients = ['kaleka132@gmail.com']
        if subject and message and request.POST.get('sender', ''):
            try:
                send_mail(subject, message, sender, recipients)
                ContactView.args['send_success'] = 'Ваше сообщение успешно отправлено.'
            except Exception as e:
                print(e)
                ContactView.args['send_error'] = 'Ваше сообщение не удалось отправить.'
        return render(request, 'contacts.html', ContactView.args)


class CallbackView(View):

    @staticmethod
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
        return redirect('/kabinet')

    @staticmethod
    def facebook_callback(request):
        from tz import settings
        from httplib2 import Http
        import json
        import datetime
        import requests
        from django.core.files import File

        code = request.GET.get('code', False)
        resp, content = Http().request(uri='https://graph.facebook.com/v2.7/oauth/access_token?client_id=%s&'
                                           'client_secret=%s&'
                                           'redirect_uri=http://127.0.0.1:8000/facebook_callback/&'
                                           'code=%s' % (settings.FACEBOOK_APP, settings.FACEBOOK_SECRET, code),
                                       method='GET')

        content = json.loads(content.decode('ascii'))
        token = content['access_token']
        session = facebook.GraphAPI(access_token=token)
        args = {'fields': 'name,email,birthday,picture'}
        new_user_data = session.get_object(id='me', **args)

        new_user = ExtUser.objects.get_or_create(
            username=new_user_data['name'],
            email=new_user_data['email'],
            firstname=new_user_data['name'].split()[0],
            lastname=new_user_data['name'].split()[1],
            date_of_birth=datetime.datetime.strptime(new_user_data['birthday'].replace('/', '-'), '%m-%d-%Y')
        )
        with open('media/tmp_avatar.jpg', 'wb') as file:
            file.write(requests.get(new_user_data['picture']['data']['url']).content)
        with open('media/tmp_avatar.jpg', 'rb') as file:
            new_user[0].avatar.save(name="media/%s's_avatar.jpg" % new_user_data['name'],
                                    content=File(file))
        os.remove('media/tmp_avatar.jpg')
        auth.login(request, new_user[0])
        return redirect('/kabinet/')


class CreateUser(CreateView):
    form_class = UserCreateForm
    template_name = 'register.html'
    success_url = '/kabinet/'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect(self.success_url)

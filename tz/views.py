# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib import auth
from django.core.mail import send_mail
from .forms import UserCreateForm
from myuser.models import ExtUser
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def name(request, args):
    args['name'] = request.user.firstname + " " + request.user.lastname[0]
    return args


def index(request):
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        args['user'] = request.user
        name(request, args)

    return render_to_response('index.html', args)


def contact(request):
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        args['user'] = request.user
        name(request, args)
    if request.POST:
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
        return render_to_response('contacts.html', args)

    else:
        return render_to_response('contacts.html', args)


def login(request):
    args = {}
    args.update(csrf(request))
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
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return render_to_response("index.html", RequestContext(request))


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreateForm()
    if request.POST:
        newuser_form = UserCreateForm(request.POST)
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
                args['reg_error'] = 'Error with email mess'
                args['form'] = newuser_form
        else:
            args['reg_error'] = 'Error.'
            args['form'] = newuser_form
    return render_to_response('register.html', args)


def kabinet(request):
    args = {}
    args.update(csrf(request))
    name(request, args)
    if request.user.is_authenticated():
        args['user'] = request.user
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

        return render_to_response('kabinet.html', args)
    else:
        return render_to_response('index.html', args)


def password_change(request):
    args = {}
    args.update(csrf(request))
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

    return render_to_response('kabinet.html', args)


def delete_user(request):
    args = {}
    args.update(csrf(request))
    args['user'] = request.user
    name(request, args)
    if request.method == 'POST':
        user = ExtUser.objects.get(username=request.user.username)
        user.delete()
        args['delet'] = 'Аккаунт успешно удалён из базы данных.'
    return redirect('/')

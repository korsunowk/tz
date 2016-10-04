from django import forms
from myuser.models import ExtUser
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField


class UserCreateForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'enter your username', 'required': 'required'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'required': 'required'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'enter your phone number', 'required': 'required'}))
    firstname = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'enter your firstname', 'required': 'required'}))
    lastname = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'enter your lastname', 'required': 'required'}))
    date_of_birth = forms.CharField(required=True, widget=forms.TextInput(attrs={'required': 'required', 'id': 'date'}))

    captcha = CaptchaField()

    class Meta:
        model = ExtUser
        fields = ("username", "email", 'phone', 'firstname', 'lastname', 'date_of_birth', "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserChangeForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    date_of_birth = forms.CharField(required=True)


class AvatarUploadForm(forms.Form):
    image = forms.ImageField()


class CaptchaForm(forms.Form):
    captcha = CaptchaField()

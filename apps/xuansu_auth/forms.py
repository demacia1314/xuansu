from django import forms
from apps.forms import FormMixin
from django.core.cache import cache
from .models import User

class LoginForm(forms.Form,FormMixin):
    account = forms.CharField(max_length=32,min_length=6,error_messages={'max_length':'账号最多32位','min_length':'账号最少6位'})
    password = forms.CharField(max_length=32,min_length=8,error_messages={'max_length':'密码最多32位','min_length':'密码最少8位'})
    remember = forms.BooleanField(required=False)

class RegisterForm(forms.Form,FormMixin):
    username = forms.CharField(max_length=16,min_length=2,error_messages={'max_length':'用户名最多16位','min_length':'用户名最少2位'})
    account = forms.CharField(max_length=32,min_length=6,error_messages={'max_length':'账号最多32位','min_length':'账号最少6位'})
    password = forms.CharField(max_length=32,min_length=8,error_messages={'max_length':'密码最多32位','min_length':'密码最少8位'})
    email = forms.EmailField(max_length=64,error_messages={'invalid':'请输入有效的邮箱地址'})
    imageCaptcha = forms.CharField(max_length=4,min_length=4,error_messages={'max_length':'图形验证码为4位','min_length':'图形验证码为4位'})
    emailCaptcha = forms.CharField(max_length=6,min_length=6,error_messages={'max_length':'邮箱验证码为6位','min_length':'邮箱验证码为6位'})

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        account = cleaned_data.get('account')
        email = cleaned_data.get('email')
        imageCaptcha = cleaned_data.get('imageCaptcha')
        cacheImageCaptcha = cache.get(imageCaptcha)
        emailCaptcha = cleaned_data.get('emailCaptcha')
        cacheEmailCaptcha = cache.get(email)


        if not imageCaptcha or cacheImageCaptcha.lower() != imageCaptcha.lower():
            raise forms.ValidationError('图形验证码错误')
        if not emailCaptcha or cacheEmailCaptcha.upper() != emailCaptcha.upper():
            raise forms.ValidationError('邮箱验证码错误')

        accountExists = User.objects.filter(account=account).exists()
        emailExists = User.objects.filter(email=email).exists()
        if accountExists:
            raise forms.ValidationError('该账号已被注册')
        if emailExists:
            raise forms.ValidationError('该邮箱已被注册')
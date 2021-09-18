from django.contrib.auth import login,logout,authenticate,get_user_model
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.http import HttpResponse
from utils import restful
from django.shortcuts import redirect,reverse
from utils.captcha.xuansu_captcha import ImageCaptcha,EmailCaptcha
from io import BytesIO
from django.core.cache import cache

User = get_user_model()

@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data.get('account')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        print(account)
        user = authenticate(request,account=account,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return  restful.ok()
            else:
                return restful.result(message='该账号封禁中')
        else:
            return restful.params_error()
    else:
        errors = form.get_errors()
        return restful.result(code=400,message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

@require_POST
def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        account = form.cleaned_data.get('account')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')

        user = User.objects.create_user(username=username,account=account,password=password,email=email)
        user.save()
        login(request,user)

        return restful.ok()
    else:
        errors = form.get_errors()
        return restful.result(code=400, message=errors)

def image_captcha(request):
    text,image = ImageCaptcha.gene_code()
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()

    cache.set(text.lower(),text.lower(),5*60)

    return response

def email_captcha(request):
    email = request.GET.get('email')
    send_email = EmailCaptcha(form_addr='automaticpython@163.com',password='DQTPQCGNZYODTXVO',smtp_server='smtp.163.com')
    ret = send_email.send_captcha_email(to_addr=email,head='玄素测试')

    cache.set(email,send_email.captcha,5*60)

    return restful.ok()
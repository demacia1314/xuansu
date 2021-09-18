from django.urls import path
from . import views

app_name = 'xuansu_auth'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('image_captcha/',views.image_captcha,name='image_captcha'),
    path('email_captcha/',views.email_captcha,name='email_captcha'),
    path('register/',views.register_view,name='register'),
]
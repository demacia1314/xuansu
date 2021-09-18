from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models

class UserManager(BaseUserManager):
    def _create_user(self,username,account,password,email,**kwargs):
        if not account:
            raise ValueError('请传入账号')
        if not password:
            raise ValueError('请传入密码')
        if not username:
            raise ValueError('请传入用户名')

        user = self.model(username=username,account=account,password=password,email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,username,account,password,email,**kwargs):
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = False
        return self. _create_user(username,account,password,email,**kwargs)

    def create_superuser(self,username,account,password,email,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self. _create_user(username,account,password,email,**kwargs)


class User(AbstractBaseUser,PermissionsMixin):
    #不使用默认的自增长主键,使用shortuuid
    uid = ShortUUIDField(primary_key=True)
    account = models.CharField(max_length=32,unique=True)
    telephone = models.CharField(max_length=11,unique=True,null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'account'  #该字段用于验证,默认使用username
    REQUIRED_FIELDS = ['username','email']  #该字段在create superuser时会提示你输入的字段,包括USERNAME_FIELD和password(默认)
    EMAIL_FIELD = 'email'  #该字段用于发送邮件

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
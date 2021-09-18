# -*- coding: utf-8 -*-
# @Author: huangyong
# @Date:   2016-10-29 22:18:38
# @Last Modified by:   Administrator
# @Last Modified time: 2016-11-21 20:08:31
import random
# pip install Pillow
# Image:是一个画板(context),ImageDraw:是一个画笔, ImageFont:画笔的字体
from PIL import Image,ImageDraw,ImageFont
import time
import os
import string
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# Captcha验证码

class ImageCaptcha(object):
    # 把一些常量抽取成类属性
    #字体的位置
    font_path = os.path.join(os.path.dirname(__file__),'verdana.ttf')
    # font_path = 'utils/captcha/verdana.ttf'
    #生成几位数的验证码
    number = 4
    #生成验证码图片的宽度和高度
    size = (100,40)
    #背景颜色，默认为白色 RGB(Re,Green,Blue)
    bgcolor = (0,0,0)
    #随机字体颜色
    random.seed(int(time.time()))
    fontcolor = (random.randint(200,255),random.randint(100,255),random.randint(100,255))
    # 验证码字体大小
    fontsize = 20
    #随机干扰线颜色。
    linecolor = (random.randint(0,250),random.randint(0,255),random.randint(0,250))
    # 是否要加入干扰线
    draw_line = True
    # 是否绘制干扰点
    draw_point = True
    # 加入干扰线的条数
    line_number = 3

    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    #用来随机生成一个字符串(包括英文和数字)
    # 定义成类方法,然后是私有的,对象在外面不能直接调用
    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.SOURCE,cls.number))#number是生成验证码的位数

    #用来绘制干扰线
    @classmethod
    def __gene_line(cls,draw,width,height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill = cls.linecolor)

    # 用来绘制干扰点
    @classmethod
    def __gene_points(cls,draw,point_chance,width,height):
        chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    #生成验证码
    @classmethod
    def gene_code(cls):
        width,height = cls.size #宽和高
        image = Image.new('RGBA',(width,height),cls.bgcolor) #创建画板
        font = ImageFont.truetype(cls.font_path,cls.fontsize) #验证码的字体
        draw = ImageDraw.Draw(image)  #创建画笔
        text = cls.gene_text() #生成字符串
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) / 2),text,font= font,fill=cls.fontcolor) #填充字符串
        # 如果需要绘制干扰线
        if cls.draw_line:
            # 遍历line_number次,就是画line_number根线条
            for x in range(0,cls.line_number):
                cls.__gene_line(draw,width,height)
        # 如果需要绘制噪点
        if cls.draw_point:
            cls.__gene_points(draw,10,width,height)

        return (text,image)

class EmailCaptcha(object):
    def __init__(self,form_addr,password,smtp_server,sign='玄素'):
        self.from_addr = form_addr
        self.password = password
        self.smtp_server = smtp_server
        self.sign = '['+sign+']'
        self.staff_sign = '['+sign+'内部测试'+']'
        self.captcha = None



    def create_captcha(self,number):
        SOURCE = list(string.ascii_letters)
        for index in range(0, 10):
            SOURCE.append(str(index))
        return ''.join(random.sample(SOURCE, number))

    def _send_email(self,to_addr,head,text,text_type,encode='utf-8'):
        text = self.sign+text
        print(text)
        message = MIMEText(text,text_type,encode)

        message['From'] = formataddr(pair=(self.staff_sign,self.from_addr))
        message['To'] = Header(to_addr)
        message['Subject'] = Header(head)
        try:
            server = smtplib.SMTP_SSL(self.smtp_server)
            server.login(self.from_addr, self.password)
            server.sendmail(self.from_addr, to_addr, message.as_string())
        except Exception as error:
            ret = error
        else:
            ret = 'Email send success'
        finally:
            server.quit()

        return ret

    def send_captcha_email(self,to_addr,head,text_type='plain',encode='utf-8'):
        captcha = self.create_captcha(6).upper()
        self.captcha = captcha
        message_template_header = '亲爱的用户,您的验证码为:'
        message_template_footer = ',请勿告诉他人哦~'
        text = message_template_header+captcha+message_template_footer
        return self._send_email(to_addr=to_addr,head=head,text=text,text_type=text_type,encode=encode)


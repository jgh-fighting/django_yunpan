from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^index/(?P<page>\d+)', view=index,name='index'),
    url(r'^detail/(?P<id>\d+)', view=detail,name='detail'),
    #注册
    url(r'^register/', view=useregister,name='register'),
    url(r'^activate/', view=useractivate,name='activate'),
    url(r'^check_activateMail/(.*)', view=check_activateMail,name='check_activateMail'),
    #登录退出
    url(r'^login/', view=userlogin,name='login'),
    url(r'^logout/', view=userlogout,name='logout'),
    url(r'^person_info/', view=person_info,name='Personal_information'),
    #修改密码
    url(r'^change_password/', view=change_password,name='change_password'),
    url(r'^send_mail/', view=sendMail,name='send_mail'),
    url(r'^checkMail/(.*)', view=checkMail,name='checkMail'),
    #修改个人信息
    url(r'^change_head/', view=change_head,name='change_head'),
    url(r'^retrieve/', view=retrieve,name='retrieve'),
]


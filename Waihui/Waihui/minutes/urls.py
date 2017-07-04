from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<entry_id>[0-9]+)/$', views.entry_detail, name='entry_detail'),
    url(r'^(?P<entry_id>[0-9]+)/qrshow/$', views.qrcode_show, name='qrcode_show'),
    url(r'^(?P<entry_id>[0-9]+)/q/$', views.qr_jumper, name='qr_jumper'),
    url(r'^(?P<entry_id>[0-9]+)/wxsignin/$', views.wechat_signin, name='wechat_signin'),
    url(r'^(?P<entry_id>[0-9]+)/trysqrshow/$', views.trysqrcode_show, name='trysqrcode_show'),
    url(r'^(?P<entry_id>[0-9]+)/trysq/$', views.trysqr_jumper, name='trysqr_jumper'),
    url(r'^(?P<entry_id>[0-9]+)/tryswxsignin/$', views.tryswx_signin, name='trys'),
    url(r'^(?P<entry_id>[0-9]+)/trys/$', views.trysfield, name='trys'),
    url(r'^(?P<entry_id>[0-9]+)/getattendees/$', views.get_attendees, name='get_attendees'),
]

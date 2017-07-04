 # -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from cStringIO import StringIO
from minutes.models import *
from minutes.forms import *
from minutes.statics import *
import urllib2
import json
import qrcode

def act_signinmeeting(display_name, department, phonenumber, entry, wx_id):
    profile = Profile(
        display_name=display_name,
        department=department,
        phonenumber=phonenumber,
        wx_id=wx_id)
    profile.save()
    profile.entries.add(entry)
    result = "OK, " + unicode(display_name) + _(u", 您已经成功签到，收藏该地址获取会议纪要")
    return result

def act_wxqrget_wx_id(request):
    if request.method == 'GET':
        code = request.GET['code']
        req = urllib2.urlopen("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+APPID+"&secret="+SECRET+"&code="+ str(code) +"&grant_type=authorization_code")
        json_data = json.loads(req.read())
        if json_data.get('openid'):
            wx_id = json_data.get('openid')
            request.session['wx_id'] = wx_id
            return wx_id
        else:
            return HttpResponse(json_data)
    else:
        return False

def act_get_attendees(entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    profile = entry.attendees.all()
    rjson = serializers.serialize("json", profile)
    # response = HttpResponse()
    # response['Content-Type'] = "text/javascript"
    # response.write(rjson)
    return rjson
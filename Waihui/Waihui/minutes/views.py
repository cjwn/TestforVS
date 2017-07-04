 # -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from cStringIO import StringIO
from minutes.models import *
from minutes.forms import *
from minutes.acts import *
from minutes.statics import *
import urllib2, json, qrcode



def index(request):
    entrys=Entry.objects.all()
    return render(request, "index.html", locals())


def generate_qrcode(request, data):
    img = qrcode.make(data.replace("[q]","?"))
    buf = StringIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")
    response['Last-Modified'] = 'Sun, 10 Jul 2016 12:05:03 GMT'
    response['Cache-Control'] = 'max-age=31536000'
    return response


def entry_detail(request, entry_id):
    if 'result' in request.session:
        result = request.session['result']
    entry = get_object_or_404(Entry, id=entry_id)
    rjson = act_get_attendees(entry_id)
    return render(request, "entry_detail.html", locals())


def qrcode_show(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    appid = APPID
    qr = "/qr/http://"
    return render(request, "qrcode_show.html", locals())

def qr_jumper(request, entry_id):
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + APPID + "&redirect_uri=http://" + request.META['HTTP_HOST'] + "/minutes/"+ entry_id +"/wxsignin/&response_type=code&scope=snsapi_base#wechat_redirect"
    return HttpResponseRedirect(url)

def wechat_signin(request, entry_id):
    wx_id = act_wxqrget_wx_id(request)
    if wx_id == False:
        wx_id = request.session['wx_id']
    entry = get_object_or_404(Entry, id=entry_id)
    if Profile.objects.filter(wx_id=wx_id):

        profile = get_object_or_404(Profile, wx_id=wx_id)
        if profile.entries.filter(id=entry.id):
            result = _(u"之前已经签到过了")
        else:
            profile.entries.add(entry)
            if profile.entries.filter(id=entry.id):
                result = _(u"您已成功签到")            
        request.session['result'] = result
        return HttpResponseRedirect(reverse('entry_detail', args=[entry_id]))
    else:
        if request.method == 'POST':
            uf = AttendForm(request.POST)
            if uf.is_valid():
                display_name = uf.cleaned_data['display_name']
                department = uf.cleaned_data['department']
                phonenumber = uf.cleaned_data['phonenumber']
                result = act_signinmeeting(display_name=display_name, department=department, phonenumber=phonenumber, entry=entry, wx_id=wx_id)
                # return HttpResponseRedirect(reverse('entry_detail', args=[entry_id]))
                return HttpResponseRedirect(reverse('entry_detail', args=[entry_id])) 
            return HttpResponse('非法操作')    
        else:
            uf = AttendForm()
            result = "请将参会信息填写完整"
            return render(request, "easy_signin.html", locals())

def trysqrcode_show(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    appid = APPID
    qr = "/qr/"
    return render(request, "trysqrcode_show.html", locals())

def trysqr_jumper(request, entry_id):
    testurl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + APPID + "&redirect_uri=http://" + request.META['HTTP_HOST'] + "/minutes/"+ entry_id +"/trys/&response_type=code&scope=snsapi_userinfo#wechat_redirect"
    return HttpResponseRedirect(testurl)

def tryswx_signin(request, entry_id):
    # wx_id = 'onlpmwit78qut1273l9jdx5LJgac'
    wx_id = act_wxqrget_wx_id(request)
    if wx_id == False:
        wx_id = request.session['wx_id']
    entry = get_object_or_404(Entry, id=entry_id)
    if Profile.objects.filter(wx_id=wx_id):
        profile = get_object_or_404(Profile, wx_id=wx_id)
        if profile.entries.filter(id=entry.id):
            return HttpResponse("already, "+profile.display_name)
        else:
            return HttpResponse("yes, "+profile.display_name)
    else:
    # profile = Profile.objects.get(wx_id=wx_id)
    # entry = get_object_or_404(Entry, id=entry_id)
    # profile.entry.add(entry)
        if request.method == 'POST':
            uf = AttendForm(request.POST)
            if uf.is_valid():
                display_name = uf.cleaned_data['display_name']
                department = uf.cleaned_data['department']
                phonenumber = uf.cleaned_data['phonenumber']
                result = act_signinmeeting(display_name=display_name, department=department, phonenumber=phonenumber, entry=entry, wx_id=wx_id)
                # return HttpResponseRedirect(reverse('entry_detail', args=[entry_id]))
                return HttpResponse(result) 
            return HttpResponse('非法操作')    
        else:
            uf = AttendForm()
            result = "请将参会信息填写完整"
            return render(request, "easy_signin.html", locals())
   
def trysfield(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    # attended_entrie = entry.attended_entrie.all()
    # test_field = entry.test_field.all()
    profile_set = entry.attendees.all()
    # 没写relate_name就是_set写了就是其自身
    return render(request, "trys.html", locals())    

def get_attendees(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    profile = entry.attendees.all()
    rjson = serializers.serialize("json", profile)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(rjson)
    return response
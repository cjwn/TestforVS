 # -*- coding: utf-8 -*-
import pytz, json, datetime
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.utils import translation, timezone
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
# from django import forms
# from login.models import User
from main.act import act_signup
from main.act import act_userlogin
# from main.act import act_jisuan
from main.act import act_addlanguage
from main.act import act_showuser
from main.act import act_showindividual
from main.act import act_addtopic
from main.act import act_htmllogin
from main.act import act_getlanguage
from main.act import act_addsku
from main.act import act_addrts
from main.act import act_addplan
from main.act import act_getinfo
from main.act import act_getanotis
from main.act import act_addorder
from main.act import act_booksku
from main.act import act_assignid_sku_topic
from main.act import act_generate_skus
# from main.act import act_cancelsku
from main.act import act_provider_cancel_sku
from main.act import act_buyer_cancel_sku
from main.act import act_provider_repick
from main.act import act_provider_ready_sku
from main.act import act_buyer_ready_sku
from main.act import act_expand_skus
from main.act import act_expand_orders
from main.act import act_edit_provider_profile
from main.act import act_upload_provider_avatar
from main.act import act_buyer_feedback_sku
from main.act import act_provider_feedback_sku
from main.act import act_buyer_cancel_order
from main.act import act_htmllogout
from main.act import act_orderpaid

from main.ds import  ds_getanoti

from main.models import User
from main.models import Language
from main.models import Provider
from main.models import Buyer
from main.models import Topic
from main.models import Sku
from main.models import ReplyToSku
from main.models import Plan
from main.models import Notification
from main.models import Order

from main.forms import LoginForm
from main.forms import SignupForm
from main.forms import AddSkuForm
from main.forms import AddRTSForm
from main.forms import AddPlanForm
from main.forms import OrderForm
from main.forms import HoldSkuForm
from main.forms import BookSkuForm
from main.forms import ScheduleForm
from main.forms import CancelSkuForm
from main.forms import RoomlinkForm
from main.forms import ProviderProfileForm
from main.forms import ProviderAvatarForm
from main.forms import ProviderFeedbackSkuForm
from main.forms import BuyerFeedbackSkuForm
from main.forms import PlaceSkuForm

def url_homepage(request):
    language = act_getlanguage(request)
    # user_language = language
    # translation.activate(user_language) 系统已经可以自动判断，这个激活暂时不需要
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    timezone.activate(pytz.timezone("Asia/Shanghai"))
    now_tz = timezone.now()
    info = act_getinfo(request)
    heading = _(u'Our hompage heading')
    return render(request, "main/home.html", locals())

def url_signup(request):
    '''用户通过浏览器将表单内容post到/signup/post后来到这里'''
    uf = SignupForm()
    language = act_getlanguage(request)
    msg = request.method + language
    if request.method == 'POST':
        uf = SignupForm(request.POST)
        if uf.is_valid():
            nickname = uf.cleaned_data['nickname']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            result = act_signup(password=password, nickname=nickname, email=email,
                http_language=language)
            msg = result + language
    info = act_getinfo(request)
    return render(request, "main/signup.html", {'info':info, 'form':uf, 'msg':msg})
    # act_signup()

def url_login_new(request):    
    uf = LoginForm(request.POST)
    msg = ''
    next = ''
    info = act_getinfo(request)
    if request.GET:  
       next = request.GET['next']
    if request.method == 'POST':
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            result = act_userlogin(request, username, password)
            if result == "not_active":
                msg = _(u'Login failed, user is not active.')
            elif result == "none_user":
                msg = _(u'Guess what? Login failed.')
            else:
                if next == '':
                    return HttpResponseRedirect(reverse('main:home'))
                else :
                    return HttpResponseRedirect(next)
            return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg, 'next':next})
        else:
            msg = _(u'form not valid')
            return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg})
    else:
        return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg, 'next':next})

def url_login(request):
    uf = LoginForm(request.POST)
    msg = ''
    next = ''
    info = act_getinfo(request)
    if request.GET:  
       next = request.GET['next']
    if request.method == 'POST':
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    info = act_getinfo(request)
                    act_htmllogin(user)
                    if next == '':
                        return render(request, "main/right.html", {'info':info, 'username':username})
                    else:
                        return HttpResponseRedirect(next)
                else:
                    msg = _(u'Login failed, user is not active.')
                    return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg, 'next':next})
            else:
                msg = _(u'Guess what? Login failed.')
                return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg, 'next':next})
        else:
            msg = _(u'form not valid')
            return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg})
        # elif uf.is_valid():
        #     name=uf.cleaned_data['name']
        #     return render(request, 'main.test_result.html',{'uf':uf})
    else:
        return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg, 'next':next})

# @login_required
def url_logout(request):
    info = act_getinfo(request)
    logout(request)
    act_htmllogout(info['current_user'])
    return HttpResponseRedirect(reverse('main:home'))

def url_tc(request, offset_id):
    return HttpResponse(offset_id)

def url_tutor(request, offset_id):
    '''For show tutor home page'''
    id = int(offset_id)
    act = act_showindividual(id, 'provider')
    return HttpResponse(act.status)

def url_orderlist(request):
    info = act_getinfo(request)
    current_user = info['current_user']
    timezone_now = timezone.now()
    orders = current_user.buyer.order_set.all()
    msg1 = str(orders)
    orders = act_expand_orders(orders)
    msg2 = str(orders)
    orders_to_pay_list = []
    for order in orders:
        if not hasattr(order, 'sku_is_past') and order.status == 1:
                orders_to_pay_list.append(order)
    return render(request, "main/orderlist.html", locals())


def url_showorder(request, order_id):
    '''展示order页面，兼容需付款order的情况，文字描述通过session传输'''
    info = act_getinfo(request)
    current_user = act_getinfo(request).get('current_user')
    order = get_object_or_404(Order, id=order_id)
    skus_topic = json.loads(order.skus_topic)
    for sku in order.skus.all():
        topic_id = (item for item in skus_topic if item["sku_id"] == sku.id).next()['topic_id']
        topic = get_object_or_404(Topic, id=topic_id)
    heading = _(u'Order Summary')
    if 'heading' in request.session:
        heading = request.session['heading']
    if 'msg' in request.session:
        msg = request.session['msg'] + str(type(skus_topic)) + str(skus_topic)
    # msg = order.object.all()
    return render(request, 'main/showorder.html', locals())

def url_buyer_cancel_order(request, order_id):
    info = act_getinfo(request)
    order = Order.objects.get(id=order_id)
    if info['current_user'].buyer == order.buyer:
        result = act_buyer_cancel_order(info['current_user'], order)
        heading = _(u'Order canceled')
        msg = str(order) + _(u'已经被取消') 
    else:
        return HttpResponse(_(u'Not the order''s buyer'))
    return render(request, 'main/ordercanceled.html', locals())

def url_lesson_prepare(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'sku')
    return HttpResponse(act)

def url_lesson_summarize(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'sku')
    return HttpResponse(act)

def url_lesson_rate(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'sku')
    return HttpResponse(act)

def url_classroom(request):
    pass

def url_user(request,offset_id):
    id = int(offset_id)
    user = act_showindividual(id, 'user')
    usern = user.username
    email = user.email 
    password = user.password
    result = usern + email + password
    return HttpResponse(result)

@login_required
def url_replytosku(request, sku_id):
    '''handling the replys to sku,'''
    info = act_getinfo(request)
    current_user = info['current_user']
    sku = Sku.objects.get(id=sku_id)
    uf = AddRTSForm(request.POST)
    uf.fields['reply_to'].queryset = ReplyToSku.objects.filter(sku=sku)
    is_involved = (current_user.provider == sku.provider) or (sku.buyer.filter(id=current_user.buyer.id).exists())
    if is_involved:
        msg = request.method
        if request.method == 'POST':
            if uf.is_valid():
                content = uf.cleaned_data['content']
                replyto = uf.cleaned_data['reply_to']
                if current_user.provider == sku.provider:
                    type = 1    
                else:
                    type = 0
                result = act_addrts(user=current_user, type=type, content=content, reply_to=replyto, sku=sku)
                msg = result
            else:
                msg = "validation failed"
        else:
            pass
    else:
        msg = 'you are not involved in this class'
    return render(request, "main/addrts.html", {'info':info, 'uf':uf, 'msg':msg, 'heading':"Reply to Sku", 'sku_id':sku.id, 'is_involved':is_involved})

@login_required
def url_addplan(request, sku_id):
    info = act_getinfo(request)
    current_user = request.user
    uf = AddPlanForm(request.POST)
    sku = get_object_or_404(Sku, id=sku_id)
    if current_user != sku.provider.user:
        msg = "no"
    else:
        msg = request.method
        topic = sku.topic
        if request.method == 'POST':
            if uf.is_valid():
                status = uf.cleaned_data['status']
                content = uf.cleaned_data['content']
                assignment = uf.cleaned_data['assignment']
                slides = uf.cleaned_data['slides']
                roomlink = uf.cleaned_data['roomlink']
                materiallinks = uf.cleaned_data['materiallinks']
                materialhtml = uf.cleaned_data['materialhtml']
                voc = uf.cleaned_data['voc']
                copy_from = uf.cleaned_data['copy_from']
                sumy = uf.cleaned_data['sumy']
                result = act_addplan(sku=sku, topic=topic, status=status, content=content,
                                     assignment=assignment, slides=slides, roomlink=roomlink,
                                     materialhtml=materialhtml, materiallinks=materiallinks, voc=voc,
                                     copy_from=copy_from, sumy=sumy)
                msg = result
        else:
            if sku.status != 5: sku.status = 4
        sku.save()
    return render(request, "main/addplan.html", {'info':info, 'uf':uf, 'msg':msg, 'heading':"Add a plan on SKU", 'sku':sku})

@login_required
def url_modifyplan(request, plan_id):
    info = act_getinfo(request)
    current_user = info['current_user']
    plan = get_object_or_404(Plan, id=plan_id)
    result = None
    if plan.sku.provider != current_user.provider:
        heading = _(u'教案也是有版权的，只有老师能改，别人不行哟')
        msg = str(plan.sku.provider) + ' & ' + str(current_user.provider) + _(u'不是一个用户')
        return render(request, "main/error.html", locals())   
    else:
        if request.method == 'POST':
            uf = AddPlanForm(request.POST)
            if uf.is_valid():
                status = uf.cleaned_data['status']
                content = uf.cleaned_data['content']
                assignment = uf.cleaned_data['assignment']
                slides = uf.cleaned_data['slides']
                roomlink = uf.cleaned_data['roomlink']
                materiallinks = uf.cleaned_data['materiallinks']
                materialhtml = uf.cleaned_data['materialhtml']
                voc = uf.cleaned_data['voc']
                copy_from = uf.cleaned_data['copy_from']
                sumy = uf.cleaned_data['sumy']
                result = act_addplan(sku=plan.sku, topic=plan.sku.topic, status=status, content=content,
                                     assignment=assignment, slides=slides, roomlink=roomlink,
                                     materialhtml=materialhtml, materiallinks=materiallinks, voc=voc,
                                     copy_from=copy_from, sumy=sumy, plan=plan)
                msg = result
        else:
            uf = AddPlanForm(initial={
                'status':plan.status,
                'content':plan.content,
                'assignment':plan.assignment,
                'slides':plan.slides,
                'roomlink':plan.roomlink,
                'materialhtml':plan.materialhtml,
                'materiallinks':plan.materiallinks,
                'voc':plan.voc,
                'copy_from':plan.copy_from,
                'sumy':plan.sumy})
            msg = result
        sku = plan.sku
    return render(request, "main/addplan.html", locals())

@login_required
def url_showsku(request, sku_id): 
    info = act_getinfo(request)
    current_user = act_getinfo(request).get('current_user')
    sku = get_object_or_404(Sku, id=sku_id)
    is_involved = (current_user.provider == sku.provider) or (sku.buyer.filter(id=current_user.buyer.id).exists())
    rtss = ReplyToSku.objects.filter(sku=sku)
    is_provider = True if current_user == sku.provider.user else False
    msg = str(request)
    heading = _(u'SKU #') + str(sku.id)
    return render(request, "main/showsku.html", locals())

def url_skulist(request):
    # timezone.activate(pytz.timezone("Asia/Shanghai"))
    info = act_getinfo(request)
    skus = Sku.objects.all()
    msg = str(request)
    return render(request, "main/skulist.html", {'info':info, 'heading':"There is a Sku list", 'msg':msg, 'skus':skus})

# def url_order_add(request, skus):
#     info = act_getinfo(request)
#     current_user = info['current_user']
#     for i in skus:
#         thesku = Sku.objects.filter(id=i)
#         thesku.status = 2


def url_test(request):
    info = act_getinfo(request)
    infos = ds_getanoti(Notification.objects.get(id=68))
    typeofinfos = type(info)
    typeofnotis = type(Notification.objects.get(id=68))
    return render(request, "main/mytest.html", locals())

def url_idtest(request, set_id):
    result = Test_skufunction(set_id)
    return render(request, "main/mytest", {'result':result})

@login_required
def url_dashboard(request):
    info = act_getinfo(request)
    skus = info.get('current_user').buyer.sku_set.all()
    skus = act_expand_skus(skus)
    return render(request, "main/dashboard.html",locals())

@login_required
def url_office(request):
    timezone.activate(pytz.timezone("Asia/Shanghai"))
    info = act_getinfo(request)
    skus = Sku.objects.filter(provider=info['current_user'].provider)
    skus = act_expand_skus(skus)
    return render(request, "main/office.html",locals())

@login_required
def url_notifications(request):
    info = act_getinfo(request)
    upcomming_anotis = act_getanotis(Notification.objects.filter(user=info['current_user'],open_time__gt=timezone.now()).order_by('-open_time'))
    past_anotis = act_getanotis(Notification.objects.filter(user=info['current_user'],close_time__lt=timezone.now()).order_by('-open_time'))
    return render(request, "main/notifications.html",locals())

@login_required
def url_notification_go(request, noti_id):
    info = act_getinfo(request)
    noti = get_object_or_404(Notification ,id=noti_id)
    if noti.user == info['current_user']:
        if noti.read == 0:
            noti.read = 1
            noti.save()
        return HttpResponseRedirect(ds_getanoti(noti)['link'])
    else:
    # 这说明这条noti不属于当前用户，无权查看的
        return HttpResponse('这条消息不属于当前用户，无权查看。')

@login_required
def url_addorder(request):
    '''add a order '''
    info = act_getinfo(request)
    buyer = act_getinfo(request).get('current_user').buyer
    uf = OrderForm(request.POST)
    uf.fields['skus'].queryset = Sku.objects.filter(buyer=buyer)
    if request.method == 'POST':
        if uf.is_valid():
            skus = uf.cleaned_data['skus']
            # msg = str(isinstance(skus,Sku))
            msg = act_addorder(info['current_user'], skus, buyer)
    # result = act_addorder(skus, buyer)
    # uf = OrderForm(request.POST)
    # uf.fields['skus'].queryset = Sku.objects.filter(buyer=info['current_user'].buyer)
    
    return render(request, "main/addorder.html", locals())

@login_required
def url_addsku(request):
    info = act_getinfo(request)
    current_user = info['current_user']
    skus = Sku.objects.all()
    if current_user.provider.status == 0:
        msg = "You have no rights to add class, Please be a teacher first."
    else:
        msg = request.method+", Provider: ["+str(current_user.username)+"]"
        if request.method == 'POST':
            uf = AddSkuForm(request.POST)
            if uf.is_valid():
                start_time = uf.cleaned_data['start_time']
                end_time = uf.cleaned_data['end_time']
                topic = uf.cleaned_data['topic']
                result = act_addsku(provider=current_user.provider, start_time=start_time, end_time=end_time, topic=topic)
                msg = result
        else:
            uf = AddSkuForm()
    return render(request, "main/addsku.html", locals())

def url_picktopic(request):
    info = act_getinfo(request)
    current_user = info.get('current_user')
    topics = Topic.objects.all()
    skus_timeok = Sku.objects.filter(Q(start_time__gte=timezone.now())&Q(status=0))
    if info['is_login']:
        skus_timeok = skus_timeok.exclude(provider=current_user.provider)
    # no_topics = Sku.objects.filter(topic=None)
    heading = _(u'Pick a topic')
    return render(request, 'main/picktopic.html', locals())

def url_skuintopic(request, topic_id):
    info = act_getinfo(request)
    current_user = info.get('current_user')
    skus_with_topics = Sku.objects.filter(topic_id=topic_id, status=0, buyer=None)
    skus_without_topics = Sku.objects.filter(topic=None, status=0, buyer=None)
    if info['is_login']:
        skus = (skus_with_topics|skus_without_topics).filter(start_time__gte=timezone.now())\
        .exclude(provider=current_user.provider)
    else:
        skus = (skus_with_topics|skus_without_topics).filter(start_time__gte=timezone.now())
    topic = Topic.objects.get(id=topic_id)
    heading = _(u'Pick a time and meet a teacher')
    if skus.count() == 0:
        heading = _(u'Sorry, No sku in this topic right now')
        return render(request, 'main/result.html', locals())
    return render(request, 'main/skuintopic.html', locals())

@login_required
def url_holdsku(request, topic_id, sku_id):
    '''用于选择单个sku（course）后直接下单'''
    info = act_getinfo(request)
    topic = get_object_or_404(Topic, id=topic_id)
    sku = get_object_or_404(Sku, id=sku_id)
    msg = None
    if sku.status != 0:
        msg = _(u'抱歉，该课程目前不可约了')
    if sku.provider == info.get('current_user').provider:
        msg = _(u'抱歉，不能给自己授课')
    if msg:
        return render(request, 'main/holdsku.html', locals())
    uf = PlaceSkuForm(request.POST)
    if request.method == 'POST':
        if uf.is_valid():
            buyer = info['current_user'].buyer
            # typeskuid = str(type(sku.id)) + str(type(sku_id)) #int & unicode
            sku_topic = act_assignid_sku_topic(sku_id=sku.id, topic_id=topic.id)
            # msg = str(isinstance(sku, Sku))
            result = act_addorder(buyer.user, sku, buyer, sku_topic)
            if not result:
                msg = _(u'result is false')
                return render(request, 'main/holdsku.html', locals())
            order = result['order']
            request.session['heading'] = _(u'Please pay the order')
            request.session['msg'] = result['info']
            return HttpResponseRedirect(reverse('main:showorder', args=[order.id]))
            # return render(request, 'main/result.html', locals())
    msg = str(request.POST)
    heading = _(u'Confirm your course information')
    return render(request, 'main/holdsku.html', {'info':info, 'heading':heading, 'sku':sku, 'topic':topic, 'uf':uf, 'msg':msg})

# @login_required
# def url_holdsku(request):
#     '''make a sku for order, One order can have many skus'''
#     info = act_getinfo(request)
#     current_user = info['current_user'] 
#     skus = Sku.objects.all()
#     msg = request.method+", user: ["+str(current_user.username)+"], user's buyer: ["+str(current_user.buyer)+"]"
#     if request.method == 'POST':
#         uf = HoldSkuForm(request.POST)
#         if uf.is_valid():
#             provider = uf.cleaned_data['provider']
#             topic = uf.cleaned_data['topic']
#             start_time = uf.cleaned_data['start_time']
#             end_time = uf.cleaned_data['end_time']
#             result = act_addsku(provider=provider, topic=topic, start_time=start_time, end_time=end_time, buyer=current_user.buyer)
#             msg = result
#     else:
#         uf = HoldSkuForm()    
#     return render(request, "main/addsku.html", {'info':info, 'uf':uf, 'msg':msg, 'heading':"add sku", 'skus':skus})
#     # teachers = Provider.objects.all()
#     # topics = Topic.objects.all()
#     # 
#     # return render(request, "main/addsku.html", {'teacher_list':teachers, 'topic_list':topics,})

@login_required
def url_booksku(request, topic_id, sku_id,):
    '''url name:booksku'''
    info = act_getinfo(request)
    uf = BookSkuForm(request.POST)
    topic = Topic.objects.get(id=topic_id)
    if request.method == 'POST':
        if uf.is_valid():
            buyer = info['current_user'].buyer
            result = act_booksku(sku_id=sku_id, topic=topic)
            msg = result
            return render(request, 'main/result.html', locals())   
    msg = str(request.POST)
    heading = _(u'Conform you course information')
    return render(request, 'main/booksku.html', locals())

@login_required
def url_bookresult(request):
    info = act_getinfo(request)
    msg = request.POST
    return render(request, 'main/bookresult.html', locals())

@login_required
def url_schedule(request):
    info = act_getinfo(request)
    timezone.activate(pytz.timezone("Asia/Shanghai"))
    tz = timezone.get_current_timezone()
    now_tz = timezone.now()
    info = act_getinfo(request)    
    current_user = info['current_user']
    provider = current_user.provider
    msg=''
    if info['is_provider']:
        if request.method == 'POST':
            uf = ScheduleForm(request.POST)
            if uf.is_valid():
                set_provider = uf.cleaned_data['provider']
                raw_schedule = json.loads(uf.cleaned_data['schedule'])
                schedule = []
                for raw_item in raw_schedule:
                    item = {}
                    try:
                        if raw_item.get('topic_id'):
                            item['topic'] = Topic.objects.get(id=int(raw_item.get('topic_id')))
                        item['start_time'] = tz.localize(datetime.datetime.strptime(\
                            raw_item['start_time'], "%Y-%m-%d %H:%M:%S"))
                        if raw_item.get('end_time'):
                            item['end_time'] = tz.localize(datetime.datetime.strptime(\
                                raw_item['end_time'], "%Y-%m-%d %H:%M:%S"))
                        else:
                            item['end_time'] = tz.localize(datetime.datetime.strptime(\
                                raw_item['start_time'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=30))
                        if item['start_time'] and (item['start_time']>now_tz):
                            schedule.append(item)
                    except Exception, e:
                        raise e
                # msg=schedule
                msg=act_generate_skus(provider, schedule)
        else:
            uf = ScheduleForm(initial = {'provider': provider })
        return render(request,"main/schedule.html", locals())
    else:
    # 这说明这个人不是老师
        return HttpResponse('You are not an authenticated tutor. 你不是教师，无权访问此页')

@login_required
def url_provider_cancel_sku(request, sku_id):
    info = act_getinfo(request)
    sku = Sku.objects.get(id=sku_id)
    if sku.provider.user == info['current_user']:
        if sku.status == 1:
            # 视作无伤害取消
            msg = act_provider_cancel_sku(sku, info['current_user'])
        elif sku.status == 4:
            # 视作有伤害取消
            msg = act_provider_cancel_sku(sku, info['current_user'])
        else:
            msg = _(u"这个课程的状态不适合取消")
    else:
        msg = _(u"对不起，不是老师不能取消")
    return render(request, "main/result.html", locals())

@login_required
def url_buyer_cancel_sku(request, sku_id):
    info = act_getinfo(request)
    sku = Sku.objects.get(id=sku_id)
    if info['current_user'].buyer not in sku.buyer.all():
        msg = _(u"对不起，不是这节课的学生不能取消")
    else:
        if sku.status == 1:
            msg = act_buyer_cancel_sku(sku=sku, user=info['current_user'])
        else:
            msg = _(u"状态不允许取消")
    return render(request, "main/result.html", locals())

@login_required
def url_repickpool(request):
    info = act_getinfo(request)
    if info.get('is_provider'):
        msg = _(u"对，你是教师，接下来要抢单")
        skus = Sku.objects.filter(Q(status=2)&Q(start_time__gte=timezone.now()))
    else:
        msg = _(u"对不起，不是老师不能抢单")
    return render(request, "main/repickpool.html", locals())

@login_required
def url_provider_repick(request, sku_id):
    info = act_getinfo(request)
    sku = Sku.objects.get(id=sku_id)
    if info.get('is_provider'):
        msg = act_provider_repick(sku=sku, new_provider=info['current_user'].provider)
    return render(request, "main/result.html", locals())

@login_required
def url_provider_ready_sku(request, sku_id):
    info = act_getinfo(request)
    sku = Sku.objects.get(id=sku_id)
    if info.get('is_provider'):
        if sku.has_plan():
            if request.method == 'POST':
                uf = RoomlinkForm(request.POST)
                if uf.is_valid():
                    roomlink = uf.cleaned_data['roomlink']
                    if act_provider_ready_sku(sku=sku, roomlink=roomlink):
                        return HttpResponseRedirect(reverse('main:showsku', args=[sku.id]))
            else:
                uf = RoomlinkForm(initial={'roomlink':sku.plan.roomlink})
        else:
            msg = _(u"必须备课才能上课")
    else:
        msg = _(u"对不起，不是老师不能开始上课")
    return render(request, "main/pready.html", locals())

@login_required
def url_buyer_ready_sku(request, sku_id):
    '''设定学生已准备好，之前会判断是否是这节课的学生，sku是否为6（教师已准备好），传入request与sku_id'''
    info = act_getinfo(request)
    sku = Sku.objects.get(id=sku_id)
    # sku = act_expand_skus(sku)
    if info['current_user'].buyer in sku.buyer.all():
        if sku.status == 6:
            if act_buyer_ready_sku(sku=sku):
                return HttpResponseRedirect(reverse('main:showsku', args=[sku.id]))
        elif sku.status == 7:
            msg = _(u"已经上课，通讯地址为：") + sku.plan.roomlink
        else:
            msg = _(u"对不起，教师尚未准备好")
    else:
        msg = _(u"诶，你不是这节课的学生呀")
    return render(request, "main/bready.html", locals())

def url_my_profile(request):
    info = act_getinfo(request)    
    provider = info.get('current_user').provider
    skus = act_expand_skus(Sku.objects.filter(provider=provider, status=0))
    finished_skus_count = Sku.objects.filter(Q(status=8) | Q(status=9), Q(provider=provider)).count()
    return render(request, "main/my_profile.html", locals())

def url_provider_profile(request, user_id):
    info = act_getinfo(request)    
    provider = User.objects.get(id=user_id).provider
    skus = act_expand_skus(Sku.objects.filter(provider=provider, status=0))
    finished_skus_count = Sku.objects.filter(Q(status=8) | Q(status=9), Q(provider=provider)).count()
    return render(request, "main/provider_profile.html", locals())

@login_required
def url_provider_profile_edit(request,):
    info = act_getinfo(request)
    provider = info.get('current_user').provider
    if request.method == 'POST':
        uf = ProviderProfileForm(request.POST, request.FILES)
        if uf.is_valid():
            # avatar = uf.cleaned_data['avatar']
            name = uf.cleaned_data['name']
            video = uf.cleaned_data['video']
            teaching_language = uf.cleaned_data['teaching_language']
            result = act_edit_provider_profile(provider=provider,
                                               # avatar=avatar,
                                               name=name,
                                               video=video,
                                               teaching_language=teaching_language)
    else:
        uf = ProviderProfileForm(initial={'name':provider.name,
                                          'video':provider.video,
                                          'teaching_language':provider.teaching_language.all()})
        
    return render(request, "main/provider_profile_edit.html", locals())

@login_required
def url_provider_profile_avatar(request):
    info = act_getinfo(request)
    provider = info.get('current_user').provider
    heading = "Provider's avatar"
    if request.method == 'POST':
        uf = ProviderAvatarForm(request.POST, request.FILES)
        if uf.is_valid():
            uploadact = act_upload_provider_avatar(provider=provider,
                                                   new_avatar=request.FILES['avatar'])
            if uploadact:
                result = "Your new avatar uploaded!"
    else:
        uf = ProviderAvatarForm()
    return render(request, "main/provider_profile_avatar.html", locals())

def url_providers(request):
    info = act_getinfo(request)
    providers = Provider.objects.all()
    return render(request, "main/providers.html", locals())

def url_feedback_sku(request, sku_id):
    info = act_getinfo(request)
    sku = get_object_or_404(Sku, id=sku_id)
    result = "HI there, i can't tell the info"
    if info.get('current_user').provider == sku.provider:
        identity = "provider"
        if request.method == 'POST':
            uf = ProviderFeedbackSkuForm(request.POST)
            uf.fields.get('buyer').queryset = sku.buyer.all()
            if uf.is_valid():
                questionnaire = uf.cleaned_data['questionnaire']
                comment = uf.cleaned_data['comment']
                buyer = uf.cleaned_data['buyer']
                result = act_provider_feedback_sku(questionnaire=questionnaire, comment=comment, sku=sku, buyer=buyer)
        else:
            if sku.buyer.all().count == 1:
                uf = ProviderFeedbackSkuForm(initial={'buyer':sku.buyer.all()[0]})
                # uf.fields.get('buyer').queryset = sku.buyer.all()
            else:
                uf = ProviderFeedbackSkuForm()
                uf.fields.get('buyer').queryset = sku.buyer.all()
            result = "You sure are the provider of this cousrs "
    elif info.get('current_user').buyer in sku.buyer.all():
        identity = "buyer"
        if request.method == 'POST':
            uf = BuyerFeedbackSkuForm(request.POST)
            if uf.is_valid():
                questionnaire = uf.cleaned_data['questionnaire']
                comment = uf.cleaned_data['comment']
                result = act_buyer_feedback_sku(questionnaire=questionnaire, comment=comment, sku=sku, buyer=info.get('current_user').buyer)
        else:
            uf = BuyerFeedbackSkuForm()
            result = "you sure are the buyer of this coures"
    return render(request, "main/feedback_sku.html", locals())

@login_required
def url_orderpaid(request, order_id):
    '''pay the order, args: order.id'''
    info = act_getinfo(request)
    buyer = info.get('current_user').buyer
    order = get_object_or_404(Order, id=order_id)
    act_orderpaid(order, buyer)
    heading = _(u'Order Paid')
    return render(request, "main/orderpaid.html", locals())


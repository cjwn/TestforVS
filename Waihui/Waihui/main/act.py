# -*- coding: utf-8 -*-
import pytz, json, datetime
from django.utils import translation, timezone
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from main.models import User
from main.models import Language
from main.models import Provider
from main.models import Buyer
from main.models import Topic
from main.models import TopicCategory
from main.models import Sku
from main.models import Plan
from main.models import Order
from main.models import OrderType
from main.models import Wallet
from main.models import ReplyToSku
from main.models import ReviewToProvider
from main.models import ReviewToBuyer
from main.models import Log
from main.models import Notification
from main.forms import OrderForm

from main.ds import ds_addlog
from main.ds import ds_getanoti
from main.ds import ds_noti_newreply
from main.ds import ds_get_order_cny_price
from main.ds import ds_change_provider
from main.ds import ds_sku_status_check
from main.ds import ds_sku_provider_check
from main.ds import ds_noti_tobuyer_skustart
from main.ds import ds_noti_tobuyer_noprovider
from main.ds import ds_noti_tobuyer_newplan
from main.ds import ds_noti_tobuyer_planmodified
from main.ds import ds_noti_toprovider_skubooked
from main.ds import ds_noti_toprovider_lostbuyer


from django.utils.translation import ugettext as _

MIN_CANCEL_TIME = datetime.timedelta(hours=8)
OK_CANCEL_TIME = datetime.timedelta(hours=12)
START_SOON_TIME = datetime.timedelta(minutes=30)


ORDER_MIN_CANCEL_TIME = datetime.timedelta(hours=8)
ORDER_OK_CANCEL_TIME = datetime.timedelta(hours=12)
ORDER_PAY_SOON_TIME = datetime.timedelta(minutes=15)

def act_getlanguage(request):
    language = request.LANGUAGE_CODE
    # language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    return language

def act_signup(email, password, nickname, http_language, time_zone="Asia/Shanghai"):
    '''signup a user'''
    
    language = http_language
    try:
        ulanguage = Language.objects.get(english_name=language)
    except Language.DoesNotExist:
        ulanguage = Language(english_name=language)
        ulanguage.save()
    
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password)
    user.save()

    buyer = Buyer(
        user=user,
        nickname=nickname,
        # gender=gender,
        mother_tongue=ulanguage,
        time_zone=time_zone)
    buyer.save()

    provider = Provider(
        user=user,
        status=0,
        name=nickname)
    provider.save()

    wallet = Wallet(
        user=user)
    wallet.save()

    result = "OK!" + str(email) + "." + str(nickname) + "has added"
    # except:
    #     pass
    return result

def act_userlogin(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            info = act_getinfo(request)
            return info
        else:
            return "not_active"
    else:
        return "none_user"


def act_addlanguage(chinese_name, english_name, local_name):
    '''add a language'''
    language = Language(
        chinese_name=chinese_name,
        english_name=english_name,
        local_name=local_name,)
    language.save()
    result = "OK, Language:" + local_name + " added!"
    return result

def act_addtc(name, url):
    '''add a TopicCategory'''
    topiccategory = TopicCategory(
        name=name,
        url=url)
    topiccategory.save()
    result = "OK, Topic category:" + name + " added!"
    return result

def act_addtopic(name, topic_id, status, user_id):
    '''add a Topic'''
    topic = Topic(
        name=name,
        category=Topic.objects.get(id=topic_id),
        status=status,
        creator=User.objects.get(id=user_id))
    topic.save()
    result = "OK, Topic:" + name + " added!"
    return result

def act_addsku(provider, start_time, end_time, topic=None, buyer=None, status=0):
    '''it will add a Sku'''
    # provider = Provider.objects.get(id=provider_id)
    # topic = Topic.objects.get(id=topic_id)
    if start_time>=end_time:
        result = 'Opps, end_time must be later than start_time!'
    elif Sku.objects.filter(
        Q(provider=provider) & ~Q(status = 10), 
        Q(start_time__lte=start_time, end_time__gt=start_time) 
        | Q(start_time__lt=end_time, end_time__gte=end_time) 
        | Q(start_time__gt=start_time, end_time__lt=end_time)
        ):
        result = 'Opps, Time[%s] to [%s] is not available for %s!'  % (start_time, end_time, provider)
    else:
        sku = Sku(
            provider=provider,
            status=status,
            start_time=start_time,
            end_time=end_time,
            topic=topic,
            )
        sku.save()
        if buyer is not None:
            sku.buyer.add(buyer)
        result = "OK, Sku:" + provider.name + "'s " + str(start_time) + " added!"
    return result

def act_addplan(sku, topic, status, content, assignment, slides, roomlink, materiallinks, materialhtml, voc, copy_from, sumy, plan=None):
    '''if import a plan, it will change the plan, if not, then add one'''
    if plan:
        plan.status = status
        plan.content = content
        plan.assignment = assignment
        plan.slides = slides
        plan.roomlink = roomlink
        plan.materialhtml = materialhtml
        plan.materiallinks = materiallinks
        plan.voc = voc
        plan.copy_from = copy_from
        plan.sumy = sumy
        result = "OK, Plan: " + sku.provider.name + " & " + topic.name + " modified!"
        ds_noti_tobuyer_planmodified(plan)
    else:
        plan = Plan(
            sku=sku,
            topic=topic,
            status=status,
            content=content,
            assignment=assignment,
            slides=slides,
            roomlink=roomlink,
            materialhtml=materialhtml,
            materiallinks=materiallinks,
            voc=voc,
            copy_from=copy_from,
            sumy=sumy,
            )
        plan.save()
        sku.status = 5
        sku.save()
        result = "OK, Plan: " + sku.provider.name + " & " + topic.name + " added!"
        ds_noti_tobuyer_newplan(plan)
    return result

def act_addrtp(provider_id, buyer_id, sku_id, questionnaire, score):
    '''it will add a ReviewToProvider'''
    provider = Provider.objects.get(id=provider_id)
    buyer = Buyer.objects.get(id=buyer_id)
    sku = Sku.objects.get(id=sku_id)
    rtp = ReviewToProvider(
        provider=provider,
        buyer=buyer,
        sku=sku,
        questionnaire=questionnaire,
        score=score)
    rtp.save()
    result = "OK, " + provider.name + "has leave a review on " + sku + "to " + Buyer.name
    return result

def act_addrtb(provider_id, buyer_id, sku_id):
    '''it will add a ReviewToBuyer'''
    provider = Provider.objects.get(id=provider_id)
    buyer = Buyer.objects.get(id=buyer_id)
    sku = Sku.objects.get(id=sku_id)
    rtb = ReviewToBuyer(
        provider=provider,
        buyer=buyer,
        sku=sku,
        )
    rtb.save()
    result = "OK, " + provider.name + "has leave a review to " + Buyer.name
    return result

def act_addrts(user, type, content, reply_to, sku):
    '''it will add a ReplyToSku'''
    rts = ReplyToSku(
        user=user,
        type=type,
        content=content,
        reply_to=reply_to,
        sku=sku,
        )
    rts.save()

    if rts.type == 1:
        for noti_buyer in sku.buyer.all():
            ds_noti_newreply(reply=rts, user=noti_buyer.user, type=1)
    elif rts.type == 0:
        ds_noti_newreply(reply=rts, user=sku.provider.user, type=0)
    

    result = "OK, " + user.username + " left a message of" + content
    return result

def act_updatewallet():
    pass

def act_showuser(id):
    '''it will show User information'''
    user = User.objects.get(id=id),
    return user

def act_showprovider(id):
    '''it will show Provider information'''
    provider = Provider.objects.get(id=id)
    return provider

def act_showbuyer(id):
    '''it will show Buyer information'''
    buyer = Buyer.objects.get(id=id)
    return buyer

def act_addorder(user, skus, buyer, skus_topic=None):
    '''it will add a Order'''
    if not ds_sku_status_check(skus, [0, 10]):
        return False
    if not ds_sku_provider_check(skus, buyer):
        pass
    cny_price = ds_get_order_cny_price(skus)
    order = Order(cny_price=cny_price, buyer=buyer, type=OrderType.objects.get(id=1), skus_topic=skus_topic)
    order.save()
    if isinstance(skus, Sku):
        order.skus.add(skus)
    else:
        order.skus = skus
    order.save()
    ds_addlog(client=0, action=2, user=user, order=order)
    result = _(u'Order added, need to pay: CNY¥'+ str(cny_price) +', this order includes: '+str(skus))
    result = {'info':result, 'order':order}
    return result

def act_showorder(id):
    '''it will show Order information'''
    order = Sku.objects.get(id=id)
    return order

def act_expand_orders(orders):
    '''用于扩展orders，增加不存在于 models 里的属性。'''
    orders_result = []
    for order in orders:
        setattr(order, 'payment_timeflag', '')
        if order.status == 1:
            if order.created > timezone.now():
                order.payment_timeflag = 'order is in mind'
            else:
                if datetime.timedelta(minutes=15) > (timezone.now() - order.created):
                    order.payment_timeflag = 'should_pay_soon'
                else:
                    order.payment_timeflag = 'over 15mins'
        # setattr(order, 'should_pay_soon', (datetime.timedelta() < timezone.now() - order.created < ORDER_PAY_SOON_TIME)) # 这节课是不是马上就要开始啦？目前是15分钟内
        # setattr(order, 'timedelta', timezone.now() - order.created)
        # setattr(order, 'should_pay_later', (timezone.now() - order.created > ORDER_PAY_SOON_TIME)) # 这节课是不是距离开始还早着呢
        setattr(order, 'is_paid', (order.cny_price < order.cny_paid)) # 该结束了
        for sku in order.skus.all():
            setattr(order, 'sku_is_past', (timezone.now() - sku.start_time > datetime.timedelta()))
        orders_result.append(order)
    return orders_result

def act_buyer_cancel_order(user, order, client='0'):
    '''买家主动取消订单'''
    order.status = '6'
    order.save()
    ds_addlog(client=client, action=4, user=user, order=order, character=0)
    result = "Order cancelec"
    return result

def act_showtopic(id):
    """this will show a topic"""
    topic = Topic.objects.get(id=id)
    return topic

def act_showtc(id):
    """it will show a topiccategory"""
    tc = TopicCategory.objects.get(id=id)
    return tc

def act_signtopic(provider, topic):
    pass

def act_upgrade_hp(self, theset):
    """unavailable in Models!:
    
    upgrade the hp by input a int """
    self.hp = theset
    self.save()
    return self.hp

def act_showindividual(id, c):
    '''
    this act is used for show lots of models
    such as Buyer Provider Order and User ETC.
    '''
    if c == 'buyer':
        r = act_showbuyer(id)
    elif c == 'provider':
        r = act_showprovider(id)
    elif c == 'order':
        r = act_showorder(id)
    elif c == 'user':
        r = act_showuser(id)
    # elif c == 'topic':
    #     r = ds_showtopic(id, bywhat)
    return r

def act_htmllogin(user):
    log = ds_addlog(client=0, action=0, user=user)
    return

def act_htmllogout(user):
    log = ds_addlog(client=0, action=1, user=user)
    return


def act_getinfo(request):
    if request.user.is_authenticated():
        info = {
        'is_login': True,
        'current_user': request.user
        }
        timezone.activate(pytz.timezone("Asia/Shanghai"))
        info['now_tz'] = timezone.now()
        info['anotis'] =        act_getanotis(Notification.objects.filter(user=request.user, open_time__lte=timezone.now(), close_time__gte=timezone.now()).order_by('-open_time'))
        info['unread_anotis'] = act_getanotis(Notification.objects.filter(user=request.user, open_time__lte=timezone.now(), close_time__gte=timezone.now(), read=0).order_by('-open_time'))
        if request.user.provider.status == 0:
            info['is_provider'] = False
        else:
            info['is_provider'] = True
    else:
        info = {
        'is_login': False,
        }
    return info

def act_getanotis(notis):
    anotis = []
    for noti in notis:
        anoti = ds_getanoti(noti)
        anotis.append(anoti)
    return anotis

def act_assignid_sku_topic(sku_id, topic_id):
    '''此为下单生成order中sku_topic_buyer field列表信息的功能，目前只能实现单个sku进行绑定'''
    skus_topic = []
    # for sku_id in sku_ids:
    sku_topic = {'sku_id':sku_id, 'topic_id':topic_id}
    skus_topic.append(sku_topic)

    # ds_noti_toprovider_skubooked(sku)
    skus_topic = json.dumps(skus_topic)
    # skus_topic = str(skus_topic)
    return skus_topic

def act_booksku(sku_id, topic, buyer):
    '''原则上为付款之后将sku状态定为booked'''
    sku = Sku.objects.get(id=sku_id)
    sku.topic = topic
    # sku.status = 1
    sku.save()
    sku.buyer.add(buyer)
    # ds_noti_toprovider_skubooked(sku)
    result = _(u'OK, +' + str(sku.topic) + ' booked')
    return result

def act_generate_skus(provider, schedule):
    '''生成sku，schedule 是一个list，其中每一个item都是dict，包含 topic, start_time, end_time'''
    result = []
    for item in schedule:
        result_item = ''
        if item.get('topic') and item['start_time'] and item['end_time']:
            result_item = act_addsku(
                provider=provider,
                start_time=item['start_time'],
                end_time=item['end_time'],
                topic=item.get('topic'))
            result.append(result_item)
        elif item['start_time'] and item['end_time']:
            result_item = act_addsku(
                provider=provider,
                start_time=item['start_time'],
                end_time=item['end_time'])
            result.append(result_item)
    return result

def act_provider_cancel_sku(sku, user):
    if sku.time_to_start() <= MIN_CANCEL_TIME:
        msg = _(u"马上开始了如果真要取消的话你自己联系学生做好解释工作，再找管理员取消吧。")
    elif sku.time_to_start() > MIN_CANCEL_TIME and sku.time_to_start() <= OK_CANCEL_TIME:
        sku.status = 3
        sku.save()
        ds_noti_tobuyer_noprovider(sku)
        msg = _(u"你是取消成功了，但是学生没法上课了，下回别这样了")
    else:
        if sku.buyer.exists():
            sku.status = 2
            sku.save()
            msg = _(u"恭喜，取消真轻松。你的学生会进入挽救池")
        else:
            sku.topic = None
            sku.status = 0
            sku.save()
            msg = _(u"虽然没有学生，但是也取消了")
    return msg


def act_buyer_cancel_sku(sku, user):
    if sku.status != (1 or 4):
        msg = _(u"Sorry, class status forbit you to cancel")
    else:
        if sku.buyer.count() > 1:
            # '''不知道remove对不对啊，好像是删掉这个buyer本身的意思'''
            sku.buyer.remove(user.buyer)
            msg = _(u"好了，这节课只有你不用来了")
        elif sku.buyer.count() == 1:
            # 改成保留这个sku，保留证据！
            sku.status = 10
            sku.save()
            msg = _(u"好了，取消成功，这节课不用上了")
            # 下面给这个老师再创建一个新的可约sku
            msg = msg + act_addsku(
                provider=sku.provider,
                start_time=sku.start_time,
                end_time=sku.end_time)
        ds_noti_toprovider_lostbuyer(sku=sku)
    return msg

def act_provider_repick(sku, new_provider):
    if sku.status == 2:
        msg = ds_change_provider(sku, new_provider)
        if sku.has_plan():
            sku.status = 5
        else:
            sku.status = 4
        sku.save()
    else:
        msg = _(u'这不是一节待抢课程。')
    return msg

def act_expand_skus(skus):
    '''用来扩展 skus，增加不存在于 models 里的属性。'''
    skus_result = []
    for sku in skus:
        setattr(sku, 'is_start_later', (sku.time_to_start() > START_SOON_TIME)) # 这节课是不是距离开始还早着呢
        setattr(sku, 'is_start_soon', (datetime.timedelta() < sku.time_to_start() < START_SOON_TIME)) 
        # 这节课是不是马上就要开始啦？目前是30分钟内
        setattr(sku, 'is_should_in_progress', (sku.start_time < timezone.now() < sku.end_time)) # 这节
        # 课是不是应该在进行中
        setattr(sku, 'is_past', (timezone.now() > sku.end_time)) # 该结束了
        skus_result.append(sku)
    return skus_result


def act_provider_ready_sku(sku, roomlink):
    '''设定sku中status为6（教师ready），传入最新的roomlink'''
    if sku.status == 5 or sku.status == 6:
        sku.status = 6
        sku.save()
        sku.plan.roomlink = roomlink
        sku.plan.save()
        ds_noti_tobuyer_skustart(sku)
    return True

def act_buyer_ready_sku(sku):
    '''设定sku中status为7（学生ready）'''
    if sku.status == 6:
        sku.status = 7
        sku.save()
    return True

def act_edit_provider_profile(provider, name, video, teaching_language):
    '''对Provider的profile其中的属性进行加工'''
    # provider.avatar = avatar
    provider.name = name
    provider.video = video
    provider.teaching_language = teaching_language
    provider.save()
    return True

def act_upload_provider_avatar(provider, new_avatar):
    provider.avatar = new_avatar
    provider.save()
    return True

def act_provider_feedback_sku(questionnaire, comment, sku, buyer):
    '''提交provider对于sku向buyer的feedback'''
    rtp = ReviewToBuyer(sku=sku, questionnaire=questionnaire, comment=comment, buyer=buyer, provider=sku.provider)
    rtp.save()
    sku.status=9
    sku.save()
    return True

def act_buyer_feedback_sku(questionnaire, comment, sku, buyer):
    '''提交buyer对于sku对provider的feedback'''
    provider = sku.provider
    raw_json = json.loads(questionnaire)
    score = (raw_json.get('q1') + raw_json.get('q2') + raw_json.get('q3') + raw_json.get('q4')) * 2.5
    rtb = ReviewToProvider(sku=sku, questionnaire=questionnaire, comment=comment, buyer=buyer, provider=provider, score=score)
    rtb.save()
    sku.status = 9
    sku.save()
    return True

def act_orderpaid(order, buyer):
    '''当order支付后对order相关信息进行增补'''
    for sku in order.skus.all():
        sku.buyer.add(buyer)
        skus_topic = json.loads(order.skus_topic)
        topic_id = (item for item in skus_topic if item["sku_id"] == sku.id).next()['topic_id']
        sku.topic = get_object_or_404(Topic, id=topic_id)
        sku.status = 1
        sku.save()
        ds_noti_toprovider_skubooked(sku)
    order.status = 2
    order.save()
    return True

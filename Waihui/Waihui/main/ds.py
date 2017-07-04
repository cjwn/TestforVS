# -*- coding: utf-8 -*-
from django.utils import translation, timezone, html
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from main.models import User
from main.models import Language
from main.models import Provider
from main.models import Buyer
from main.models import Topic
from main.models import TopicCategory
from main.models import Sku
from main.models import Plan
from main.models import Order
from main.models import Wallet
from main.models import ReplyToSku
from main.models import ReviewToProvider
from main.models import ReviewToBuyer
from main.models import Log
from main.models import Notification
import datetime

def ds_showtopic(id=0, bywhat=0):
    if bywhat == 0:
        topic = Topic.objects.get(id=id)
    elif id == 0:
        topic = Topic.objects.order_by('bywhat')
    elif bywhat == 0 & id == 0:
        topic = "error"
    return topic

def ds_addlog(client, action, user, order=None, character=None):
    '''增加日志记录
    TYPE_OF_CLIENT = (
        (0, '网页端'),
        (1, '移动网页端'),
        (2, 'IOS客户端'),
        (3, '安卓客户端')
    )
    TYPE_OF_ACTION = (
        (0, '登陆'),
        (1, '登出'),
        (2, '下单'),
        (3, '修改'),
        (4, '取消')
    )'''
    log = Log(client=client,
              action=action,
              user=user,
              order=order,
              character=character,
             )
    log.save()
    return log

def ds_getanoti(noti):
    if noti.noti == 0:
        content = u"Your tutor <strong>%s</strong> left a comment:<br/> %s<br>-- from <i>Topic: %s</i>" % (noti.reply.user.provider.name, noti.reply.content, noti.sku.topic.name)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 10:
        content = u"Your student <strong>%s</strong> left a comment:<br/> %s<br>-- from <i>Topic: %s</i>" % (noti.reply.user.buyer.nickname, noti.reply.content, noti.sku.topic.name)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 3:
        content = u"the <strong>%s</strong>'s \" <strong>%s</strong> \" class will begin in 30 mins" % (noti.sku.provider.name, noti.sku.topic.name)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 6:
        content = u"Your teacher <strong>%s</strong> canceled your course:<br/>-- <i>Topic: %s</i>" % (noti.sku.provider.name, noti.sku.topic.name)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 9:
        content = u"Your student %s canceled your course: <br/>-- <i>Topic: %s Time: %s</i>"  % (html.escape(list(noti.sku.buyer.all())), noti.sku.topic, noti.sku.start_time)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 5:
        content = u"Your course's teacher has changed to : <strong>%s</strong><br/>-- <i>Topic: %s</i>" % (noti.sku.provider.name, noti.sku.topic.name)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 8:
        content = u"A student %s booked your course! please confirm and prepare:<br/>-- <i>Topic: %s Time: %s</i>" % (noti.sku.buyer.all().last(), noti.sku.topic.name, noti.sku.start_time)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 2:
        content = u"Your course's plan is ready! please be prepared<br/>-- <i>Topic: %s Time: %s</i>" % (noti.sku.topic.name, noti.sku.start_time)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 7:
        content = u"Your course's plan has been modified! please checkout<br/>-- <i>Topic: %s Time: %s</i>" % (noti.sku.topic.name, noti.sku.start_time)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 12:
        content = _(u"Your teacher is ready! please checkout <br />-- <i>Link: %s ") % (noti.sku.plan.roomlink)
        link = reverse('main:showsku', args=[noti.sku.id])
    anoti = {'id': noti.id,
             'read' : noti.read,
             'content' : content,
             'open_time': noti.open_time,
             'close_time': noti.close_time,
             'link' : link,
            }
    return anoti

def ds_noti_newreply(reply, user, type):
    noti = 0 if type == 1 else 10
    notification = Notification(user=user,
        reply=reply, sku=reply.sku, open_time = timezone.now(), close_time = timezone.now() + datetime.timedelta(weeks=100), noti=noti)
    notification.save()
    return True

# def ds_noti_newcancel(sku, user, type):
#     noti = 6 if type == 1 else 9
#     notification = Notification(user=user,
#         sku=sku, open_time = timezone.now(),
#         close_time = timezone.now() + datetime.timedelta(weeks=100),
#         noti=noti)
#     notification.save()
#     return True

def ds_get_order_cny_price(skus):
    SKU_CNY_PRICE = 90.00
    if isinstance(skus, Sku):
        cny_price = SKU_CNY_PRICE
    else:
        cny_price = len(skus) * SKU_CNY_PRICE
    return cny_price

def ds_noti_tobuyer_noprovider(sku):
    """给学生发一个 noti 说完蛋了课不上了"""
    for buyer in sku.buyer.all():
        notification = Notification(user=buyer.user, sku=sku,
                                    noti=6, open_time=timezone.now(),
                                    close_time=timezone.now() + datetime.timedelta(weeks=100))
        notification.save()
    return True

def ds_noti_toprovider_lostbuyer(sku):
    """给sku的教师发消息，减少了某学生"""
    notification = Notification(user=sku.provider.user, sku=sku, noti=9,
                                open_time=timezone.now(),
                                close_time=sku.end_time)
    notification.save()
    return True

def ds_change_provider(sku, new_provider):
    """变更教师，传入sku及provider"""
    sku.provider = new_provider
    sku.save()
    ds_noti_tobuyer_changeprovider(sku)
    msg = _(u'教师已变更')
    return msg

def ds_noti_tobuyer_changeprovider(sku):
    """给学生发一个 noti 说课换老师了"""
    for buyer in sku.buyer.all():
        notification = Notification(user=buyer.user, sku=sku,
                                    noti=5, open_time=timezone.now(),
                                    close_time=sku.start_time + datetime.timedelta(hours=1))
        notification.save()
    return True

def ds_noti_toprovider_skubooked(sku):
    """跟教师发通知说sku已被预订"""
    notification = Notification(user=sku.provider.user, sku=sku, noti=8, open_time=timezone.now(),
                                close_time=sku.end_time)
    notification.save()
    return True

def ds_sku_status_check(skus, status):
    '''检查sku的状态是否为可约（0 or 10），能否下单'''
    try:
        if iter(skus):
            for sku in skus:
                if sku.status in status:
                    return True
                else:
                    return False
    except:
        if skus.status in status:
            return True
        else:
            return False

def ds_sku_provider_check(skus, buyer):
    '''检查sku的买家和卖家是否为一个'''
    try:
        if iter(skus):
            for sku in skus:
                if sku.provider.user == buyer.user:
                    return False
                else:
                    return True
    except:
        if skus.provider.user == buyer.user:
            return False
        else:
            return True

def ds_noti_tobuyer_newplan(plan):
    '''通知学生，这节课，老师已经备课完成'''
    for buyer in plan.sku.buyer.all():
        notification = Notification(
            user=buyer.user,
            noti=2,
            sku=plan.sku,
            open_time=timezone.now(),
            close_time=plan.sku.end_time,
            )
        notification.save()
    return True

def ds_noti_tobuyer_planmodified(plan):
    '''通知学生，这节课，老师的教案已修改'''
    for buyer in plan.sku.buyer.all():
        notification = Notification(
            user=buyer.user,
            noti=7,
            sku=plan.sku,
            open_time=timezone.now(),
            close_time=plan.sku.end_time,
            )
        notification.save()
    return True

def ds_noti_tobuyer_skustart(sku):
    '''通知学生，有节课程老师已经准备就绪，可以点击上课链接roomlink了'''
    for buyer in sku.buyer.all():
        notification = Notification(
            user=buyer.user,
            noti=12,
            sku=sku,
            open_time=timezone.now(),
            close_time=sku.end_time,
            note="快上课",
            url=sku.plan.roomlink,
            )
        notification.save()
    return True
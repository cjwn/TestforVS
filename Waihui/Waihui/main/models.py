# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
import datetime
# from main.act import act_upgrade_hp
# 无法导入acts
BEFORE_COURSE_TIME = datetime.timedelta(minutes=15)

def upgrade_hp(self,theset):
    """upgrade the hp by input a int """
    self.hp = theset
    self.save()
    return self.hp

def upgrade_status(self,theset):
    """upgrade the hp by input a int """
    self.status = theset
    self.save()
    return self.status

# Create your models here.
# index 1
class Language(models.Model):

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __unicode__(self):
        return u'%s' % self.english_name
    chinese_name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)
    # 需要修改english_name为系统可识别 
    local_name = models.CharField(max_length=50)
    def autoaddlanguage(self, language_name):
        self.english_name = get_language()
        self.save()
        return self.english_name


        

# index 2
class Provider(models.Model):
    """
    There are user(o2o), status(mc), name(mc), weekday_pattern(mcoseint), fee_rate(mfloat), hp(mfloat),hp(mfloat)
    and get_fee_rate(), upgrade_status(int), upgrade_hp(int), set_weekday_pattern()
    in Provider model
    """ 
    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"
        db_tablespace = "ImageStore"

    def __unicode__(self):
        return u'%s' % self.name
    user = models.OneToOneField(User)

    LEVELS_OF_TEACHER_CHOICES = (
        (0, '非教师'),
        (1, '已申请'),
        (2, '实习'),
        (3, '正式'),
        )
    status = models.IntegerField(
        choices=LEVELS_OF_TEACHER_CHOICES,
        default=0,
        )
    name = models.CharField(max_length=50, )
    weekday_pattern = models.CommaSeparatedIntegerField(max_length=200, blank=True, null=True)
    fee_rate = models.FloatField(default=1)
    hp = models.FloatField(default=100)
    teaching_language = models.ManyToManyField(Language, blank=True)
    bio = models.TextField(blank=True)
    video = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="provider_avatars/%Y/%m/%d/", default='/media/none/a.png', blank=True, null=True)
    assigned_location = models.TextField(blank=True, null=True)
    assigned_nationality = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_fee_rate(self):
        """对该老师的fee_rate进行更新（在需要时）"""
        if self.fee_rate == '':
            return "empty value"
        else:
            return '%s' %(self.fee_rate)
        self.save()
        return self.fee_rate
    def upgrade_status(self, theset):
        """对教师状态进行升级"""
        # if form is OK
        return upgrade_status(self, theset)
    def upgrade_hp(self, theset):
        '''upgrade hp of teacher'''
        # user.last_login
        d1 = datetime.datetime.now()
        d2 = self.modified
        if (d1-d2).days >= 1:
            return "in if"
        return upgrade_hp(self, theset)

    def set_weekday_pattern(self, theset):
        pass


# index 3
class Buyer(models.Model):

    class Meta:
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"

    def __unicode__(self):
        return u'%s' % self.nickname
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=50)
    MALE = 0
    FEMALE = 1
    CHOICES_OF_GENDER = (
        (MALE, '男'),
        (FEMALE, '女'),
        )
    gender = models.IntegerField(
        choices=CHOICES_OF_GENDER,
        blank=True, null=True,
        )
    brithday = models.DateField(blank=True, null=True)
    mother_tongue = models.ForeignKey(Language, blank=True, null=True)
    time_zone = models.CharField(max_length=50)
    hp = models.IntegerField(default=100)
    provider = models.ForeignKey(Provider, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    nationality = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def set_provider(self, provider):
        new_provider = provider
        self.provider = new_provider
        return u'%s' %self.provider

# index 4
class TopicCategory(models.Model):

    class Meta:
        verbose_name = "TopicCategory"
        verbose_name_plural = "TopicCategorys"

    def __unicode__(self):
        return u'%s' % self.name
    name = models.CharField(max_length=50, blank=True, null=True)
    background_image = models.URLField()

# index 5
class Topic(models.Model):

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __unicode__(self):
        return u'%s' % self.name
    name = models.CharField(max_length=50)
    desc = models.TextField()
    category = models.ForeignKey(TopicCategory)
    # default_plan = models.ForeignKey(Plan,blank=True,null=True)
    status = models.IntegerField()
    creator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)    

# index 6
class Sku(models.Model):

    class Meta:
        verbose_name = "Sku"
        verbose_name_plural = "Skus"
        # ordering = ['-start_time']

    def __unicode__(self):
        if self.topic is None:
            return u'%s' % str(str(self.id)+". ("+self.start_time.strftime("%c")+") "+"no topic")
        else:
            return u'%s' % str(str(self.id)+". ("+self.start_time.strftime("%c")+") "+str(self.topic))
    provider = models.ForeignKey(Provider, )
    buyer = models.ManyToManyField(Buyer, blank=True)

    STATUS_OF_SKU_CHOICES = (
        (0, _(u'可约')), #定教师没学生,教师生成sku，等待学生预约
        (1, '已约'), #学生完成付费预约，等待教师确认
        (2, '待抢'), #教师取消，等待新教师接单
        (3, '没有教师了'), #来不及换老师了。。。
        (4, '已定'), #教师确认学生的预约
        (5, '已备课'),
        (6, '老师ready'),
        (7, '学生进了教室'),
        (8, '已结束待评价'),
        (9, '已结束 '),
        (10, '学生取消'),
    )
    
    status = models.IntegerField(
        choices=STATUS_OF_SKU_CHOICES,
        default=0,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    topic = models.ForeignKey(Topic, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def duration(self):
        duration = (self.end_time - self.start_time)
        duration = {
        'Total':duration,
        'hours':duration.seconds//3600,
        'minuets':(duration.seconds % 3600) // 60,
        'seconds':duration.seconds % 60,
        }
        return duration
    def has_plan(self):
        try:
            plan = self.plan
            has_plan = True
        except Plan.DoesNotExist:
            has_plan = False
        return has_plan
    def time_to_start(self):
        return self.start_time - timezone.now()
    def further(self):
        if self.start_time > timezone.now():
            return self
        
# index 7
class Plan(models.Model):

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __unicode__(self):
        return u'Plan of %s' % self.sku
    sku = models.OneToOneField(Sku ,blank=True, null=True)
    topic = models.ForeignKey(Topic, )
# 给sku：
# 已备课；已上完；
# 给topic：
# 待审核；成功通过；失败待修改
    status = models.IntegerField()
    content = models.TextField()
    assignment = models.TextField(blank=True,null=True)
    slides = models.TextField(blank=True,null=True)
    materiallinks = models.TextField(blank=True,null=True)
    materialhtml = models.TextField(blank=True,null=True)
    voc = models.TextField(blank=True,null=True)
    copy_from = models.ForeignKey('self',blank=True,null=True)
    # summary 写sum我怕出问题
    sumy = models.TextField(blank=True,null=True)
    roomlink = models.URLField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 8
class Wallet(models.Model):

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __unicode__(self):
        return u'%s' % self.cny_balance
    user = models.OneToOneField(User)
    cny_balance = models.FloatField(default=0)
    display_currency = models.CharField(default="CNY", max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def upgragde_balance(self, theset, order):
        if order == 0:
            self.cny_balance = theset
        elif order.status == 1:
            amount = order.cny_price
            self.cny_balance -= amount
        self.save()
        return self.cny_balance



# index 9
class ReviewToProvider(models.Model):

    class Meta:
        verbose_name = "ReviewToProvider"
        verbose_name_plural = "ReviewToProviders"

    def __unicode__(self):
        return u'%s' % 'SkuID:[' + str(self.sku.id) + ']' + ' Score:[' + str(self.score) + '] ' +str(self.buyer.nickname) + ' reviews to ' + str(self.provider.name)
    provider = models.ForeignKey(Provider)
    buyer = models.ForeignKey(Buyer)
    sku = models.OneToOneField(Sku)
    questionnaire = models.CharField(max_length=50)
    comment = models.CharField(max_length=250, blank=True, null=True)
    score = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 10
class ReviewToBuyer(models.Model):

    class Meta:
        verbose_name = "ReviewToBuyer"
        verbose_name_plural = "ReviewToBuyers"

    def __unicode__(self):
        return u'%s' % 'SkuID:[' + str(self.sku.id) + ']' + str(self.provider.name) + ' reviews to ' + str(self.buyer.nickname)
    provider = models.ForeignKey(Provider)
    buyer = models.ForeignKey(Buyer)
    sku = models.ForeignKey(Sku)
    questionnaire = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 11
class ReplyToSku(models.Model):

    class Meta:
        verbose_name = "ReplyToSku"
        verbose_name_plural = "ReplyToSkus"

    def __unicode__(self):
        return u'%s' % self.content
    sku = models.ForeignKey(Sku)
    user = models.ForeignKey(User)
    type = models.IntegerField()
    content = models.TextField()
    reply_to = models.ForeignKey('self', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 12
class OrderType(models.Model):

    class Meta:
        verbose_name = "OrderType"
        verbose_name_plural = "OrderTypes"

    def __unicode__(self):
        return u'%s' % self.type
    type = models.CharField( max_length=50)

# index 13
class Order(models.Model):

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __unicode__(self):
        return u'%s' % '['+str(self.id)+'] '+"Order of "+ str(self.buyer) + " contains "+ str(len(self.skus.all())) + " skus, cost " + str(self.cny_price) + " Yuan"

    buyer = models.ForeignKey(Buyer)
    provider = models.ForeignKey(Provider, null=True)
    cny_price = models.FloatField()
    cny_paid = models.FloatField(default=0)
    pay_method = models.CharField(blank=True, null=True, max_length=50)
    skus = models.ManyToManyField(Sku, blank=True)
    skus_topic = models.CharField(blank=True, null=True, max_length=300)
    type = models.ForeignKey(OrderType)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    paidtime = models.DateTimeField(null=True, blank=True) #付款日期
    paidbacktime = models.DateTimeField(null=True, blank=True) #退款日期
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

# 不可支付、未支付、已支付、已完成、申请退款、已退款……

    STATUS_OF_ORDER_TYPE = (
        (0, '不可支付'),
        (1, '未支付'),
        (2, '已支付'),
        (3, '已完成'),
        (4, '申请退款'),
        (5, '已退款'),
        (6, '已取消'),#页面显示为cancel
    )

    status = models.IntegerField(
        choices=STATUS_OF_ORDER_TYPE,
        default=1)

    def upgrade_status(self, theset):
        """对order状态进行升级"""
        self.status = theset
        self.save()

    def time_to_pay_24hours(self):
        '''剩余余款时间 时限设置为24小时'''
        return self.created - timezone.now() + datetime.timedelta(hours=24)

    def time_to_pay(self, timedelta):
        '''剩余余款时间 时限设置为24小时'''
        return self.created - timezone.now() + datetime.timedelta(timedelta)

class Log(models.Model):
    '''Model Log is for record of the journal of a User daily action.
    To record this info, you should insert log attribution in Front'''
    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __unicode__(self):
        return u'%s' % '['+str(self.user.username)+'] '+ self.get_action_display() + ' on ' + self.get_client_display() + ' as ' + str(self.get_character_display())


    TYPE_OF_CLIENT = (
        (0, '网页端'),
        (1, '移动网页端'),
        (2, 'IOS客户端'),
        (3, '安卓客户端')
    )
    client = models.IntegerField(
        choices=TYPE_OF_CLIENT,
        default=0)

    TYPE_OF_ACTION = (
        (0, '登陆'),
        (1, '登出'),
        (2, '下单'),
        (3, '修改'),
        (4, '取消')
    )
    action = models.IntegerField(choices=TYPE_OF_ACTION)
    user = models.ForeignKey(User)
    order = models.ForeignKey(Order, null=True, blank=True)
    TYPE_OF_CHARACTER = (
        (0, 'buyer'),
        (1, 'provider'))
    character = models.IntegerField(choices=TYPE_OF_CHARACTER, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __unicode__(self):
        return u'%s' % "[" +str(self.id) + "] " +str(self.noti) + " " + str(self.user)

    STATUS_OF_NOTI = (
        (0, '老师发表了回复'),
        (1, '老师确认了你的课，已经开始备课'),
        (2, '老师已经备课完成！'),
        (3, '还有半个小时'),
        (4, '开始上课！(5分钟)'),
        (5, '换了老师'),
        (6, '抱歉，由于老师的时间安排，课程取消。退款到账户余额'),
        (7, '教案被修改'),
        (8, '学生预订你的课啦！该备课了请确认'),
        (9, '学生取消了课'),
        (10, '学生发表了回复'),
        (11, '超级通知'),
        (12, '老师准备就绪，请注意查收上课链接')
    )

    user = models.ForeignKey(User)
    noti = models.IntegerField(choices=STATUS_OF_NOTI)
    sku = models.ForeignKey(Sku, blank=True, null=True,)
    reply = models.ForeignKey(ReplyToSku, blank=True, null=True,)
    note = models.CharField(blank=True, null=True, max_length=200)
    url = models.URLField(blank=True, null=True,)
    open_time = models.DateTimeField(blank=True, null=True,)
    close_time = models.DateTimeField(blank=True, null=True,)

    STATUS_OF_READ = (
        (0, 'unread'),
        (1, 'read'))
    read = models.IntegerField(choices=STATUS_OF_READ, default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    

#upload path methods:

def provider_avatar_path(instance, filename):
    # TODO 暂未启用
    # file will be uploaded to MEDIA_ROOT/provider_avatars/user_<id>/
    return 'provider_avatars/user_{0}/{1}'.format(instance.user.id, filename)

# TODO 有空时咱们一起进行：
# 默认值、是否必填等有些还需要再调整
# max_length长度有些字段可能不够
# 添加日期、修改日期回头统一给每一个 model 加
# 最后再根据文档过一遍，看看还有哪里有遗漏

# TODO 添加方法（coolgene 将写出文档）    

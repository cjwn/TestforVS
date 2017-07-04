# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField

# Create your models here.
class Entry(models.Model):
    """会议记录条目"""
    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"

    def __unicode__(self):
        return u'%s' %self.title

    title = models.CharField(u'会议标题', max_length=100)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    content_A = UEditorField(u'议程', blank=True,
                             imagePath="minutes/images/",
                             filePath="minutes/files/",
                             toolbars="normal",
                             )
    content_B = UEditorField(u'纪要', blank=True,
                             imagePath="minutes/images/",
                             filePath="minutes/files/",
                             toolbars="normal",
                             )
    content_C = UEditorField(u'下一步工作安排', blank=True,
                             imagePath="minutes/images/",
                             filePath="minutes/files/",
                             toolbars="normal",
                             )
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name="会议纪要创建人", related_name='created_entries')
    attendees_user = models.ManyToManyField(User, verbose_name="参会人", related_name='attended_entries')
    created = models.DateTimeField(u'创建时间', auto_now_add=True)
    modified = models.DateTimeField(u'最后修改时间', auto_now=True)
    modified_save = models.DateTimeField(u'最后手动保存时间', blank=True, null=True)
    content_A_save = models.TextField(u'议程（手动保存）', blank=True)
    content_B_save = models.TextField(u'纪要（手动保存）', blank=True)
    content_C_save = models.TextField(u'下一步工作安排（手动保存）', blank=True)


class Profile(models.Model):
    """用户基本信息"""
    display_name = models.CharField(u'姓名', max_length=50, blank=True, null=True)
    department = models.CharField(u'部门', max_length=100, blank=True, null=True)
    phonenumber = models.CharField(u'手机', max_length=50, blank=True, null=True)
    wx_id = models.CharField(u'微信', max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True)
    entries = models.ManyToManyField(Entry, verbose_name=_(u"出席的会议"), related_name='attendees')
    def __unicode__(self):
        return u'%s' % self.display_name

        # , verbose_name ="出席的会议", related_name="attendee"
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django import forms

class AttendForm(forms.Form):
    # TODO: Define form fields here
    display_name = forms.CharField(
        label=_(u'姓名'),
        max_length=30,
        )
    department = forms.CharField(
        label=_(u'部门'),
        max_length=30,
        )
    phonenumber = forms.CharField(
        label=_(u'电话'),
        max_length=30,
        )

# -*- coding: utf-8 -*-
from django import forms
from main.models import Provider
from main.models import Topic 
from main.models import Sku
from main.models import ReplyToSku
from main.models import Plan
from main.models import Order
from main.models import Language

class SignupForm(forms.Form):
    nickname = forms.CharField(
      # label=_('姓名'),
      max_length=30,
    )

    email = forms.EmailField(label='Email',)

    password = forms.CharField(
        # label=_('password'),
        widget=forms.PasswordInput(),
        )

    password_2 = forms.CharField(
        # label=_('passowrd_confirmed'),
        widget=forms.PasswordInput(),
    )

    def clean_password_2(self):
        password = self.cleaned_data.get("password")
        password_2 = self.cleaned_data.get("password_2")
        if password and password_2 and password != password_2:
            raise forms.ValidationError('password confirm failed')
        return password_2

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

class AddSkuForm(forms.Form):
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), required=False)

class AddRTSForm(forms.Form):
    # sku = forms.ModelChoiceField(queryset=Sku.objects.all())
    content = forms.CharField(widget=forms.Textarea())
    # reply_to = forms.ModelChoiceField(queryset=ReplyToSku.objects.all(), required=False)
    reply_to = forms.ModelChoiceField(queryset=None, required=False)

class AddPlanForm(forms.Form):
    # sku = forms.ModelChoiceField(queryset=Sku.objects.all())
    # topic = forms.ModelChoiceField(queryset=Topic.objects.all())
    status = forms.IntegerField()
    content = forms.CharField(widget=forms.Textarea())
    assignment = forms.CharField(widget=forms.Textarea(), required=False)
    slides = forms.CharField(widget=forms.Textarea(), required=False)
    roomlink = forms.URLField(required=False)
    materiallinks = forms.CharField(widget=forms.Textarea(), required=False)
    materialhtml = forms.CharField(widget=forms.Textarea(), required=False)
    voc = forms.CharField(widget=forms.Textarea(), required=False)
    copy_from = forms.ModelChoiceField(queryset=Plan.objects.all(), required=False)
    sumy = forms.CharField(widget=forms.Textarea(), required=False)

class ScheduleForm(forms.Form):
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, empty_label=None, widget=forms.Select(attrs={'disabled':'disabled'}))
    schedule = forms.CharField(widget=forms.Textarea(), required=True)
    

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('skus',)
    
class HoldSkuForm(forms.ModelForm):
    class Meta:
        model = Sku
        fields = ('status',)

class BookSkuForm(forms.Form):
    sku = forms.ModelChoiceField(queryset=None, required=False)
    provider = forms.ModelChoiceField(queryset=None, required=False)
    buyer = forms.ModelChoiceField(queryset=None, required=False)
    topic = forms.ModelChoiceField(queryset=None, required=False)

class PlaceSkuForm(forms.Form):
    '''用于由sku（course）直接下单（order）的web页面使用'''
    sku = forms.ModelChoiceField(queryset=None, required=False)
    provider = forms.ModelChoiceField(queryset=None, required=False)
    buyer = forms.ModelChoiceField(queryset=None, required=False)
    topic = forms.ModelChoiceField(queryset=None, required=False)

    # sku = forms.ChoiceField(queryset=None)
    # provider = forms.ModelChoiceField(queryset=None)
    # buyer = forms.ModelChoiceField(queryset=None)
    # topic = forms.ModelChoiceField(queryset=None)


class CancelSkuForm(forms.Form):
    sku = forms.ModelChoiceField(queryset=None, required=False)
    provider = forms.ModelChoiceField(queryset=None, required=False)
    buyer = forms.ModelChoiceField(queryset=None, required=False)

class RoomlinkForm(forms.Form):
    roomlink = forms.URLField(required=True)

# class ImageUploadForm(forms.Form):
#     """image upload form"""
#     image = forms.ImageField()

class ProviderProfileForm(forms.Form):
    """edit provider profile form"""
    # avatar = forms.ImageField()
    name = forms.CharField()
    video = forms.URLField()
    teaching_language = forms.ModelMultipleChoiceField(queryset=Language.objects.all())

class ProviderAvatarForm(forms.Form):
    """Form for providers to upload their avatars"""
    avatar = forms.ImageField()

class ProviderFeedbackSkuForm(forms.Form):
    """Form for providers to feedback on a course"""
    questionnaire = forms.CharField(max_length=200)
    comment = forms.CharField(max_length=200)
    buyer = forms.ModelChoiceField(queryset=None, empty_label=None)

class BuyerFeedbackSkuForm(forms.Form):
    """Form for buyers to feedback on a course"""
    questionnaire = forms.CharField(max_length=200)
    comment = forms.CharField(max_length=200)

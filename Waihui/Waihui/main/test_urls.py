from django.conf.urls import patterns, include, url
from main import test_views

urlparttens = patterns('',
    url(r'^test/$', test_views.my_view, name='get_language'),
    url(r'^test/(\d{1,2})/$', test_views.url_test_set, name='test_setnum'),
    )
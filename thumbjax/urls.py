# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

testpatterns = patterns('thumbjax.views.tests',
    url(r'^$', 'index', name='index'),
    url(r'^control/$', 'control_group', name='control'),
    url(r'^std/$', 'std_thumbnailer', name='std'),
    url(r'^jaxd/$', 'thumbjaxd', name='jaxd'),
)

urlpatterns = patterns('',
    url(r'^tests/', include(testpatterns, namespace='tests'))
)

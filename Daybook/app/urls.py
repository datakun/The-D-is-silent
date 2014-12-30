from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
    url(r'^$', views.get_daybook),
    # url(r'^erase/(?P<date>[0-9]+)/$', views.erase_daybook, name='erase_daybook'),
    url(r'^erase/$', views.erase_daybook),
    url(r'^write/$', views.write_daybook),
    # url(r'^(?P<date>\d+)/$', views.get_daybook, name='get_daybook'),
)
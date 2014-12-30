from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^daybook/', include('app.urls')),
    url(r'^login/$', views.signin),
    url(r'^logout/$', views.signout,),
    url(r'^register/$', views.signup),
    url(r'^admin/', include(admin.site.urls)),
)

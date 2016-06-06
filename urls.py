#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.views.static import serve
from tastypie.api import Api
from food.api.resources import EventResource, UserResource
from food.api.resources import UserProfileResource
import food.views


admin.autodiscover()

event_resource = EventResource()
user_resource = UserResource()
userprofile_resource = UserProfileResource()

urlpatterns = patterns('',
    url(r'^$', food.views.login_user),
    url(r'^insertview/$', food.views.insertview, name='insert'),
	url(r'^register/$', food.views.registerNewUser, name='register'),
	url(r'^createEvent/$', food.views.createEvent, name='createEvent'),
    url(r'^reviewEvent/(?P<event_id>[\d]+)$', food.views.reviewEvent, name='reviewEvent'),
    url(r'^viewEvent/(?P<event_id>[\d]+)$', food.views.viewEvent, name='viewEvent'),
    url(r'^reviewUser/(?P<user_id>[\d]+)$', food.views.reviewUser, name='reviewUser'),
    url(r'^viewUserProfile/(?P<user_id>[\d]+)$', food.views.viewUserProfile, name='viewUserProfile'),
    url(r'^searchEvents/$', food.views.searchEvents, name='searchEvents'),
    url(r'^participateInEvents/(?P<event_id>[\d]+)$', food.views.participateInEvents, name='participateInEvents'),
	url(r'^approveRequest/(?P<notification_id>[\d]+)$', food.views.approveRequest, name='approveRequest'),
	url(r'^deleteEvent/(?P<event_id>[\d]+)$', food.views.deleteEvent, name='deleteEvent'),
	url(r'^deleteNotification/(?P<notification_id>[\d]+)$', food.views.deleteNotification, name='deleteNotification'),
    url(r'^success/$', food.views.success, name='success'),
	(r'^site_media/(?P<path>.*)$', serve,
        {'document_root': settings.BASE_DIR+'/staticfiles/'}),
	url(r'^login/$', food.views.login_user, name='login'),
	url(r'^ajaxMapRefresh/$', food.views.ajaxMapRefresh, name='ajaxMapRefresh'),
	url(r'^logout/$', food.views.logout_user, name='logout'),
	url(r'^accounts/login/$', views.login),
	url(r'^viewNotifications/$', food.views.viewNotifications, name='viewNotifications'),
	url(r'^viewMessages/$', food.views.viewMessages, name='viewMessages'),
	url(r'^api/', include(event_resource.urls)),
    url(r'^api/', include(user_resource.urls)),
	url(r'^api/', include(userprofile_resource.urls)),
)

from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'food.views.indexview', name='index'),
	(r'indexview', 'food.views.indexview'),
	(r'myFirstview', 'food.views.myFirstview'),
    url(r'^insertview/$', 'food.views.insertview', name='insertview'),
	url(r'^register/$', 'food.views.registerNewUser', name='register'),
	url(r'^createEvent/$', 'food.views.createEvent', name='createEvent'),
    url(r'^success/$', 'food.views.success', name='success'),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/remote/users/cmarques/dev/fooding/staticfiles/'}),
	(r'^login/$', 'food.views.login_user'),
	(r'^logout/$', 'food.views.logout_user'),
	(r'^accounts/login/$', 'django.contrib.auth.views.login'),
) 
from django.conf.urls.defaults import *
#from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fooding.views.home', name='home'),
	#url(r'^fooding/', 'food.views.indexview', name='indexview'),
	#url(r'^fooding/', include('blog.urls')),
	(r'indexview', 'food.views.indexview'),
	(r'myFirstview', 'food.views.myFirstview'),
    (r'insertview', 'food.views.insertview'),

    #url(r'^admin/', include(admin.site.urls)),
)

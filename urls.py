from django.conf.urls.defaults import *
from django.contrib import admin
#from django.conf.urls.static import static
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from food import settings


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fooding.views.home', name='home'),
	#url(r'^fooding/', 'food.views.indexview', name='indexview'),
	#url(r'^fooding/', include('blog.urls')),
	(r'indexview', 'food.views.indexview'),
	(r'myFirstview', 'food.views.myFirstview'),
    (r'insertview', 'food.views.insertview'),
	url(r'^register/$', 'food.views.registerNewUser', name='register'),
    url(r'^success/$', 'food.views.success', name='success'),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/remote/users/cmarques/dev/fooding/staticfiles/'}),

    #url(r'^admin/', include(admin.site.urls)),
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += staticfiles_urlpatterns()
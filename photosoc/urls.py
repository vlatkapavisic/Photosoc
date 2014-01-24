from django.conf.urls.defaults import *
from photosoc_app.views import *
from django.views.generic import TemplateView
import os

site_media=os.path.join(os.path.dirname(__file__), 'site_media')

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', main_page),
	(r'^users/$', users_page),
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', logout_page),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': site_media}),
    (r'^register/$', register_page),
    (r'^register/success/$', TemplateView.as_view(template_name='registration/register_success.html')),
    (r'^users/(?P<uname>\w+)/$', user_page),
    (r'^photos/$', photos_page),
    (r'^photos/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/debellatrix/Desktop/photosoc'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^upload/$', upload_photo),
    (r'^friends/$', friends_page),
    (r'^friend/add/$', friend_add),
    (r'^like/$', like_photo_page),
    (r'^unlike/$', unlike_photo_page),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^photo/(?P<photo_id>\d+)/comments/$', photo_comments_page),
    (r'^photo/(?P<photo_id>\d+)/tag/$', tag_photo_page),
    # Examples:
    # url(r'^$', 'photosoc.views.home', name='home'),
    # url(r'^photosoc/', include('photosoc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)



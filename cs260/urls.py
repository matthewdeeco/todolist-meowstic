from django.conf.urls import patterns, include, url
#from django.conf.urls.defaults import *
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'todo.views.home_page', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

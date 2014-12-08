from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'todo.views.index_page', name='index'),
    url(r'^login/', 'todo.views.login_page', name='login'),
    url(r'^logout', 'todo.views.logout_page', name='logout'),
    url(r'^home/new_item$', 'todo.views.new_item', name='new_item'),
    url(r'^home/toggle_complete_item$', 'todo.views.toggle_complete_item', name='toggle_complete_item'),
    url(r'^home/', 'todo.views.home_page', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'todo.views.index_page', name='index'),
    url(r'^signup/$', 'todo.views.signup_page', name='signup'),
    url(r'^login/$', 'todo.views.login_page', name='login'),
    url(r'^logout$', 'todo.views.logout_page', name='logout'),
    url(r'^home/$', 'todo.views.home_page', name='home'),
    url(r'^home/daily_view/$', 'todo.views.daily_view', name='daily_view'),
    url(r'^home/weekly_view/$', 'todo.views.weekly_view', name='weekly_view'),
    url(r'^home/monthly_view/$', 'todo.views.monthly_view', name='monthly_view'),
    url(r'^home/new_item$', 'todo.views.new_item', name='new_item'),
    url(r'^home/toggle_complete_item$', 'todo.views.toggle_complete_item', name='toggle_complete_item'),
    url(r'^home/reschedule_item$', 'todo.views.reschedule_item', name='reschedule_item'),
    url(r'^home/cancel_item/(\d+)$', 'todo.views.cancel_item', name='cancel_item'),
    url(r'^home/delete_item/(\d+)$', 'todo.views.delete_item', name='delete_item'),
    url(r'^admin/', include(admin.site.urls)),
)

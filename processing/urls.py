from django.urls import re_path

from processing import views

urlpatterns = [
    re_path(r'^$', views.index, name='index_redirect'),
    re_path(r'^home/$', views.index, name='index'),
    re_path(r'^submit/$', views.submit, name='submit'),
    re_path(r'^home/(?P<page_num>\d+)/$', views.index, name='index_num'),
    re_path(r'^post/(?P<post_id>\d+)/$', views.post, name='post'),
    re_path(r'^delete/(?P<post_id>\d+)/$', views.delete, name='delete'),
    re_path(r'^undelete/(?P<post_id>\d+)/$', views.undelete, name='undelete'),
    re_path(r'^update/(?P<post_id>\d+)/$', views.update, name='update'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout, name='logout'),
]

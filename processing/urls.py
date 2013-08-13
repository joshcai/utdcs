from django.conf.urls import patterns, url

from processing import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index_redirect'),
	url(r'^home/$', views.index, name='index'),
	url(r'^submit/$', views.submit, name='submit'),
	url(r'^home/(?P<page_num>\d+)/$', views.index, name='index_num'),
	url(r'^post/(?P<post_id>\d+)/$', views.post, name='post'),
	)

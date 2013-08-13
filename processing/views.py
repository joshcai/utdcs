# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from website import secrets
import datetime

from processing.models import Post

#debugging
#import pdb
def render_post(current_post):
	newpost = """var sketchProc=function(processingInstance){ with (processingInstance){
		var xWidth=400;
		var yHeight=400;
		frameRate(45);
		size(xWidth, yHeight);"""
	newpost += current_post
	newpost +="}};"
	return newpost

def index(request, page_num=1):
	post_entries = Post.objects.order_by('-date').exclude(deleted=True)
	context ={ 
		'post_entries': post_entries[(float(page_num)-1)*5:float(page_num)*5],
		'page_num': page_num,
		'request': request,
		}
	if float(page_num) > 1:
		context['prev'] = True
	if float(page_num)*5 < len(post_entries): # this can be optimized later - (code is already hitting database once)
		context['next'] = True 

	return render(request, 'processing/index.html', context)

def submit(request):
	if request.method == 'POST':
		if request.POST['title'] and request.POST['content']:
			d = datetime.datetime.now()
			if request.POST['author']:
				auth = request.POST['author'] 
			else:
				auth = "Anonymous"
			p = Post(title=request.POST['title'], 
				content=request.POST['content'],
				content_rendered=render_post(request.POST['content']),
				author=auth,
				date=d, 
				date_str=d.strftime('%B %d, %Y %I:%M%p'))
			p.save()
			return HttpResponseRedirect(reverse('processing:index'))
		else:
			context={
				'title': request.POST['title'],
				'content': request.POST['content'],
				'error_message': "Title and content required<br />",
				'url': reverse('processing:submit'),
				'request': request,
			}
			return render(request, 'processing/newpost.html', context)
	return render(request, 'processing/newpost.html', {'url': reverse('processing:submit'), 'request': request})

def login(request):
	context={'request': request}
	if request.method == 'POST':
		if request.POST['password'] == secrets.login_password:
			request.session['logged_in'] = True
			return HttpResponseRedirect(reverse('blog:index'))
		else:
			context['error_message'] = "Invalid password<br />"
	return render(request, 'blog/login.html', context) 

def delete(request, post_id):
	if 'logged_in' in request.session and request.session['logged_in']:
		post = get_object_or_404(Post, pk=post_id)
		post.deleted = True
		post.save()
		return HttpResponseRedirect(reverse('blog:index'))

def post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	context={
		'post': post,
		'request': request,
	}
	query = Post.objects.all().exclude(deleted=True)
	next = query.filter(pk__gt=post_id)
	if next:
		context['next'] = next[0]
	prev = query.filter(pk__lt=post_id).order_by('id').reverse()
	if prev:
		context['prev'] = prev[0]
	return render(request,'processing/post.html', context)

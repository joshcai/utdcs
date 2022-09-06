# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

import datetime
from dateutil import parser
import re

from processing.models import Post

#debugging
#import pdb


def render_post(current_post):
    newpost = """var sketchProc=function(processingInstance){ with (processingInstance){
		var xWidth=400;
		var yHeight=400;
		frameRate(45);
		size(xWidth, yHeight);"""
    newpost += re.sub(r'rotate *\((?P<num>.*)\) *;',
                      r'rotate(radians(\g<num>));', current_post)
    # newpost += current_post

    newpost += "}};"
    return newpost


def index(request, page_num=1):
    post_entries = Post.objects.order_by('-date').exclude(deleted=True)
    if 'logged_in' in request.session and request.session['logged_in']:
        if 'unfiltered' in request.GET:
            post_entries = Post.objects.order_by('-date')
        if 'deleted' in request.GET:
            post_entries = Post.objects.order_by('-date').exclude(
                deleted=False)
    if 'author' in request.GET:
        post_entries = post_entries.filter(
            author__iexact=request.GET['author'])
    context = {
        'post_entries':
        post_entries[(float(page_num) - 1) * 5:float(page_num) * 5],
        'page_num': page_num,
        'request': request,
    }
    if 'author' in request.GET:
        context['author'] = request.GET['author']
    if float(page_num) > 1:
        context['prev'] = True
    if float(page_num) * 5 < len(
            post_entries
    ):  # this can be optimized later - (code is already hitting database once)
        context['next'] = True

    return render(request, 'processing/index.html', context)


def submit(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['content']:
            if request.POST.get('time', ''):
              d = parser.parse(request.POST['time'])
            else:
              d = datetime.datetime.now()
            if request.POST['author']:
                auth = request.POST['author']
            else:
                auth = "Anonymous"
            if request.POST.getlist('linked'):  #fix ?
                lin = request.POST['link']
                linke = True
            else:
                linke = False
                lin = ''
            p = Post(title=request.POST['title'],
                     content=request.POST['content'],
                     content_rendered=render_post(request.POST['content']),
                     author=auth,
                     date=d,
                     link=lin,
                     linked=linke,
                     date_str=d.strftime('%B %d, %Y %I:%M%p'))
            p.save()
            request.session[p.id] = True
            return HttpResponseRedirect(reverse('processing:index'))
        else:
            context = {
                'title': request.POST['title'],
                'content': request.POST['content'],
                'author': request.POST['author'],
                'linked': request.POST['linked'],
                'link': request.POST['link'],
                'error_message': "Title and content required<br />",
                'url': reverse('processing:submit'),
                'request': request,
            }
            return render(request, 'processing/newpost.html', context)
    return render(request, 'processing/newpost.html', {
        'url': reverse('processing:submit'),
        'request': request
    })


def login(request):
    context = {'request': request}
    if request.method == 'POST':
        if request.POST['password'] == 'passwordnotneeded':
            request.session['logged_in'] = True
            return HttpResponseRedirect(reverse('processing:index'))
        else:
            context['error_message'] = "Invalid password<br />"
    return render(request, 'processing/login.html', context)


def logout(request):
    request.session['logged_in'] = False
    return HttpResponseRedirect(reverse('processing:index'))


def update(request, post_id):
    if float(post_id) in request.session or ('logged_in' in request.session
                                             and request.session['logged_in']):
        post = get_object_or_404(Post, pk=post_id)
        context = {
            'title': post.title,
            'author': post.author,
            'content': post.content,
            'link': post.link,
            'linked': post.linked,
            'url': reverse('processing:update', kwargs={'post_id': post_id}),
            'request': request,
        }
        if request.method == 'POST':
            if request.POST['title'] and request.POST['content']:
                post.title = request.POST['title']
                if request.POST['author']:
                    post.author = request.POST['author']
                else:
                    post.author = 'Anonymous'
                post.content = request.POST['content']
                post.content_rendered = render_post(request.POST['content'])
                if request.POST.getlist('linked'):  #fix ?
                    post.link = request.POST['link']
                    post.linked = True
                else:
                    post.linked = False
                post.save()
                print(post.id)
                return HttpResponseRedirect(
                    reverse('processing:post', kwargs={'post_id': post_id}))
            else:
                context['title'] = request.POST['title']
                context['author'] = request.POST['author']
                context['content'] = request.POST['content']
                context['link'] = request.POST['link']
                context['linked'] = request.POST['linked']
                context['error_message'] = "Please fill in all fields<br />"
        return render(request, 'processing/update.html', context)
    else:
        return HttpResponseRedirect(reverse('processing:index'))


def delete(request, post_id):
    if float(post_id) in request.session or ('logged_in' in request.session
                                             and request.session['logged_in']):
        post = get_object_or_404(Post, pk=post_id)
        post.deleted = True
        post.save()
    return HttpResponseRedirect(reverse('processing:index'))


def undelete(request, post_id):
    if float(post_id) in request.session or ('logged_in' in request.session
                                             and request.session['logged_in']):
        post = get_object_or_404(Post, pk=post_id)
        post.deleted = False
        post.save()
    return HttpResponseRedirect(reverse('processing:index'))


def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.deleted:
        return HttpResponseRedirect(reverse('processing:index'))
    context = {
        'post': post,
        'request': request,
    }
    if 'rendered' in request.GET:
        context['rendered'] = True
    query = Post.objects.all().exclude(deleted=True)
    next = query.filter(pk__gt=post_id).order_by('id')
    if next:
        context['next'] = next[0]
    prev = query.filter(pk__lt=post_id).order_by('id').reverse()
    if prev:
        context['prev'] = prev[0]
    return render(request, 'processing/post.html', context)

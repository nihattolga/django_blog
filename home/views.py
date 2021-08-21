from datetime import datetime, timedelta
from math import log
import json
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .utils import best, hot
from posts.models import Article, Category, Comment
from posts.forms import CommentForm
from accounts.models import User
from django.contrib import messages

def search(request):
    if request.GET.get('q',''):
        queryset = Article.objects.filter(title__icontains=request.GET.get('q',''))\
        .annotate(ncomment=Count('comment'),
        ncategory=Count('category'), nupvote=Count('upvote'),
        ndownvote=Count('downvote')).order_by('-created_at').distinct()
        
    else:
        queryset = []

    categories = Category.objects.all().annotate(ncategory=Count('article'))\
    .order_by('-ncategory')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': queryset,
        'categories': categories
    }
    return render(request, 'home/search_view.html', context)

def index(request):
    #autocomplete
    if 'term' in request.GET:
        queryset = Article.objects.filter(title__icontains=request.GET\
            .get('term')).distinct()
        results = [q.title for q in queryset]
        return JsonResponse(results, safe=False)

    articles = Article.objects.all().annotate(ncomment=Count('comment'))
    categories = Category.objects.all().annotate(ncategory=Count('article'))\
    .order_by('-ncategory')

    if articles:

        hot_articles_anno = [hot(timezone.now(), i.created_at, 
                i.upvote.count(), i.downvote.count()) for i in articles]
        a = Article.objects.all().values_list('pk', flat=True)
        pk_list_hot = list(list(zip(*sorted(zip(hot_articles_anno,a))))[1])
        pk_list_hot.reverse()
        objects_hot = Article.objects.filter(pk__in=pk_list_hot)

        objects_hot = dict([(obj.pk, obj) for obj in objects_hot])
        articles_hot = [objects_hot[id] for id in pk_list_hot]

        best_articles_anno = [best(i.upvote.count(), i.downvote.count(), 
                (((timezone.now() - i.created_at).total_seconds())/60)) for i in articles]
        pk_list_best = list(list(zip(*sorted(zip(best_articles_anno,a))))[1])
        pk_list_best.reverse()
        objects_best = Article.objects.filter(pk__in=pk_list_best)

        objects_best = dict([(obj.pk, obj) for obj in objects_best])
        articles_best = [objects_best[id] for id in pk_list_best]

    else:
        articles_hot, articles_best=list(), list()

    articles_new = Article.objects.order_by('-created_at')

    articles_most_liked = Article.objects.order_by('upvote')

    articles_most_viewed = Article.objects.order_by('view')

    page_number = request.GET.get('page')
    def pagination(queryset, page_number):
        paginator = Paginator(queryset, 10)
        page_obj = paginator.get_page(page_number)
        return page_obj

    context = {
        'articles': articles,
        'articles_new': pagination(articles_new, page_number),
        'articles_best': pagination(articles_best, page_number),
        'articles_hot': pagination(articles_hot, page_number),
        'articles_most_liked': pagination(articles_most_liked, page_number),
        'articles_most_viewed': pagination(articles_most_viewed, page_number),
        'categories': categories,
    }

    return render(request, 'home/index.html', context)

def categories_view(request):
    if 'term' in request.GET:
        queryset = Category.objects.filter(category__icontains=request.GET\
            .get('term')).distinct()
        results = [q.category for q in queryset]
        return JsonResponse(results, safe=False)

    categories = Category.objects.all().annotate(ncategory=Count('article'))\
    .order_by('ncategory')
    if request.GET.get('cat') != '' and request.GET.get('cat') is not None:
        categories=Category.objects.filter(category__icontains=request.GET.get('cat'))\
        .annotate(ncategory=Count('article'))\
        .order_by('ncategory')

    paginator = Paginator(categories, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/category_view.html', {'categories': page_obj})

def articles_by_cat(request, id, category):
    posts = Article.objects.filter(category=id)\
    .annotate(ncomment=Count('comment'))
    categories = Category.objects.all().annotate(ncategory=Count('article'))\
    .order_by('ncategory')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
        'posts': posts,
        'categories': categories
    }
    return render(request, 'home/posts-by-cat.html', context)

def detail_view(request, id ,slug):
    article = Article.objects.filter(article_id=id).annotate(ncomment=Count('comment')).get()
    comments = Comment.objects.filter(article=article).order_by('-created_at')
    article.view += 1
    article.save()
    categories = Category.objects.all().annotate(ncategory=Count('article'))
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.article = article
            comment.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        form = CommentForm()

    context={
        'post': article,
        'categories': categories,
        'comments': comments,
        'form': form
    }
    return render(request, 'home/post_detail.html', context)




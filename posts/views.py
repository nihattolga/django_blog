from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, CommentForm, CategoryForm
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Article
from django.core.exceptions import PermissionDenied

User = get_user_model()

@login_required
def post_create(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()

            messages.success(request, 'Your article is now Live!')
            return HttpResponseRedirect('/index/')
    context = {
        'form': form
    }
    return render(request, "posts/post_create.html", context)

@login_required
def post_edit(request, id, slug):
    print(request.user.id)
    post = get_object_or_404(Article, article_id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=post)
    if request.user.is_authenticated and request.user.id == post.created_by.id:
        if request.method == "POST":
            if form.is_valid():
                form.instance.created_by = request.user
                form.save()
                return HttpResponseRedirect('/')
        context = {
            'form': form,
            'post': post,
        }
        return render(request, "posts/post_edit.html", context)
    else:
        raise PermissionDenied

@login_required
def post_delete(request, id, slug):
    post = get_object_or_404(Article, article_id=id) 
    user = User.objects.get(pk=request.user.id)
    if request.user.is_authenticated and request.user.id == post.created_by.id:
        post.delete()
        return HttpResponseRedirect('/')
    else:
        raise PermissionDenied

    return render(request, 'posts/post_delete.html')

@login_required
def category_create(request):
    form = CategoryForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/post/create/')
        else:
            form = CategoryForm()

    context = {
        'form': form
    }
    return render(request, 'posts/create_cat.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import SigUpForm, LoginForm, UpdateForm
from django.contrib.auth.decorators import login_required
from .models import User
from posts.models import Article, Comment
from django.core.exceptions import PermissionDenied
from django.db.models import Count


def signup_view(request, *args, **kwargs):
    form = SigUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('accounts:accounts_login')
    context = {
        'form': form
    }
    return render(request, "accounts/signup.html", context)


def login_view(request, *args, **kwargs):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        return HttpResponseRedirect("/")
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def update_view(request, *args, **kwargs):
    user = User.objects.get(pk=request.user.id)
    if user.id != request.user.id:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = UpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:accounts_view")
        else:
            form = UpdateForm(request.POST, instance=request.user,
                initial={
                    "id": user.id,
                    "email": user.email, 
                    "username": user.username,
                    "avatar": user.avatar,
                    "bio": user.bio,
                }
            )
            context['form'] = form
    else:
        form = UpdateForm(
            initial={
                    "id": user.id,
                    "email": user.email, 
                    "username": user.username,
                    "avatar": user.avatar,
                    "bio": user.bio,
                }
            )
        context['form'] = form
    return render(request, "accounts/account_edit.html", context)

@login_required
def deactivate_view(request):
    user = User.objects.get(pk=request.user.id)
    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            logout(request)
            user.update(is_active= False)
            return HttpResponseRedirect('/')             
        return render(request, "accounts/account_deactivate.html")
    else:
        raise PermissionDenied

@login_required
def delete_view(request):
    user = User.objects.get(pk=request.user.id)
    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            logout(request)
            user.delete()
            return HttpResponseRedirect('/')
                
        return render(request, "accounts/account_delete.html")
    else:
        raise PermissionDenied

@login_required
def account_bookmark_add(request, id):
    post = get_object_or_404(Article, article_id=id)
    if post.bookmark.filter(id=request.user.id).exists():
        post.bookmark.remove(request.user)
    else:
        post.bookmark.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def post_upvote(request, id):
    post = get_object_or_404(Article, article_id=id)
    if post.upvote.filter(id=request.user.id).exists():
        post.upvote.remove(request.user.id)
    else:
        post.upvote.add(request.user)
        if post.downvote.filter(id=request.user.id).exists():
            post.downvote.remove(request.user.id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def post_downvote(request, id):
    post = get_object_or_404(Article, article_id=id)
    if post.downvote.filter(id=request.user.id).exists():
        post.downvote.remove(request.user.id)
    else:
        post.downvote.add(request.user)
        if post.upvote.filter(id=request.user.id).exists():
            post.upvote.remove(request.user.id)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def account_view(request):
    user_saved_posts = Article.objects.filter(bookmark=request.user).annotate(ncomment=Count('comment'),
     ncategory=Count('category'))
    user_upvoted_posts = Article.objects.filter(upvote=request.user).annotate(ncomment=Count('comment'),
     ncategory=Count('category'))
    user_downvoted_posts = Article.objects.filter(downvote=request.user).annotate(ncomment=Count('comment'),
     ncategory=Count('category'))
    user_posts = Article.objects.filter(created_by=request.user).annotate(ncomment=Count('comment'),
     ncategory=Count('category'))
    user_comments = Comment.objects.filter(created_by=request.user)
    user = User.objects.get(id=request.user.id)

    context = {
        'user_posts': user_posts,
        'user_saved_posts': user_saved_posts,
        'user_upvoted_posts': user_upvoted_posts,
        'user_downvoted_posts': user_downvoted_posts,
        'user_comments': user_comments,
        'user': user
    }


    return render(request, 'accounts/account_view.html', context)



from django.urls import path
from .views import post_create, post_edit, post_delete, category_create

app_name = 'posts'

urlpatterns = [
    path('post/create/', post_create, name='post_create'),
    path('post/edit/<id>/<slug>/', post_edit, name='post_edit'),
    path('post/delete/<id>/<slug>/', post_delete, name='post_delete'),
    path('category/create/', category_create, name='category_create')
]

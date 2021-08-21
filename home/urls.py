from django.urls import path
from .views import index, articles_by_cat, detail_view, search, categories_view

app_name = 'home'

urlpatterns = [
    path('', index),
    path('index/', index, name='index'),
    path('posts/category/', categories_view, name='categories'),
    path('posts/category/<id>/<category>', articles_by_cat, name='post_by_categories'),
    path('posts/<id>/<slug>/', detail_view, name='detail_view'),
    path('search/', search, name='search')
    
]

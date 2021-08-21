from django.contrib import admin
from .models import Article, Comment, Category

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category','created_by', 'created_at',
     'updated_at', 'view')
    list_filter = ('title', 'category')
    prepopulated_fields = {'slug': ('title', ) }

    filter_horizontal =('upvote', 'downvote', 'bookmark')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
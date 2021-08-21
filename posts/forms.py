from django import forms
from django.forms import ModelForm, Textarea, TextInput, FileInput, Select
from .models import Article, Comment, Category

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'subtitle','thumbnail', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']
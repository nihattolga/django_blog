from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()
    
class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category

class Article(models.Model):
    article_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='article_thumbnail_images', null=True, blank=True)
    content = RichTextField(blank=True)
    category = models.ForeignKey(Category, to_field="category_id", on_delete=models.DO_NOTHING)
    slug = models.SlugField(max_length=255, unique=False)
    created_by = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvote = models.ManyToManyField(User, related_name='upvote', default=None, blank=True)
    downvote = models.ManyToManyField(User, related_name='downvote', default=None, blank=True)
    view = models.IntegerField(default=0)
    bookmark = models.ManyToManyField(User, related_name='saved', default=None, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.article_id:
            self.slug = slugify(self.title) + slugify(self.article_id)
        super(Article, self).save(*args, **kwargs)

    def total_upvote(self):
        return(self.upvote.count())

    def total_downvote(self):
        return(self.downvote.count())

@receiver(pre_delete, sender=Article)
def Article_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.thumbnail.delete(False)

class Comment(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article, to_field="article_id", related_name='comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
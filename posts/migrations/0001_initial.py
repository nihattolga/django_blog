# Generated by Django 3.2.6 on 2021-08-21 04:01

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='article_thumbnail_images')),
                ('content', ckeditor.fields.RichTextField(blank=True)),
                ('slug', models.SlugField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('view', models.IntegerField(default=0)),
                ('bookmark', models.ManyToManyField(blank=True, default=None, related_name='saved', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='posts.article')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='posts.category'),
        ),
        migrations.AddField(
            model_name='article',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
        migrations.AddField(
            model_name='article',
            name='downvote',
            field=models.ManyToManyField(blank=True, default=None, related_name='downvote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='upvote',
            field=models.ManyToManyField(blank=True, default=None, related_name='upvote', to=settings.AUTH_USER_MODEL),
        ),
    ]
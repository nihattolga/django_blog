import random
import secrets
import string   
import datetime

import names

from django.core.management.base import BaseCommand
from posts.models import Article, Category, Comment
from accounts.models import User

from .create_random_txt import txt_generator, tokenize_words
from .create_thumbnail.anime_face_generetor import generate_faces

categories = [
    'Sport',
    'Lifestyle',
    'Music',
    'Coding',
    'Travelling',
    'Business',
    'Technology',
    'Food',
    'Finance',
    'Fitness',
    'Calisthenics:)',
    'Politics',
    'Parenting',
    'Movies',
    'Cars',
    'News',
    'Pets',
    'Gaming'
]


file = open("blog/create_random_txt/dataset/11.txt").read()\
+open("blog/create_random_txt/dataset/1342.txt").read()\
+open("blog/create_random_txt/dataset/1661.txt").read()\
+open("blog/create_random_txt/dataset/84.txt").read()

def generate_author_name():
    index = random.randint(0, 499)
    return user[index]

def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))

def generate_avatar():
    return generate_faces()

def generate_category_name():
    index = random.randint(0, 17)
    return categories[index]

def generate_publish_date():
    year = random.randint(2000, 2021)
    month = random.randint(1, 12)
    if month==2:
        day = random.randint(1, 29)
    elif month==(1 or 3 or 5 or 7 or 8 or 10 or 12)
        day = random.randint(1, 31)
    else:
        day = random.randint(1, 30)
    return datetime.date(year, month, day)

def create_user(n_users, file=file):
    users = [names.get_first_name() for i in range(n_users)]
    for u in users:
        User.objects.create_user(username=u, email='{}.gmail.com'.format(u),
        password=generate_password(), avatar=generate_avatar(),
        bio='this is a bio which belongs to {}...'.format(u))
        User.save()

def create_article(n_article, n_users, file=file):
    for i in range(n_article):
        date_1 = generate_publish_date()
        date_2 = generate_publish_date()
        view = random.randint(1,n_users)
        l = (list(User.objects.all().values_list('id', flat=True)))
        if i > i*95/100:
            if date_1 > date_2:
                Article(title=txt_generator(file, random.randint(5,15)),
                    subtitle=txt_generator(file, random.randint(5,15)), 
                    thumbnail=generate_avatar(),
                    content=txt_generator(file, random.randint(200,2000)),
                    category=Category.objects.get_or_create(category=generate_category_name()),
                    created_by=User.objects.get(username=generate_author_name()),
                    created_at=date_2, updated_at=date_1, view=view).save()
            else:
                Article(title=txt_generator(file, random.randint(5,15)),
                    subtitle=txt_generator(file, random.randint(5,15)), 
                    thumbnail=generate_avatar(),
                    content=txt_generator(file, random.randint(200,2000)),
                    category=Category.objects.get_or_create(category=generate_category_name()),
                    created_by=User.objects.get(username=generate_author_name()),
                    created_at=date_1, updated_at=date_2, view=view).save()

            random.shuffle(l)
            l = l[:random.randint(0:(n_users-1))]
               
            for i in range(len(l)):
                Article.upvote.add(l[i])

            random.shuffle(l)
            l = l[:random.randint(0:(n_users-1))]
            for i in range(len(l)):
                Article.downvote.add(l[i])

            random.shuffle(l)
            l = l[:random.randint(0:(n_users-1))]
            for i in range(len(l)):
                Article.bookmark.add(l[i])

        else:
            Article(title=txt_generator(file, random.randint(5,15)),
                subtitle=txt_generator(file, random.randint(5,15)), 
                thumbnail=generate_avatar(),
                content=txt_generator(file, random.randint(200,2000)),
                category=Category.objects.get_or_create(category=generate_category_name()),
                created_by=User.objects.get(username=generate_author_name()),
                created_at=date_1, updated_at=date_1, view=view).save()


            random.shuffle(l)
            l = l[:random.randint(0:(n_users-1))]
               
            for i in range(len(l)):
                Article.upvote.add(l[i])

            random.shuffle(l)
            l = l[:random.randint(0:(n_users-1))]
            for i in range(len(l)):
                Article.downvote.add(l[i])

            random.shuffle(l)
            l = l[:random.randint(0:(n_users-1))]
            for i in range(len(l)):
                Article.bookmark.add(l[i])    
       

def create_comment(file=file):
    for i in range(random.randint(0,10)): 
        date_1 = generate_publish_date()
        Comment(comment=txt_generator(file, random.randint(5,15)),
            created_by=User.objects.get(username=generate_author_name()),
            created_at=date_1, updated_at=date_1,
            article=Article.objects.get(id=random.randint(1, n_article)))



class Command(BaseCommand):

    def add_arguments(self, parser):
        
        parser.add_argument(
            'n_users', type=int, help='Total user number', default=200)
        parser.add_argument(
            'n_article', type=int, help='Total article number', default=500)
        parser.add_argument
    def handle(self, *args, **kwargs):
        
        create_user(kwargs['n_users'])
        create_article( kwargs['n_article'], kwargs['n_users'])
        create_comment()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))


from django.db import models
from django.contrib.auth.models import User  #  Модель User
# Create your models here.

class Author(models.Model):  # Модель, содержащая объекты всех авторов
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        total_post_rating = 0
        for post in Post.objects.filter(author=self):
            total_comment_post_rating = 0
            for comment in Comment.objects.filter(post=post):
                total_comment_post_rating += comment.rating
            total_post_rating += post.rating * 3 + total_comment_post_rating

        total_self_comment_user_rating = 0
        for comments in Comment.objects.filter(user=self.user):
            total_self_comment_user_rating += comments.comment_rating

        self.rating = total_post_rating + total_self_comment_user_rating
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):  # Модель, содержащая объекты категорий
    name = models.CharField(max_length=30, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name}'

class Post(models.Model):  # Модель, содержащая объекты всех постов
    news = 'NW'
    article = 'AT'

    CHOICE = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    kind = models.CharField(max_length=2, choices=CHOICE, default=news)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=50)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self): # Рейтинг поста
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview = self.text[:124]
        return str(preview) + '...'

    def __str__(self):
        return f'{self.title}:\n{self.text}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на главную страницу
        return f'/news/{self.id}'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self): # Рейтинг коммента
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'
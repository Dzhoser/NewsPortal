from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.FloatField(default = 0.0)

    def update_rating(self):
        #artic_rating = Post.objects.filter(position=Post.article_rating)
        posts = Post.objects.filter(author_id = self.author.id)
        _rating = 0
        for post in posts:
            _rating += 3 * post.article_rating

        aut_comments = Comment.objects.filter(userlink_id = self.author.id)
        for comment in aut_comments:
            _rating += comment.comment_rating

        for post in posts:
            list_comments = Comment.objects.filter(postlink_id = post.id)
            for comment in list_comments:
                _rating += comment.comment_rating

        self.author_rating = _rating



sport = 'SP'
politics = 'PL'
education = 'ED'
entertainment = 'ET'
science = 'SC'

CATEGORIES = [
    (sport, 'Спорт'),
    (politics, 'Политика'),
    (education, 'Образование'),
    (entertainment, 'Развлечения'),
    (science, 'Наука')
]


class Category(models.Model):
    category = models.CharField(max_length=2, choices=CATEGORIES)

news = 'NW'
article = 'AT'

POSTTYPES = [
    (news, 'Новость'),
    (article, 'Статья')
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    posttype = models.CharField(max_length=2, choices=POSTTYPES)
    date_in = models.DateTimeField(auto_now_add = True)
    postcat = models.ManyToManyField(Category, through = 'PostCategory')
    article_text = models.TextField()
    article_rating = models.FloatField(default=0.0)

    def like(self):
        self.article_rating += 1

    def dislike(self):
        self.article_rating -= 1

    def preview(self):
        return ' '.join((self.article_text[0:123], '...'))



class PostCategory(models.Model):
    postlink = models.ForeignKey(Post, on_delete = models.CASCADE)
    categorylink = models.ForeignKey(Category, on_delete = models.CASCADE)



class Comment(models.Model):
    postlink = models.ForeignKey(Post, on_delete = models.CASCADE)
    userlink = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1

    def dislike(self):
        self.comment_rating -= 1
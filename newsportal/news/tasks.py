from .models import Post, Category
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from celery import shared_task

@shared_task
def week_mailing():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    # get all post for the last week
    posts = Post.objects.filter(created_at__gte=last_week)
    # get categories only once
    categories = set(posts.values_list('postcategory__category__name', flat=True))
    subscribers_id = set(Category.objects.filter(name__in=categories).values_list('subscribers', flat=True))

    for subscriber_id in subscribers_id:
        user_mail_ = User.objects.filter(id=subscriber_id).values_list('email', flat=True)
        category_list = Category.objects.filter(subscribers=subscriber_id).values_list('name', flat=True)
        category_list_id = Category.objects.filter(subscribers=subscriber_id).values_list('id', flat=True)
        posts_ = Post.objects.filter(postcategory__category__in=category_list_id)
        week_posts = set(posts_) & set(posts)

        subscriber_categories = set(item for item in category_list)
        week_categories = set(item for item in categories)


        if subscriber_categories & week_categories:
            is_subscribed = True
        else:
            is_subscribed = False

        # is_subscribed = any(item in category_list for item in categories)

        if is_subscribed:
            html_content = render_to_string(
                'daily_post.html',
                {
                    'link': settings.SITE_URL,
                    'posts': week_posts,
                    'categories': list(category_list),

                }
            )
            msg = EmailMultiAlternatives(
                subject='Celery task: Weekly news',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=user_mail_,
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

@shared_task
def new_post_mailing(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postcategory.all()
    subscribers: list(str) = []
    for category in categories:
        subscribers += category.subscribers.all()

    subscribers = [s.email for s in subscribers]

    category_list = Post.objects.filter(pk=pk).values_list('postcategory__category__name', flat=True)
    for subscriber in subscribers:  # send e-mails for each subscriber separately
        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': f"{post.preview()}",
                'link': f"{settings.SITE_URL}/news/{post.pk}",
                'category_list': f"{list(category_list)}",

            }
        )
        msg = EmailMultiAlternatives(
            subject=f"Celery task: {post.topic}",
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
'''Импортируем модули, позволяющие отрабатывать сигналы или "события", такие как отправка post запроса'''
from django.db.models.signals import post_save, post_delete, m2m_changed  # отправляется сигнал после вызова метода save() модели
from django.dispatch import receiver  # декоратор, объявляющий функцию получателя сигнала, функция принимает аргумент
# sender, а также аргументы (**kwargs) в формате словаря; все обработчики сигналов должны принимать подобные аргументы

from .models import Post, Category, PostCategory  # импортируем модели
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.core.mail import mail_admins


# В декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправителе - модель
# Создаем функцию обработчик с параметрами под регистрацию сигнала
# Арг: sender - модель, instance - фактически сохраняемый экз, created - бул, истинно, если была создана новая запись

@receiver(m2m_changed, sender=Post.category.through)
def notify_new_post(sender, action, instance, **kwargs):
    if action == 'post_add':  # если проходит команда post_add, то есть добавляется новость,то выполняются следующие действия:
        subject = f'{instance.title} {instance.created_at.strftime("%d %m %Y")}'
    else:  # если изменена:
        subject = f'Изменено  {instance.title} {instance.created_at.strftime("%d %m %Y")}'
    id_post = instance.pk
    link = f'http://127.0.0.1:8000/{id_post}'
    categories = instance.category.all()
    emails = []

    for category in categories:
        subscribers = category.subscribers.all()
        for sub in subscribers:
            emails.append(sub.email)
    print(emails)

    send_mail(
        subject='"' + subject + '"',
        message='В вашей любимой категории новая публикация:' + link + ' ' + instance.text,
        from_email='example@yandex.ru',
        recipient_list=emails
    )


@receiver(post_delete, sender=Post)
def notify_post_del(sender, instance, **kwargs):
    subject = f'Новость "{instance.title}" удалена'

    send_mail(
        subject=subject,
        message=instance.text,
        from_email='example@yandex.ru',
        recipient_list=['example@yandex.ru']
    )

# Generated by Django 4.1.4 on 2023-01-05 08:33

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
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_rating', models.FloatField(default=0.0)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('SP', 'Спорт'), ('PL', 'Политика'), ('ED', 'Образование'), ('ET', 'Развлечения'), ('SC', 'Наука')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posttype', models.CharField(choices=[('NW', 'Новость'), ('AT', 'Статья')], max_length=2)),
                ('date_in', models.DateTimeField(auto_now_add=True)),
                ('heading', models.CharField(max_length=255)),
                ('article_text', models.TextField()),
                ('article_rating', models.FloatField(default=0.0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorylink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('postlink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='postcat',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('date_in', models.DateTimeField(auto_now_add=True)),
                ('comment_rating', models.FloatField(default=0.0)),
                ('postlink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
                ('userlink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

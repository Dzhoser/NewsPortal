from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView  # класс, который позволяет в представлении выводить список объектов из БД
from .models import Post, Category
from django.views.generic import UpdateView, CreateView, DeleteView, TemplateView
from .filters import PostFilter  # импортируем фильтр
from .forms import PostForm
from django.views import View
from django.views.decorators.cache import cache_page


from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.cache import cache


'''Импортируем миксин, который проверяет аутентификацию и допускает на страницу только зарегистрированных пользователей.
 Его добавляем в наследуемые классы. Кроме миксина можно использовать декоратор login_required'''
from django.contrib.auth.mixins import LoginRequiredMixin
'''Импортируем миксин, который проверяет, есть ли у пользователя, обращающегося к представлению, все заданные 
разрешения. Нужно указать разрешение (или итерацию разрешений) с помощью параметра permission_required
<app>.<action>_<model>.'''
from django.contrib.auth.mixins import PermissionRequiredMixin
'''Импортируем встроенный модуль, позволяющий отправлять электронные письма'''

from django.core.mail import *
# from .tasks import *

from django.http import HttpResponse


from django.utils.translation import gettext as _ #  импортируем функцию для перевода
from django.utils.translation import activate, get_supported_language_variant

from django.utils import timezone
import pytz #  импортируем стандартный модуль для работы с часовыми поясами


# rest_framework
import json
from rest_framework import viewsets
from rest_framework import permissions            # https://www.django-rest-framework.org/api-guide/permissions/
from rest_framework.response import Response
import django_filters.rest_framework
from news.serializers import *
from news.models import *


# Create your views here.




class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'  # указываем имя шаблона, показывающий как именно выводить страницу (HTML)
    context_object_name = 'posts'  # имя списка с объектами (нужен, чтобы обратиться к нему в HTML)
    queryset = Post.objects.order_by('-created_at')  # то в каком порядке мы выводим элементы (сначала новые)
    paginate_by = 2  # постраничный вывод в х элементов


class PostDetail(DetailView):  # редставление, в котором будут детали конкретного отдельного поста
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    # pk_url_kwarg = 'id'

    # def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
    #     # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
    #     obj = cache.get(f'post-{self.kwargs["id"]}', None)
    #
    #     # если объекта нет в кэше, то получаем его и записываем в кэш
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'post-{self.kwargs["id"]}', obj)
    #     return obj


class PostSearch(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, показывающий как именно выводить страницу (HTML)
    context_object_name = 'posts'  # имя списка с объектами (нужен, чтобы обратиться к нему в HTML)
    queryset = Post.objects.order_by('-created_at')  # то в каком порядке мы выводим элементы (сначала новые)
    # Далее настраиваем URL, чтобы к представлению можно было "обратиться". Создаем urls.py

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты
        # переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class CategoryDetail(DetailView):  # представление, в котором будут детали категории
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'



class PostAdd(CreateView, LoginRequiredMixin, PermissionRequiredMixin):  # Джейнерик для создания объекта
    template_name = 'add.html'
    form_class = PostForm
    # Форма разрешений: <app>.<action>_<model>.
    permission_required = ('news.add_post', 'news.delete_post', 'news.change_post')

    def post(self, request, *args, **kwargs):
        '''Отправляет письмо подписчикам после создания нового поста'''
        form = PostForm(request.POST)
        post = form.save()
        post_categories = post.category.all()
        list_of_users = []
        for category in post_categories:
            for i in range(len(Category.objects.get(name=category).subscribers.all())):
                list_of_users.append(Category.objects.get(name=category).subscribers.all()[i].email)
        send_mail(
            subject='Новый пост на портале newsportal!',
            message=f'Новая новость в вашей категории!',
            from_email='example@yandex.ru',
            recipient_list=list_of_users,
        )
        return redirect('/news')

class PostDelete(DeleteView, PermissionRequiredMixin, LoginRequiredMixin):  # Джейнерик для удаления объекта
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.add_post', 'news.delete_post', 'news.change_post')


class PostUpdate(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):  # Джейнерик для редактирования объекта, используем тот же шаблон add
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post', 'news.delete_post', 'news.change_post')

    # get_object используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class SubscribeCategory(UpdateView):   # представление для редактирования объекта category и добавление подписчиков
    model = Category
    context_object_name = 'subscribe_category'

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=self.kwargs.get('pk'))
        email = request.user.email
        if not Category.objects.get(pk=self.kwargs.get('pk')).subscribers.filter(username=self.request.user).exists():
            Category.objects.get(pk=self.kwargs.get('pk')).subscribers.add(self.request.user)
            send_mail(
                subject=f'{category.name}',
                message=f'Категория на которую вы подписаны: {category.name}.  ',
                from_email='merrimorlavrushina@yandex.ru',
                recipient_list=[email],
            )
        else:
            Category.objects.get(pk=self.kwargs.get('pk')).subscribers.remove(self.request.user)

        return redirect(request.META.get('HTTP_REFERER'))


# class Index(View):
#     def get(self, request):
#         # string = _('Hello world')
#         # context = {'string': string }
#
#         models = Post.objects.all()
#         context = {
#             'models': models,
#         }
#
#         return HttpResponse(render(request, 'index.html', context))


class Index(View):
    def get(self, request):
        curent_time = timezone.now()

        # .  Translators: This message appears on the home page only
        models = Post.objects.all()

        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


# ===== rest_framework =====
# create a ReadOnly
class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["author", "id", "category", "rating"]

    # deny all by default using rest_framework
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # set a readOnly by default using rest_framework
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    # set a IsAuthenticated rights by default using rest_framework
    permission_classes = [permissions.IsAuthenticated]


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # set a IsAdminUser rights by default using rest_framework
    permission_classes = [permissions.IsAdminUser]


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # .filter(is_active=True) #- we won't see this instance in API
    serializer_class = CommentSerializer

    # set a readOnly
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def destroy(self, request, pk, format=None):  # set new functionality for delete
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=204)  # status.HTTP_204_NO_CONTENT

# ==========================

# ===== REST API =====

def get_news_list(_):
    news_list = Post.objects.all().values(
        'id',
        'title',
    )
    return HttpResponse(content=news_list, status=200)


def get_news(_, pk):
    news = Post.objects.filter(pk=pk)
    return HttpResponse(content=news, status=200)


def create_news(request):
    if request.method == 'POST':
        # body = json.loads(request.body.decode('utf-8'))
        body = json.loads(request.body)
        news = Post.objects.create(
            topic=body['title'],
            content=body['kind'],
            author=body['author'],
            contentType=body['category'],
        )
        return HttpResponse(content=news, status=201)


def edit_news(request, pk):
    body = json.loads(request.body.decode('utf-8'))
    news = Post.objects.get(pk=pk)
    for attr, value in body.items():
        setattr(news, attr, value)
    news.save()
    data = {'title': news.title, 'kind': news.kind, 'author': news.author, 'contentType': news.category}
    print(data)
    return HttpResponse(content=data, status=200)


def delete_news(_, pk):
    news = Post.objects.get(pk=pk).delete()
    return HttpResponse(content=news, status=204)

# =======================
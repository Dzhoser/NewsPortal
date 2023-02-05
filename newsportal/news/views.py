from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView  # класс, который позволяет в представлении выводить список объектов из БД
from .models import Post, Category
from django.views.generic import UpdateView, CreateView, DeleteView, TemplateView
from .filters import PostFilter  # импортируем фильтр
from .forms import PostForm
from django.views import View


from datetime import datetime, timedelta
from django.contrib.auth.models import User

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

    # def post(self, request, *args, **kwargs):
    #     '''Отправляет письмо подписчикам после создания нового поста'''
    #     form = PostForm(request.POST)
    #     post = form.save()
    #     post_categories = post.category.all()
    #     list_of_users = []
    #     for category in post_categories:
    #         for i in range(len(Category.objects.get(name=category).subscribers.all())):
    #             list_of_users.append(Category.objects.get(name=category).subscribers.all()[i].email)
    #     send_mail(
    #         subject='Новый пост на портале newsportal!',
    #         message=f'Новая новость в вашей категории!',
    #         from_email='example@yandex.ru',
    #         recipient_list=list_of_users,
    #     )
    #     return redirect('/news')

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





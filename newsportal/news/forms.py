from django.forms import ModelForm
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета описываем модель, по которой будет строится форма
    class Meta:
        model = Post
        fields = ['author', 'kind', 'category', 'title', 'text']


# Кастомизируем форму регистрации SignupForm, которую предоставляет пакет allauth
# В кастомизированном классе формы, в котором мы хотим добавлять пользователя в группу, мы должны переопределить
# только метод save(), который выполняется при успешном заполнении формы регистрации.
class BasicSignupForm(SignupForm):

    # Встроенная ф-ция super обращается к атрибутам классов стоящих над текущем порядке наследования без указания имени
    # Функция может принимать 2 параметра. super([type [, object]]). Первый аргумент – это тип, к предкам которого
    # мы хотим обратиться. А второй аргумент – это объект, к которому надо привязаться.
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user  # Обязательным требованием метода save() является возвращение объекта модели User по итогу вып.

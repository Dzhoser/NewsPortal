from django_filters import FilterSet
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться
    class Meta:
        model = Post
        fields = {  # чтобы нам выводило что-то хотя бы отдалённо похожее на то что запросил пользователь
                  'title':['icontains']
        }  # поля, которые мы будем фильтровать


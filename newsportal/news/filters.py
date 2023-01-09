from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Category

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    # category = ModelChoiceFilter(
    #     field_name = 'Категория',
    #     queryset = Category.category
    #     )



   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'heading': ['icontains'],
           # количество товаров должно быть больше или равно
           'date_in': ['gt'],
           'postcat__category': ['exact']
       }
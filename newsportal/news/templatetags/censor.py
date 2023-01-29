# Создание своего фильтра
from django import template

register = template.Library()  # регистрируем фильтры, чтобы Джанго их "увидел"


@register.filter(name='censor')  # регистрируем фильтр как фильтр
def censor(value):
    censor_list = ['Бурно']
    if isinstance(value, str):  # проверяем, что значение - строка
        value = value.split()  # разбиваем на слова
        new_value = []
        for word in value:
            if word in censor_list:  # если слово в цензор-списке, цензурируем
                new_value += '*нецензурная лексика*' + ' '
            else:
                new_value += word + ' '
        new_value = "".join(new_value)
        return str(new_value)  # возвращаем цензурированное значение

#         # if value == word:
#         #     word = '* ненормативная лексика *'
#         # return word
    else:
        raise ValueError(f'Нельзя приминить этот фильтр не к строке')  # кидаем ошибку, если применяется не к строке

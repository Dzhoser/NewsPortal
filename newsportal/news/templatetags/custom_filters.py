from django import template


register = template.Library()

def change_word(word):
    _word = word[0] + (len(word)-1) * '*'
    return  _word


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor_text(value):
    """
    value: значение, к которому нужно применить фильтр
    """
    # Возвращаемое функцией значение подставится в шаблон.
    censored_words = {'редиска', 'морковка'}
    _value = value
    for word in censored_words:
        _value = _value.replace(word, change_word(word))

    return f'{_value}'
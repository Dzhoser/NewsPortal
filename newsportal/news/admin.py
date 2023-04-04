from django.contrib import admin
from .models import Post, Author, Comment, Category, PostCategory
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

#Настройка моделей в админке:
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые хотим видеть в таблице с товарами
    list_display = ('id', 'title', 'text', 'created_at')
    list_filter = ('id', 'title', 'created_at')  # фильтры
    list_display_links = ('id', 'title')
    search_fields = ('title', 'created_at')


class CategoryAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые хотим видеть в таблице с товарами
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


class CategoryAdmin(TranslationAdmin):
    model = Category


# add translation area
class PostAdmin(TranslationAdmin):
    model = Post



# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory)

# add translation area

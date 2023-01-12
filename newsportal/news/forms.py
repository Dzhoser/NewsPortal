from django import forms
from .models import Post, Category

# from django.forms import ModelChoiceField

# class CategoryModelChoiceField(ModelChoiceField):
#     def label_from_instance(self, obj):
#          return obj.category

class PostFormNews(forms.ModelForm):
   # postcat = CategoryModelChoiceField(queryset=Category.objects.all())
   class Meta:
       model = Post
       fields = [
           'author',
           'postcat',
           'heading',
           'article_text',
           'article_rating'
       ]


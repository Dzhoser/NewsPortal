from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostsDetail


urlpatterns = [
   # path — означает путь.

   path('', PostsList.as_view()),
   path('<int:pk>', PostsDetail.as_view()),
]
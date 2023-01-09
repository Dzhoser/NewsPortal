from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostsDetail, SearchList


urlpatterns = [
   # path — означает путь.

   path('', PostsList.as_view()),
   path('<int:pk>', PostsDetail.as_view()),
   path('search', SearchList.as_view()),
]
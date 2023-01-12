from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostsDetail, SearchList, PostCreateNews, PostUpdateNews, PostDeleteNews, PostCreateArticles, PostUpdateArticles, PostDeleteArticles


urlpatterns = [
   # path — означает путь.

   path('', PostsList.as_view(), name = 'post_list'),
   path('<int:pk>', PostsDetail.as_view(), name = 'post_detail'),
   path('search', SearchList.as_view(), name = 'search_list'),
   path('create', PostCreateArticles.as_view(), name = 'post_create_articles'),
   path('<int:pk>/update/', PostUpdateArticles.as_view(), name='post_update_articles'),
   path('<int:pk>/delete/', PostDeleteArticles.as_view(), name='post_delete_articles'),
]
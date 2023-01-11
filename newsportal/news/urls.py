from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostsDetail, SearchList, PostCreateNews, PostUpdateNews, PostDeleteNews


urlpatterns = [
   # path — означает путь.

   path('', PostsList.as_view(), name = 'post_list'),
   path('<int:pk>', PostsDetail.as_view(), name = 'post_detail'),
   path('search', SearchList.as_view(), name = 'search_list'),
   path('create', PostCreateNews.as_view(), name = 'post_create_news'),
   path('<int:pk>/update/', PostUpdateNews.as_view(), name='post_update_news'),
   path('<int:pk>/delete/', PostDeleteNews.as_view(), name='post_delete_news'),
]
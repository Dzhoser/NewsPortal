from django.urls import path  # path — означает путь
from .views import PostList, PostDetail, CategoryDetail, PostSearch,  PostAdd, PostUpdate, PostDelete, SubscribeCategory, get_news_list, get_news, create_news, edit_news, delete_news
from django.views.decorators.cache import cache_page


# rest_framework
from django.urls import path, include
from rest_framework import routers
from news import views
router = routers.DefaultRouter()
router.register(r'news', views.PostViewset)
router.register(r'catergory', views.CategoryViewset)
router.register(r'author', views.AuthorViewset)
router.register(r'user', views.UserViewset)
router.register(r'comment', views.CommentViewset)





urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='main'),  # т.к. сам по себе это класс, нам надо представить этот класс в виде view
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category'),
    path('category/<int:pk>/subscribe', SubscribeCategory.as_view(), name='subscribe_category'),
    path('search/', PostSearch.as_view()),
    path('add/', PostAdd.as_view(), name='post_add'),
    path('update/<int:pk>', PostUpdate.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),


# add REST API
   path('api/news/', get_news_list),
   path('api/news/<int:pk>', get_news),
   path('api/create_news/', create_news),
   path('api/edit_news/<int:pk>', edit_news),
   path('api/delete_news/<int:pk>', delete_news),
   path('api-auth/', include(router.urls), name='api'),


]
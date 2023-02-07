from django.urls import path  # path — означает путь
from .views import PostList, PostDetail, CategoryDetail, PostSearch,  PostAdd, PostUpdate, PostDelete, SubscribeCategory
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='main'),  # т.к. сам по себе это класс, нам надо представить этот класс в виде view
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category'),
    path('category/<int:pk>/subscribe', SubscribeCategory.as_view(), name='subscribe_category'),
    path('search/', PostSearch.as_view()),
    path('add/', PostAdd.as_view(), name='post_add'),
    path('update/<int:pk>', PostUpdate.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
]
from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    # path('', adminapp.index, name='index'),
    path('', adminapp.ShopUserList.as_view(), name='index'),
    path('user/create/', adminapp.user_create, name='user_create'),
    path('user/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('user/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),
    path('category/list/', adminapp.categories, name='categories'),
    # path('category/create/', adminapp.category_create, name='category_create'),
    path('category/create/', adminapp.GameCategoryCreateView.as_view(), name='category_create'),
    # path('category/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('category/update/<int:pk>/', adminapp.GameCategoryUpdateView.as_view(),
         name='category_update'),
    # path('category/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('category/delete/<int:pk>/', adminapp.GameCategoryDelete.as_view(), name='category_delete'),
    path('category/<int:pk>/games/', adminapp.category_games, name='category_games'),
    path('category/<int:category_pk>/game/create/', adminapp.game_create, name='game_create'),
    path('game/update/<int:pk>/', adminapp.game_update, name='game_update'),
    path('game/delete/<int:pk>/', adminapp.game_delete, name='game_delete'),
    # path('game/read/<int:pk>/', adminapp.game_read, name='game_read'),
    path('game/read/<int:pk>/', adminapp.GameDetail.as_view(), name='game_read'),
]
"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.index, name='index'),
    re_path(r'^games/$', mainapp.games, name='games'),

    re_path(r'^category/(?P<pk>\d+)/games/$',
            mainapp.games_by_category, name='games_by_category'),
    re_path(r'^category/(?P<pk>\d+)/games/(?P<page>\d+)/$',
            mainapp.games_by_category, name='games_by_category_pagination'),

    re_path(r'^game/(?P<pk>\d+)/$', mainapp.game, name='game'),

    re_path(r'^points/$', mainapp.points, name='points'),
]

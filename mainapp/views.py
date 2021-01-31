import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from mainapp.models import GameCategory, Game


def get_categories():
    return GameCategory.objects.filter(is_active=True)


def get_new_game():
    return random.choice(Game.objects.filter(is_active=True))


def index(request):
    context = {
        'page_title': 'интернет-магазин игр ubisoft',
    }
    return render(request, 'mainapp/index.html', context)


def games(request):
    all_games = Game.objects.filter(is_active=True)
    new_game = get_new_game()

    context = {
        'page_title': 'игры',
        'categories': get_categories(),
        'all_games': all_games,
        'new_game': new_game,
    }
    return render(request, 'mainapp/games.html', context)


def games_by_category(request, pk, page=1):
    if pk == '0':
        category = {'pk': 0, 'name': 'все жанры'}
        all_games = Game.objects.filter(is_active=True)
    else:
        category = get_object_or_404(GameCategory, pk=pk)
        all_games = category.game_set.filter(is_active=True)

    games_paginator = Paginator(all_games, 2)
    try:
        all_games = games_paginator.page(page)
    except PageNotAnInteger:
        all_games = games_paginator.page(1)
    except EmptyPage:
        all_games = games_paginator.page(games_paginator.num_pages)

    context = {
        'page_title': 'каталог',
        'categories': get_categories(),
        'all_games': all_games,
        'category': category,
    }
    return render(request, 'mainapp/games_by_category.html', context)


def game(request, pk):
    context = {
        'page_title': 'продукт',
        'game': get_object_or_404(Game, pk=pk),
        'categories': get_categories(),
    }

    return render(request, 'mainapp/game.html', context)


def points(request):
    locations = [
        {
            'city': 'Красноярск',
            'phone': '+7-950-150-0000',
            'email': 'ubikrk@gmail.com',
            'adress': 'Киренского 2и оф. 101',
        },
        {
            'city': 'Новосибирск',
            'phone': '+7-990-250-0000',
            'email': 'ubinsk@gmail.com',
            'adress': 'Кирова 28 оф. 55',
        },
        {
            'city': 'Омск',
            'phone': '+7-910-350-0000',
            'email': 'ubiomsk@gmail.com',
            'adress': 'Огородный переулок 12 оф. 1',
        },
    ]

    context = {
        'page_title': 'точки самовывоза',
        'locations': locations,
    }
    return render(request, 'mainapp/points.html', context)

import os
import json

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import GameCategory, Game
from django.conf import settings


def load_from_json(file_name):
    with open(
            os.path.join(settings.JSON_PATH, f'{file_name}.json'),
            encoding='utf-8'
    ) as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):
        categories = load_from_json('category')

        GameCategory.objects.all().delete()
        [GameCategory.objects.create(**category) for category in categories]

        games = load_from_json('games')
        Game.objects.all().delete()
        for game in games:
            category_name = game['category']
            _category = GameCategory.objects.get(name=category_name)
            game['category'] = _category
            new_game = Game(**game)
            new_game.save()

        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser(username='django', email='admin@geekshop.local', password='geekbrains')

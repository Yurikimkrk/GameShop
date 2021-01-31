from django.contrib import admin

from mainapp.models import GameCategory, Game

admin.site.register(GameCategory)
admin.site.register(Game)
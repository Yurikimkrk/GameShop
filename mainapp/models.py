from django.db import models


class GameCategory(models.Model):
    name = models.CharField('имя категории', max_length=64)
    descript = models.TextField('описание категории', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'


class Game(models.Model):
    category = models.ForeignKey(GameCategory,
                                 on_delete=models.CASCADE,
                                 verbose_name='категория игры')
    name = models.CharField(verbose_name='имя игры', max_length=128)
    image = models.ImageField(upload_to='games_images', blank=True)
    short_desc = models.CharField(verbose_name='краткое описание игры', max_length=64, blank=True)
    descript = models.TextField(verbose_name='описание игры', blank=True)
    price = models.DecimalField(verbose_name='цена игры', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

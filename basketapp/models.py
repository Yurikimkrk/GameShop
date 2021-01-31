from django.db import models

from authapp.models import ShopUser
from mainapp.models import Game


# class BasketQuerySet(models.QuerySet):  # own model manager
#     def delete(self):
#         for object in self:
#             # object.product.quantity += object.quantity
#             # object.product.save()
#             object.delete()
#         return super().delete()

class Basket(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    # objects = BasketQuerySet.as_manager()

    @property
    def game_cost(self):
        return self.game.price * self.quantity

    @property
    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self.user.basket.all()))
        # return sum([el.quantity for el in self.user.basket.all()])

    @property
    def total_cost(self):
        return sum(map(lambda x: x.game_cost, self.user.basket.all()))
        # return sum([el.game_cost() for el in self.user.basket.all()])

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     pass

    # def delete(self, using=None, keep_parents=False):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     return super().delete(using=None, keep_parents=False)

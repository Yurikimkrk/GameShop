from django.contrib.auth import get_user_model
from django.db import models

from authapp.models import ShopUser
from mainapp.models import Game


class Order(models.Model):
    FORMING = 'F'
    SENT_TO_PROCEED = 'S'
    PROCEEDED = 'P'
    PAID = 'D'
    READY = 'Y'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус',
                              max_length=1,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id}'

    #
    def get_total_quantity(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_game_type_quantity(self):
        items = self.orderitems.all()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity * x.game.price, items)))

    # def delete(self):
    #     for item in self.orderitems.select_related():
    #         item.game.quantity += item.quantity
    #         item.game.save()
    #
    #     self.is_active = False
    #     self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    game = models.ForeignKey(Game,
                             verbose_name='игра',
                             on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)

    @property
    def game_cost(self):
        return self.game.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)

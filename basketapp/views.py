from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from geekshop.settings import LOGIN_URL
from mainapp.models import Game


@login_required
def index(request):
    return render(request, 'basketapp/index.html')


@login_required
def add_game(request, pk):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(
            reverse(
                'mainapp:game',
                kwargs={'pk': pk}
            )
        )

    game = get_object_or_404(Game, pk=pk)
    basket = Basket.objects.filter(user=request.user, game=game).first()

    if not basket:
        basket = Basket(user=request.user, game=game)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_game(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return HttpResponseRedirect(reverse('basket:index'))


@login_required
def change(request, pk, quantity):
    if request.is_ajax():
        basket = get_object_or_404(Basket, pk=pk)
        if quantity <= 0:
            basket.delete()
        else:
            basket.quantity = quantity
            basket.save()

        result = render_to_string(
            'basketapp/includes/inc__basket_list.html',
            request=request
        )

        return JsonResponse({'result': result})
        # return JsonResponse({
        #     'total_cost': basket.total_cost,
        #     'total_quantity': basket.total_quantity,
        #     'game_cost': basket.game_cost,
        # })


# @receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def game_quantity_update_save(sender, update_fields, instance, **kwargs):
    print(f'pre save: {sender}')
    if instance.pk:
        instance.game.quantity -= instance.quantity - \
                                     sender.get_item(instance.pk).quantity
    else:
        instance.game.quantity -= instance.quantity
    instance.game.save()


# @receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def game_quantity_update_delete(sender, instance, **kwargs):
    print(f'pre delete: {sender}')
    instance.game.quantity += instance.quantity
    instance.game.save()

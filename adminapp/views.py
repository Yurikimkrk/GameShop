from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm, AdminGameCategoryUpdateForm, \
    AdminGameUpdateForm
from authapp.models import ShopUser
from mainapp.models import GameCategory, Game


# @user_passes_test(lambda x: x.is_superuser)
# def index(request):
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': 'админка/пользователи',
#         'object_list': users_list
#     }
#


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.page_title
        return context


class ShopUserList(SuperUserOnlyMixin, ListView):
    model = ShopUser


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = AdminShopUserCreateForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserCreateForm()

    context = {
        'title': 'пользователи/создание',
        'form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserUpdateForm(instance=user)

    context = {
        'title': 'пользователи/редактирование',
        'form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))

    context = {
        'title': 'пользователи/удаление',
        'user_to_delete': user,
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def categories(request):
    categories = GameCategory.objects.all()
    context = {
        'title': 'админка/категории',
        'object_list': categories,
    }
    return render(request, 'adminapp/categories_list.html', context)


# @user_passes_test(lambda x: x.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         form = AdminGameCategoryUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('my_admin:categories'))
#     else:
#         form = AdminGameCategoryUpdateForm()
#
#     context = {
#         'title': 'категории игр/создание',
#         'form': form
#     }
#     return render(request, 'adminapp/gamecategory_form.html', context)

class GameCategoryCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = GameCategory
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminGameCategoryUpdateForm
    page_title = 'категории игр/создание'


# @user_passes_test(lambda x: x.is_superuser)
# def category_update(request, pk):
#     obj = get_object_or_404(GameCategory, pk=pk)
#     if request.method == 'POST':
#         form = AdminGameCategoryUpdateForm(request.POST, request.FILES, instance=obj)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('my_admin:categories'))
#     else:
#         form = AdminGameCategoryUpdateForm(instance=obj)
#
#     context = {
#         'title': 'категории игр/редактирование',
#         'form': form
#     }
#     return render(request, 'adminapp/templates/mainapp/gamecategory_form.html', context)

class GameCategoryUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = GameCategory
    success_url = reverse_lazy('my_admin:categories')
    form_class = AdminGameCategoryUpdateForm
    page_title = 'категории игр/редактирование'


# @user_passes_test(lambda x: x.is_superuser)
# def category_delete(request, pk):
#     obj = get_object_or_404(GameCategory, pk=pk)
#
#     if request.method == 'POST':
#         obj.is_active = False
#         obj.save()
#         return HttpResponseRedirect(reverse('my_admin:categories'))
#
#     context = {
#         'title': 'категории/удаление',
#         'object': obj,
#     }
#     return render(request, 'adminapp/gamecategory_confirm_delete.html', context)

class GameCategoryDelete(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = GameCategory
    success_url = reverse_lazy('my_admin:categories')
    page_title = 'категории игр/удаление'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def category_games(request, pk):
    category = get_object_or_404(GameCategory, pk=pk)
    object_list = category.game_set.all()
    context = {
        'title': f'категория {category.name}/игры',
        'category': category,
        'object_list': object_list
    }
    return render(request, 'adminapp/category_games_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def game_create(request, category_pk):
    category = get_object_or_404(GameCategory, pk=category_pk)
    if request.method == 'POST':
        form = AdminGameUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_games',
                kwargs={'pk': category.pk}
            ))
    else:
        form = AdminGameUpdateForm(
            initial={
                'category': category,
                'image': 'default.jpg',
            }
        )

    context = {
        'title': 'игры/создание',
        'form': form,
        'category': category,
    }
    return render(request, 'adminapp/game_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = AdminGameUpdateForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_games',
                kwargs={'pk': game.category.pk}
            ))
    else:
        form = AdminGameUpdateForm(instance=game)

    context = {
        'title': 'игры/редактирование',
        'form': form,
        'category': game.category,
    }
    return render(request, 'adminapp/game_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def game_delete(request, pk):
    obj = get_object_or_404(Game, pk=pk)

    if request.method == 'POST':
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(reverse(
            'my_admin:category_games',
            kwargs={'pk': obj.category.pk}
        ))

    context = {
        'title': 'игры/удаление',
        'object': obj,
    }
    return render(request, 'adminapp/game_delete.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def game_read(request, pk):
#     obj = get_object_or_404(Game, pk=pk)
#     context = {
#         'title': 'игры/подробнее',
#         'object': obj,
#     }
#     return render(request, 'adminapp/game_read.html', context)

class GameDetail(DetailView):
    model = Game

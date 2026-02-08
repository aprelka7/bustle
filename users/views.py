from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .forms import CustomUserCreationForm, CustomUserLoginForm, \
    CustomUserUpdateForm
from .models import CustomUser
from django.contrib import messages
from main.models import Dish, Allergen
""" from orders.models import Order """


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('main:index')
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})
    

@login_required(login_url='/users/login')
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.headers.get("HX-Request"):
                return HttpResponse(headers={'HX-Redirect': reverse('users:profile')})
            return redirect('users:profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    recommended_dishes = Dish.objects.all().order_by('id')
    if request.user.is_authenticated:
        excluded_ids = list(request.user.excluded_allergens.values_list('pk', flat=True))
        if excluded_ids:
            recommended_dishes = recommended_dishes.exclude(allergens__id__in=excluded_ids).distinct()
    recommended_dishes = recommended_dishes[:3]

    return TemplateResponse(request, 'users/profile.html', {
        'form': form,
        'user': request.user,
        'recommended_dishes': recommended_dishes,
        'all_allergens': Allergen.objects.all().order_by('name'),
    })


@login_required(login_url='/users/login')
def allergen_preferences(request):
    """Страница выбора аллергенов в профиле."""
    all_allergens = Allergen.objects.all().order_by('name')
    user_excluded_ids = set(request.user.excluded_allergens.values_list('pk', flat=True))
    return TemplateResponse(request, 'users/partials/allergen_preferences.html', {
        'all_allergens': all_allergens,
        'user_excluded_ids': user_excluded_ids,
    })


@login_required(login_url='/users/login')
def update_allergen_preferences(request):
    """Сохранение выбранных аллергенов (исключить из выдачи)."""
    if request.method != 'POST':
        if request.headers.get('HX-Request'):
            return HttpResponse(headers={'HX-Redirect': reverse('users:profile')})
        return redirect('users:profile')
    ids = request.POST.getlist('allergen_ids')
    try:
        ids = [int(x) for x in ids if x.strip().isdigit()]
    except (ValueError, AttributeError):
        ids = []
    valid_ids = list(Allergen.objects.filter(pk__in=ids).values_list('pk', flat=True))
    request.user.excluded_allergens.set(valid_ids)
    user_excluded_ids = set(valid_ids)
    all_allergens = Allergen.objects.all().order_by('name')
    return TemplateResponse(request, 'users/partials/allergen_preferences.html', {
        'all_allergens': all_allergens,
        'user_excluded_ids': user_excluded_ids,
        'saved': True,
    })


@login_required(login_url='/users/login')
def account_details(request):
    user = CustomUser.objects.get(id=request.user.id)
    return TemplateResponse(request, 'users/partials/account_details.html', {'user': user})


@login_required(login_url='/users/login')
def edit_account_details(request):
    form = CustomUserUpdateForm(instance=request.user)
    return TemplateResponse(request, 'users/partials/edit_account_details.html',
                            {'user': request.user, 'form': form})


@login_required(login_url='/users/login')
def update_account_details(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.clean()
            user.save()
            updated_user = CustomUser.objects.get(id=user.id)
            request.user = updated_user
            if request.headers.get('HX-Request'):
                return TemplateResponse(request, 'users/partials/account_details.html', {'user': updated_user})
            return TemplateResponse(request, 'users/partials/account_details.html', {'user': updated_user})
        else:
            return TemplateResponse(request, 'users/partials/edit_account_details.html', {'user': request.user, 'form': form})
    if request.headers.get('HX-Request'):
        return HttpResponse(headers={'HX-Redirect': reverse('user:profile')})
    return redirect('users:profile')


def logout_view(request):
    logout(request)
    if request.headers.get('HX-Request'):
        return HttpResponse(headers={'HX-Redirect': reverse('main:index')})
    return redirect('main:index')

""" @login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return TemplateResponse(request, 'users/partials/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return TemplateResponse(request, 'users/partials/order_detail.html', {'order': order}) """
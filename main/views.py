from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import Category, Dish
from django.db.models import Q


class IndexView(TemplateView):
    template_name = 'main/base.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = None
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'main/home_content.html', context)
        return TemplateResponse(request, self.template_name, context)
    
class CatalogView(TemplateView):
    template_name = 'main/base.html'

    FILTER_MAPPING = {
        'min_price' : lambda queryset, value: queryset.filter(price__gte=value),
        'max_price' : lambda queryset, value: queryset.filter(price__lte=value),
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = kwargs.get('category_slug')
        categories = Category.objects.all()
        dishes = Dish.objects.all().order_by('-created_at')
        show_all_dishes = self.request.GET.get('show_all') in ('1', 'true', 'on')
        if self.request.user.is_authenticated and not show_all_dishes:
            excluded_ids = list(self.request.user.excluded_allergens.values_list('pk', flat=True))
            if excluded_ids:
                dishes = dishes.exclude(allergens__id__in=excluded_ids).distinct()
        current_category = None

        if category_slug:
            current_category = get_object_or_404(Category, slug=category_slug)
            dishes = dishes.filter(category=current_category)
        query = self.request.GET.get('q')
        if query:
            dishes = dishes.filter(
                Q(name__icontains=query)
            )
        
        filter_params = {}
        for param, filter_func in self.FILTER_MAPPING.items():
            value = self.request.GET.get(param)
            if value:
                dishes = filter_func(dishes, value)
                filter_params[param] = value
            else:
                filter_params[param] = ''
            
        filter_params['q'] = query or ''
        filter_params['show_all'] = '1' if show_all_dishes else ''

        context.update({
            'categories': categories,
            'dishes': dishes,
            'current_category': current_category,
            'filter_params': filter_params,
            'search_query': query or '',

        })

        if self.request.GET.get('show_search') == 'true':
            context['show_search'] = True
        elif self.request.GET.get('reset_search') == 'true':
            context['reset_search'] = True
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            if context.get('show_search'):
                return TemplateResponse(request, 'main/search_input.html', context)
            elif context.get('reset_search'):
                return TemplateResponse(request, 'main/search_button.html', {})
            template = 'main/filter_modal.html' if request.GET.get('show_filters') == 'true' else 'main/catalog.html'
            return TemplateResponse(request, template, context)
        return TemplateResponse(request, self.template_name, context)
    

class DishDetailView(DetailView):
    model = Dish
    template_name = 'main/dish_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dish = self.get_object()
        related = Dish.objects.filter(category=dish.category).exclude(id=dish.id)
        if self.request.user.is_authenticated:
            excluded_ids = list(self.request.user.excluded_allergens.values_list('pk', flat=True))
            if excluded_ids:
                related = related.exclude(allergens__id__in=excluded_ids).distinct()
        context['categories'] = Category.objects.all()
        context['related_dishes'] = related[:4]
        context['current_category'] = dish.category.slug
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'main/dish_detail.html', context)
        return self.render_to_response(context)

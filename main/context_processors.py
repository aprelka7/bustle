from .models import Category

def common_context(request):
    return {
        'categories': Category.objects.all(),
        'current_category': request.resolver_match.kwargs.get('slug') if request.resolver_match else None,
    }
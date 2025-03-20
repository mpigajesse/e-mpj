from products.models import Category

def categories(request):
    """Context processor pour rendre les catégories disponibles globalement"""
    return {
        'nav_categories': Category.objects.filter(is_active=True)
    } 
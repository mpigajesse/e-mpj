# Importation des modèles nécessaires
from .models import Category
from django.db.models import Count

def categories_processor(request):
    """
    Context processor qui rend les catégories disponibles globalement
    dans tous les templates.
    
    Returns:
        dict: Dictionnaire contenant les catégories actives et leurs informations
    """
    # Récupérer toutes les catégories actives avec le nombre de produits
    all_categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('products')
    ).order_by('-product_count')

    # Catégories mises en avant (les 5 avec le plus de produits)
    featured_categories = all_categories[:5]
    
    # Grouper les catégories par ordre alphabétique pour la navbar
    nav_categories = all_categories.order_by('name')
    
    return {
        'nav_categories': nav_categories,  # Pour la navbar
        'featured_categories': featured_categories,  # Top 5 catégories
        'all_categories': all_categories,  # Toutes les catégories
    } 
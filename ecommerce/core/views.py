from django.shortcuts import render
from products.models import Category, Product
from django.db.models import Q
import random

# Create your views here.

def home(request):
    # Données pour le hero
    hero_data = {
        'title': 'Découvrez notre sélection unique de produits',
        'subtitle': 'Des articles soigneusement sélectionnés pour répondre à tous vos besoins, avec une qualité exceptionnelle et des prix compétitifs.'
    }
    
    # Récupération des produits mis en avant
    featured_products = list(Product.objects.filter(
        is_active=True,
        is_featured=True,
        image__isnull=False
    ).exclude(
        image=''
    ).select_related('category'))
    
    # Si nous n'avons pas assez de produits mis en avant, compléter avec des produits actifs aléatoires
    if len(featured_products) < 3:
        remaining_products = list(Product.objects.filter(
            is_active=True,
            is_featured=False,
            image__isnull=False
        ).exclude(
            image='',
            id__in=[p.id for p in featured_products]
        ).select_related('category'))
        
        # Mélanger les produits restants et en prendre le nombre nécessaire
        if remaining_products:
            random.shuffle(remaining_products)
            featured_products.extend(remaining_products[:3 - len(featured_products)])
    
    # Si nous avons plus de 3 produits mis en avant, n'en prendre que 3 aléatoirement
    if len(featured_products) > 3:
        featured_products = random.sample(featured_products, 3)
    
    # Statistiques
    stats = [
        {'value': '10K+', 'label': 'Clients satisfaits'},
        {'value': '5K+', 'label': 'Produits disponibles'},
        {'value': '24/7', 'label': 'Support client'}
    ]
    
    # Récupération des catégories actives avec leurs images de façon aléatoire
    categories_with_images = list(Category.objects.filter(
        is_active=True,
        image__isnull=False
    ).exclude(
        image=''
    ))
    
    # Récupérer les catégories sans images
    categories_without_images = list(Category.objects.filter(
        Q(is_active=True),
        Q(image__isnull=True) | Q(image='')
    ))
    
    # Mélanger les deux listes
    random.shuffle(categories_with_images)
    random.shuffle(categories_without_images)
    
    # Prendre les 6 premières catégories avec images
    selected_categories = categories_with_images[:6]
    
    # Si nous n'avons pas assez de catégories avec images, compléter avec celles sans images
    if len(selected_categories) < 6:
        remaining_slots = 6 - len(selected_categories)
        selected_categories.extend(categories_without_images[:remaining_slots])
    
    # Données promotionnelles
    promo_data = {
        'title': 'Offres Spéciales',
        'description': 'Profitez de -20% sur votre première commande avec le code BIENVENUE20'
    }
    
    context = {
        'hero': hero_data,
        'featured_products': featured_products,
        'stats': stats,
        'categories': selected_categories,
        'promo': promo_data,
    }
    
    return render(request, 'core/home.html', context)

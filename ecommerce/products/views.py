from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product

# Create your views here.
def product_list(request):
    """Vue pour afficher la liste des produits avec filtrage et pagination"""
    # Récupération des produits actifs uniquement
    products = Product.objects.filter(is_active=True)
    
    # Filtrage par catégorie
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Filtrage par prix
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Recherche par mot-clé
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Tri des produits
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 12)  # 12 produits par page
    products = paginator.get_page(page)
    
    # Récupération des catégories pour le filtrage
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'current_sort': sort_by,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    """Vue pour afficher les détails d'un produit"""
    # Récupération du produit
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Produits similaires (même catégorie, excluant le produit actuel)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]  # Limite à 4 produits similaires
    
    context = {
        'product': product,
        'related_products': related_products
    }
    
    return render(request, 'products/product_detail.html', context)

def category_list(request):
    """Vue pour afficher la liste des catégories"""
    # Récupération des catégories actives avec le nombre de produits
    categories = Category.objects.filter(is_active=True).prefetch_related('products')
    
    # Calcul du nombre total de produits
    total_products = Product.objects.filter(is_active=True).count()
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(categories, 12)  # 12 catégories par page
    categories = paginator.get_page(page)
    
    context = {
        'categories': categories,
        'total_products': total_products,
    }
    
    return render(request, 'products/category_list.html', context)

def category_detail(request, slug):
    """Vue pour afficher les produits d'une catégorie spécifique"""
    # Récupération de la catégorie
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Récupération des produits de la catégorie
    products = Product.objects.filter(category=category, is_active=True)
    
    # Tri des produits
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 12)  # 12 produits par page
    products = paginator.get_page(page)
    
    context = {
        'category': category,
        'products': products,
        'current_sort': sort_by
    }
    
    return render(request, 'products/category_detail.html', context)






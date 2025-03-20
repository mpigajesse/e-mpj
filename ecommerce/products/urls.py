# Importation des modules nécessaires
from django.urls import path
from . import views

# Définition du namespace de l'application
app_name = 'products'

# Configuration des URLs de l'application
urlpatterns = [
    # Page principale listant tous les produits
    # URL: /products/
    path('', views.product_list, name='product_list'),
    
    # Liste de toutes les catégories
    # URL: /products/categories/
    path('categories/', views.category_list, name='category_list'),
    
    # Détails d'une catégorie spécifique (utilise le slug)
    # URL: /products/category/nom-de-la-categorie/
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Détails d'un produit spécifique (utilise le slug)
    # URL: /products/product/nom-du-produit/
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
] 
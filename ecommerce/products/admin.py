# Importation des modules nécessaires
from django.contrib import admin
from .models import Category, Product, ProductImage

# Configuration de l'affichage inline des images produits dans l'interface d'administration
class ProductImageInline(admin.TabularInline):
    model = ProductImage  # Modèle à utiliser
    extra = 1  # Nombre de formulaires vides à afficher

# Configuration de l'interface d'administration pour les catégories
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la vue liste
    list_display = ['name', 'slug', 'is_active', 'created_at', 'updated_at']
    
    # Filtres disponibles dans la barre latérale
    list_filter = ['is_active', 'created_at', 'updated_at']
    
    # Champs sur lesquels la recherche est possible
    search_fields = ['name', 'description']
    
    # Génération automatique du slug à partir du nom
    prepopulated_fields = {'slug': ('name',)}
    
    # Champs modifiables directement dans la vue liste
    list_editable = ['is_active']
    
    # Navigation par date
    date_hierarchy = 'created_at'

# Configuration de l'interface d'administration pour les produits
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la vue liste
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'is_active', 'is_featured', 'created_at']
    
    # Filtres disponibles dans la barre latérale
    list_filter = ['is_active', 'is_featured', 'category', 'created_at', 'updated_at']
    
    # Champs sur lesquels la recherche est possible
    search_fields = ['name', 'description']
    
    # Génération automatique du slug à partir du nom
    prepopulated_fields = {'slug': ('name',)}
    
    # Champs modifiables directement dans la vue liste
    list_editable = ['price', 'stock', 'is_active', 'is_featured']
    
    # Navigation par date
    date_hierarchy = 'created_at'
    
    # Inclusion des images produits
    inlines = [ProductImageInline]
    
    # Organisation des champs en sections
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Prix et stock', {
            'fields': ('price', 'discount_price', 'stock')
        }),
        ('Images', {
            'fields': ('image',)
        }),
        ('Options', {
            'fields': ('is_active', 'is_featured')
        }),
    )

# Configuration de l'interface d'administration pour les images produits
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    # Liste des champs à afficher dans la vue liste
    list_display = ['product', 'alt_text', 'is_feature', 'created_at']
    
    # Filtres disponibles dans la barre latérale
    list_filter = ['is_feature', 'created_at']
    
    # Champs sur lesquels la recherche est possible
    search_fields = ['product__name', 'alt_text']
    
    # Champs modifiables directement dans la vue liste
    list_editable = ['is_feature']

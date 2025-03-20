from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

# Modèle pour les catégories de produits
class Category(models.Model):
    # Champs de base
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # URL conviviale
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Image")
    
    # Champs de suivi temporel
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    # Champs de statut
    is_active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']  # Tri par nom par défaut

    def __str__(self):
        """Représentation textuelle de l'objet"""
        return self.name

    def save(self, *args, **kwargs):
        """Surcharge de la méthode save pour générer automatiquement le slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Retourne l'URL absolue de la catégorie"""
        return reverse('products:category_detail', args=[self.slug])

# Modèle pour les produits
class Product(models.Model):
    # Informations de base
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # URL conviviale
    description = models.TextField(verbose_name="Description")
    
    # Informations commerciales
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix remisé")
    
    # Relations et médias
    image = models.ImageField(upload_to='products/', verbose_name="Image principale")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Catégorie")
    
    # Champs de suivi temporel
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    # Champs de statut
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_featured = models.BooleanField(default=False, verbose_name="Mis en avant")
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']  # Tri par date de création décroissante

    def __str__(self):
        """Représentation textuelle de l'objet"""
        return self.name

    def save(self, *args, **kwargs):
        """Surcharge de la méthode save pour générer automatiquement le slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Retourne l'URL absolue du produit"""
        return reverse('products:product_detail', args=[self.slug])

    @property
    def get_discount_percentage(self):
        """Calcule le pourcentage de réduction si un prix remisé existe"""
        if self.discount_price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount)
        return 0

# Modèle pour les images supplémentaires des produits
class ProductImage(models.Model):
    # Relations et médias
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Produit")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Image")
    
    # Informations sur l'image
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Texte alternatif")
    is_feature = models.BooleanField(default=False, verbose_name="Image principale")
    
    # Champ de suivi temporel
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image du produit"
        verbose_name_plural = "Images des produits"
        ordering = ['-is_feature', 'created_at']  # Tri par image principale puis date

    def __str__(self):
        """Représentation textuelle de l'objet"""
        return f"Image de {self.product.name}"




# Rapport du Projet E-commerce

## Table des matières
1. Prérequis
2. Installation de l'environnement
3. Création du projet Django
4. Configuration du projet
5. Développement des fonctionnalités
6. Tests et déploiement

## 1. Prérequis

### 1.1 Installation de Python
- **Windows**:
  ```bash
  # Télécharger Python 3.9+ depuis python.org
  # OU via winget
  winget install Python.Python.3.9
  ```

### 1.2 Installation de PostgreSQL
```bash
# Windows
winget install PostgreSQL.PostgreSQL 

# Création de la base de données via pgadmin4
psql -U admin
CREATE DATABASE e-mpj;
CREATE USER admin WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE e-mpj TO admin;
```

## 2. Installation de l'environnement

### 2.1 Création du dossier projet
```bash
mkdir ecommerce_project
cd ecommerce_project
```

### 2.2 Création de l'environnement virtuel
```bash
python -m venv env

# Activation (Windows)
.\env\Scripts\activate



### 2.3 Installation des dépendances de base
```bash
pip install django==4.2.0
pip install djangorestframework==3.14.0
pip install psycopg2-binary==2.9.5
pip install python-dotenv==1.0.0
pip install Pillow==9.4.0

```

## 3. Création du projet Django

### 3.1 Initialisation du projet Django
```bash
django-admin startproject ecommerce .
```

### 3.2 Création des applications
```bash
python manage.py startapp core
python manage.py startapp products
python manage.py startapp cart
python manage.py startapp users
```

### 3.3 Structure du projet résultante
```
ecommerce_project/
├── ecommerce/           # Configuration principale
│   ├── __init__.py
│   ├── settings.py      # Paramètres du projet
│   ├── urls.py         # URLs principales
│   └── wsgi.py         # Configuration WSGI
├── core/               # Application principale
├── products/          # Gestion des produits
├── cart/              # Gestion du panier
├── users/             # Gestion des utilisateurs
├── templates/         # Templates HTML
├── static/            # Fichiers statiques
├── media/            # Fichiers uploadés
├── manage.py         # Script de gestion
└── requirements.txt   # Dépendances
```

## 4. Configuration du projet

### 4.1 Configuration de la base de données (settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce',
        'USER': 'ecommerce_user',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4.2 Configuration des applications (settings.py)
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Applications tierces
    'rest_framework',
    'corsheaders',
    
    # Applications locales
    'core',
    'products',
    'cart',
    'users',
]
```

### 4.3 Configuration des fichiers statiques et médias
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 5. Développement des fonctionnalités

### 5.1 Création des modèles

#### 5.1.1 Products (products/models.py)
```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

### 5.2 Création des vues

#### 5.2.1 Products (products/views.py)
```python
from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

### 5.3 Configuration des URLs

#### 5.3.1 URLs principales (ecommerce/urls.py)
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('api/', include('cart.urls')),
    path('api/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 6. Tests et déploiement

### 6.1 Création des migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6.2 Création d'un superutilisateur
```bash
python manage.py createsuperuser
```

### 6.3 Lancement du serveur de développement
```bash
python manage.py runserver
```

### 6.4 Tests

#### 6.4.1 Tests unitaires (products/tests.py)
```python
from django.test import TestCase
from .models import Product, Category

class ProductTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=99.99,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 99.99)
```

### 6.5 Déploiement en production

#### 6.5.1 Configuration de production (settings.py)
```python
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com']

# Sécurité
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### 6.5.2 Installation de Gunicorn
```bash
pip install gunicorn
```

#### 6.5.3 Lancement en production
```bash
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
```

## 7. Maintenance

### 7.1 Sauvegarde de la base de données
```bash
pg_dump ecommerce > backup.sql
```

### 7.2 Mise à jour des dépendances
```bash
pip freeze > requirements.txt
pip install -r requirements.txt --upgrade
```

### 7.3 Configuration des logs
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## 8. Bonnes pratiques

### 8.1 Sécurité
- Utilisation de variables d'environnement
- Protection contre les attaques CSRF
- Validation des données utilisateur
- Gestion sécurisée des mots de passe

### 8.2 Performance
- Mise en cache des requêtes fréquentes
- Optimisation des requêtes de base de données
- Compression des fichiers statiques
- Utilisation de CDN pour les fichiers statiques

### 8.3 Code
- Respect des conventions PEP 8
- Documentation du code
- Tests unitaires et d'intégration
- Revue de code régulière
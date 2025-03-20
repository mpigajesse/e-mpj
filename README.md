# E-Commerce Django Project

## Description
Projet e-commerce développé avec Django, offrant une plateforme complète de vente en ligne avec gestion des produits, panier d'achat, et système de paiement.

## Fonctionnalités

- 🛍️ Gestion des produits
- 🛒 Panier d'achat
- 👤 Authentification des utilisateurs (avec support OAuth)
- 💳 Système de paiement
- 📱 Interface responsive
- 🔍 Recherche de produits
- 🏷️ Gestion des catégories
- 📦 Suivi des commandes
- 🌍 Support multilingue
- 🔄 Tâches asynchrones avec Celery
- 📊 Monitoring avec Flower

## Technologies Utilisées

- Django 5.1.7
- Python 3.9+
- PostgreSQL / MySQL (support des deux bases de données)
- Django REST Framework 3.14+
- Celery 5.3.6
- Redis 5.0.1
- JWT Authentication
- Bootstrap 5

## Installation

1. Cloner le projet
```bash
git clone git@github.com:mpigajesse/e-mpj.git
cd e-mpj
```

2. Créer l'environnement virtuel
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# ou
.\env\Scripts\activate  # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement
```bash
# Créer un fichier .env à la racine du projet avec :
DEBUG=True
SECRET_KEY=votre_clé_secrète
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# ou
DATABASE_URL=mysql://user:password@localhost:3306/dbname
REDIS_URL=redis://localhost:6379/0
```

5. Appliquer les migrations
```bash
python manage.py migrate
```

6. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

7. Lancer les services
```bash
# Terminal 1 : Serveur Django
python manage.py runserver

# Terminal 2 : Celery Worker
celery -A ecommerce worker -l info

# Terminal 3 : Flower (monitoring Celery)
celery -A ecommerce flower
```

## Structure du Projet

```
ecommerce_project/
├── ecommerce/           # Configuration principale
├── env/                # Environnement virtuel
└── requirements.txt    # Dépendances du projet
```

## Dépendances Principales

- djangorestframework : API REST
- django-environ & python-dotenv : Gestion des variables d'environnement
- Pillow : Manipulation des images
- django-allauth : Authentification sociale
- djangorestframework-simplejwt : Authentification JWT
- django-cors-headers : Gestion des CORS
- whitenoise : Gestion des fichiers statiques
- celery & flower : Tâches asynchrones et monitoring
- Babel & django-modeltranslation : Internationalisation

## Tests

```bash
# Lancer les tests avec pytest
pytest

# Avec couverture de code
coverage run -m pytest
coverage report
```

## Déploiement

1. Configurer les variables d'environnement de production
2. Collecter les fichiers statiques
```bash
python manage.py collectstatic
```
3. Configurer le serveur web (Nginx/Apache)
4. Configurer Gunicorn
5. Configurer SSL
6. Configurer Redis et Celery

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/NouvelleFeature`)
3. Commit les changements (`git commit -m 'Ajout de NouvelleFeature'`)
4. Push vers la branche (`git push origin feature/NouvelleFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE.md](LICENSE.md) pour plus de détails.

## Contact

Jesse MPIGA - mpigajesse@gmail.com

Lien du projet: [https://github.com/mpigajesse/e-mpj](https://github.com/mpigajesse/e-mpj) 
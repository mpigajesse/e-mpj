# E-Commerce Django Project

## Description
Projet e-commerce développé avec Django, offrant une plateforme complète de vente en ligne avec gestion des produits, panier d'achat, et système de paiement.

## Fonctionnalités

- 🛍️ Gestion des produits
- 🛒 Panier d'achat
- 👤 Authentification des utilisateurs
- 💳 Système de paiement
- 📱 Interface responsive
- 🔍 Recherche de produits
- 🏷️ Gestion des catégories
- 📦 Suivi des commandes

## Technologies Utilisées

- Django 4.2.0
- Python 3.9+
- PostgreSQL
- Django REST Framework
- Celery
- Redis
- HTML/CSS/JavaScript
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

4. Configurer la base de données
```bash
# Créer un fichier .env à la racine du projet avec :
DEBUG=True
SECRET_KEY=votre_clé_secrète
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

5. Appliquer les migrations
```bash
python manage.py migrate
```

6. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

7. Lancer le serveur
```bash
python manage.py runserver
```

## Structure du Projet

```
ecommerce_project/
├── ecommerce/           # Configuration principale
│   ├── core/           # Fonctionnalités principales
│   ├── products/       # Gestion des produits
│   ├── cart/          # Gestion du panier
│   ├── users/         # Gestion des utilisateurs
│   ├── orders/        # Gestion des commandes
│   └── payments/      # Gestion des paiements
├── static/            # Fichiers statiques
├── media/            # Fichiers uploadés
├── templates/        # Templates HTML
└── requirements.txt  # Dépendances
```

## API Endpoints

- `/api/products/` - Liste des produits
- `/api/categories/` - Liste des catégories
- `/api/cart/` - Gestion du panier
- `/api/orders/` - Gestion des commandes
- `/api/users/` - Gestion des utilisateurs

## Tests

```bash
# Lancer les tests
python manage.py test

# Avec couverture de code
coverage run manage.py test
coverage report
```

## Déploiement

1. Configurer les variables d'environnement
2. Collecter les fichiers statiques
```bash
python manage.py collectstatic
```
3. Configurer le serveur web (Nginx/Apache)
4. Configurer Gunicorn
5. Configurer SSL

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE.md](LICENSE.md) pour plus de détails.

## Contact

Jesse MPIGA - mpigajesse@gmail.com

Lien du projet: [https://github.com/mpigajesse/e-mpj](https://github.com/mpigajesse/e-mpj) 
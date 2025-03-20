import os
import sys
import django
from pathlib import Path

# Obtenir le chemin absolu du répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from products.models import Category, Product, ProductImage
from django.db import transaction

def clear_database():
    """
    Vide toutes les tables de la base de données liées aux produits
    """
    try:
        with transaction.atomic():
            # Supprimer d'abord les images des produits
            ProductImage.objects.all().delete()
            print("✓ Les images des produits ont été supprimées")

            # Supprimer les produits
            Product.objects.all().delete()
            print("✓ Les produits ont été supprimés")

            # Supprimer les catégories
            Category.objects.all().delete()
            print("✓ Les catégories ont été supprimées")

            print("\n✨ La base de données a été vidée avec succès!")

    except Exception as e:
        print(f"\n❌ Une erreur est survenue lors de la suppression des données : {str(e)}")

if __name__ == '__main__':
    # Demander confirmation avant de vider la base de données
    confirmation = input("⚠️  Attention! Vous êtes sur le point de vider toutes les tables de la base de données. "
                      "Cette action est irréversible.\nÊtes-vous sûr de vouloir continuer ? (oui/non) : ")
    
    if confirmation.lower() == 'oui':
        clear_database()
    else:
        print("\n🛑 Opération annulée. Aucune donnée n'a été supprimée.")

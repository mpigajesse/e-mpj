import os
import sys
import django
import requests
import shutil
from pathlib import Path

# Ajout du chemin du projet au PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.core.files import File
from products.models import Category, Product, ProductImage

# Créer le dossier images s'il n'existe pas
IMAGES_DIR = Path(__file__).parent / 'images'
IMAGES_DIR.mkdir(exist_ok=True)

def download_image(url, category_name=None, product_name=None, is_gallery=False, gallery_index=None):
    """Télécharge une image depuis une URL et la sauvegarde localement"""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Construire le nom du fichier
            if category_name:
                filename = f"category_{category_name.lower().replace(' ', '_')}.jpg"
            elif product_name:
                if is_gallery:
                    filename = f"gallery_{product_name.lower().replace(' ', '_')}_{gallery_index}.jpg"
                else:
                    filename = f"product_{product_name.lower().replace(' ', '_')}.jpg"
            
            # Chemin complet du fichier
            file_path = IMAGES_DIR / filename
            
            # Sauvegarder l'image localement
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            
            # Retourner le fichier pour Django
            return file_path
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image {url}: {str(e)}")
    return None

def create_category(name, description, image_url):
    """Crée une catégorie avec une image téléchargée"""
    try:
        category = Category.objects.get(name=name)
        print(f"La catégorie {name} existe déjà")
    except Category.DoesNotExist:
        try:
            category = Category(name=name, description=description)
            if image_url:
                image_path = download_image(image_url, category_name=name)
                if image_path:
                    with open(image_path, 'rb') as img_file:
                        category.image.save(image_path.name, File(img_file), save=True)
            category.save()
            print(f"Catégorie {name} créée avec succès")
        except Exception as e:
            print(f"Erreur lors de la création de la catégorie {name}: {str(e)}")
            return None
    return category

def create_product(name, description, price, stock, category, main_image_url, gallery_images=[]):
    """Crée un produit avec ses images"""
    try:
        product = Product.objects.get(name=name)
        print(f"Le produit {name} existe déjà")
    except Product.DoesNotExist:
        try:
            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                category=category
            )
            
            # Image principale
            if main_image_url:
                image_path = download_image(main_image_url, product_name=name)
                if image_path:
                    with open(image_path, 'rb') as img_file:
                        product.image.save(image_path.name, File(img_file), save=True)
            
            product.save()
            
            # Images de la galerie
            for idx, gallery_url in enumerate(gallery_images):
                image_path = download_image(gallery_url, product_name=name, is_gallery=True, gallery_index=idx+1)
                if image_path:
                    product_image = ProductImage(
                        product=product,
                        alt_text=f"Image {idx+1} pour {name}",
                        is_feature=(idx == 0)
                    )
                    with open(image_path, 'rb') as img_file:
                        product_image.image.save(image_path.name, File(img_file), save=True)
                    product_image.save()
            
            print(f"Produit {name} créé avec succès")
        except Exception as e:
            print(f"Erreur lors de la création du produit {name}: {str(e)}")
            return None
    return product

def populate_database():
    """Fonction principale pour peupler la base de données"""
    print("Début de la population de la base de données...")
    
    # Catégories avec leurs images Unsplash
    categories_data = [
        {
            'name': 'Électronique',
            'description': 'Produits électroniques et gadgets innovants pour tous vos besoins technologiques',
            'image_url': 'https://images.unsplash.com/photo-1498049794561-7780e7231661'
        },
        {
            'name': 'Mode',
            'description': 'Vêtements et accessoires tendance pour homme et femme',
            'image_url': 'https://images.unsplash.com/photo-1445205170230-053b83016050'
        },
        {
            'name': 'Maison',
            'description': 'Décoration et ameublement pour un intérieur chaleureux',
            'image_url': 'https://images.unsplash.com/photo-1484101403633-562f891dc89a'
        },
        {
            'name': 'Sport',
            'description': 'Équipements et accessoires pour tous les sports',
            'image_url': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211'
        },
        {
            'name': 'École',
            'description': 'Tout le nécessaire pour la rentrée et l\'année scolaire',
            'image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b'
        },
        {
            'name': 'Cuisine',
            'description': 'Ustensiles et équipements pour une cuisine professionnelle',
            'image_url': 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f'
        }
    ]

    # Création des catégories
    categories = {}
    for cat_data in categories_data:
        category = create_category(
            cat_data['name'],
            cat_data['description'],
            cat_data['image_url']
        )
        if category:
            categories[cat_data['name']] = category

    # Produits pour chaque catégorie
    products_data = {
        'Électronique': [
            {
                'name': 'Smartphone XYZ Pro',
                'description': 'Smartphone haut de gamme avec écran 6.7" et processeur dernière génération',
                'price': 999.99,
            'stock': 50,
            'main_image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9',
                'gallery': ['https://images.unsplash.com/photo-1565849904461-04a58ad377e0']
            },
            {
                'name': 'Laptop Ultra',
                'description': 'Ordinateur portable ultra-fin avec 16GB RAM et SSD 512GB',
                'price': 1299.99,
                'stock': 30,
                'main_image': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853',
                'gallery': ['https://images.unsplash.com/photo-1498050108023-c5249f4df085']
            },
            {
                'name': 'Tablette Pro',
                'description': 'Tablette 10" parfaite pour les créatifs',
                'price': 599.99,
                'stock': 40,
                'main_image': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0',
                'gallery': ['https://images.unsplash.com/photo-1537498425277-c283d32ef9db']
            },
            {
                'name': 'Écouteurs Sans Fil',
                'description': 'Écouteurs bluetooth avec réduction de bruit active',
            'price': 199.99,
                'stock': 100,
                'main_image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e',
                'gallery': ['https://images.unsplash.com/photo-1484704849700-f032a568e944']
            },
            {
                'name': 'Montre Connectée',
                'description': 'Montre intelligente avec suivi d\'activité',
                'price': 299.99,
                'stock': 60,
                'main_image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30',
                'gallery': ['https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1']
            },
            {
                'name': 'Enceinte Bluetooth',
                'description': 'Enceinte portable waterproof',
                'price': 129.99,
                'stock': 45,
                'main_image': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1',
                'gallery': ['https://images.unsplash.com/photo-1545454675-3531b543be5d']
            },
            {
                'name': 'Appareil Photo Pro',
                'description': 'Appareil photo mirrorless 24MP',
                'price': 1499.99,
                'stock': 20,
                'main_image': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32',
                'gallery': ['https://images.unsplash.com/photo-1502982720700-bfff97f2ecac']
            },
            {
                'name': 'Drone 4K',
                'description': 'Drone avec caméra 4K et stabilisation',
                'price': 799.99,
                'stock': 15,
                'main_image': 'https://images.unsplash.com/photo-1507582020474-9a35b7d455d9',
                'gallery': ['https://images.unsplash.com/photo-1473968512647-3e447244af8f']
            },
            {
                'name': 'Console de Jeux',
                'description': 'Console de jeux dernière génération',
                'price': 499.99,
                'stock': 25,
                'main_image': 'https://images.unsplash.com/photo-1486401899868-0e435ed85128',
                'gallery': ['https://images.unsplash.com/photo-1493711662062-fa541adb3fc8']
            },
            {
                'name': 'Projecteur HD',
                'description': 'Projecteur home cinéma Full HD',
                'price': 699.99,
                'stock': 10,
                'main_image': 'https://images.unsplash.com/photo-1478720568477-152d9b164e26',
                'gallery': ['https://images.unsplash.com/photo-1489599849927-2ee91cede3ba']
            }
        ],
        'Mode': [
            {
                'name': 'Sac à Main Luxe',
                'description': 'Sac à main en cuir véritable italien',
                'price': 299.99,
            'stock': 30,
            'main_image': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3',
                'gallery': ['https://images.unsplash.com/photo-1591561954557-26941169b49e']
            },
            {
                'name': 'Montre Élégante',
                'description': 'Montre analogique en acier inoxydable',
                'price': 199.99,
                'stock': 40,
                'main_image': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314',
                'gallery': ['https://images.unsplash.com/photo-1533139502658-0198f920d8e8']
            },
            {
                'name': 'Blazer Classique',
                'description': 'Blazer noir coupe ajustée',
                'price': 159.99,
                'stock': 25,
                'main_image': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf',
                'gallery': ['https://images.unsplash.com/photo-1598033129183-c4f50c736f10']
            },
            {
                'name': 'Robe de Soirée',
                'description': 'Robe longue élégante',
                'price': 249.99,
                'stock': 20,
                'main_image': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1',
                'gallery': ['https://images.unsplash.com/photo-1595777457583-95e059d581b8']
            },
            {
                'name': 'Chaussures Cuir',
                'description': 'Chaussures en cuir italien fait main',
                'price': 179.99,
                'stock': 35,
                'main_image': 'https://images.unsplash.com/photo-1449505278894-297fdb3edbc1',
                'gallery': ['https://images.unsplash.com/photo-1543163521-1bf539c55dd2']
            },
            {
                'name': 'Ceinture Designer',
                'description': 'Ceinture en cuir avec boucle design',
            'price': 89.99,
                'stock': 50,
                'main_image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62',
                'gallery': ['https://images.unsplash.com/photo-1624222247344-550fb60583dc']
            },
            {
                'name': 'Lunettes Soleil',
                'description': 'Lunettes de soleil polarisées',
                'price': 129.99,
                'stock': 45,
                'main_image': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083',
                'gallery': ['https://images.unsplash.com/photo-1473496169904-658ba7c44d8a']
            },
            {
                'name': 'Écharpe Luxe',
                'description': 'Écharpe en cachemire',
                'price': 149.99,
                'stock': 30,
                'main_image': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f',
                'gallery': ['https://images.unsplash.com/photo-1520903920243-00d872a2d1c9']
            },
            {
                'name': 'Portefeuille Cuir',
                'description': 'Portefeuille en cuir véritable',
                'price': 79.99,
                'stock': 60,
                'main_image': 'https://images.unsplash.com/photo-1627123424574-724758594e93',
                'gallery': ['https://images.unsplash.com/photo-1606503825008-909a67e63c3d']
            },
            {
                'name': 'Chapeau Fedora',
                'description': 'Chapeau fedora en feutre',
                'price': 69.99,
                'stock': 25,
                'main_image': 'https://images.unsplash.com/photo-1514327605112-b887c0e61c0a',
                'gallery': ['https://images.unsplash.com/photo-1521369909029-2afed882baee']
            }
        ],
        'Maison': [
            {
                'name': 'Lampe Design',
                'description': 'Lampe de table moderne',
                'price': 129.99,
                'stock': 40,
                'main_image': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c',
                'gallery': ['https://images.unsplash.com/photo-1513506003901-1e6a229e2d15']
            },
            {
                'name': 'Canapé Confort',
                'description': 'Canapé 3 places en tissu',
                'price': 899.99,
                'stock': 10,
                'main_image': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc',
                'gallery': ['https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e']
            },
            {
                'name': 'Table Basse',
                'description': 'Table basse en bois massif',
                'price': 299.99,
                'stock': 15,
                'main_image': 'https://images.unsplash.com/photo-1533090161767-e6ffed986c88',
                'gallery': ['https://images.unsplash.com/photo-1532372576444-dda954194ad0']
            },
            {
                'name': 'Tapis Design',
                'description': 'Tapis moderne 160x230cm',
                'price': 199.99,
            'stock': 20,
                'main_image': 'https://images.unsplash.com/photo-1575414003591-ece8d0416c7a',
                'gallery': ['https://images.unsplash.com/photo-1531985664928-7b15ddd6f12d']
            },
            {
                'name': 'Miroir Mural',
                'description': 'Miroir décoratif rond',
                'price': 149.99,
                'stock': 25,
                'main_image': 'https://images.unsplash.com/photo-1618220179428-22790b461013',
                'gallery': ['https://images.unsplash.com/photo-1616046229478-9901c5536a45']
            },
            {
                'name': 'Vase Décoratif',
                'description': 'Vase en céramique fait main',
                'price': 79.99,
                'stock': 30,
                'main_image': 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d',
                'gallery': ['https://images.unsplash.com/photo-1581783898377-1c85bf937427']
            },
            {
                'name': 'Coussin Design',
                'description': 'Coussin décoratif 45x45cm',
                'price': 39.99,
                'stock': 50,
                'main_image': 'https://images.unsplash.com/photo-1592078615290-033ee584e267',
                'gallery': ['https://images.unsplash.com/photo-1616627451515-cbc80e5ece35']
            },
            {
                'name': 'Horloge Murale',
                'description': 'Horloge design silencieuse',
                'price': 59.99,
                'stock': 35,
                'main_image': 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c',
                'gallery': ['https://images.unsplash.com/photo-1592283763920-0c13ee14b1fd']
            },
            {
                'name': 'Étagère Murale',
                'description': 'Étagère flottante en bois',
                'price': 89.99,
                'stock': 25,
                'main_image': 'https://images.unsplash.com/photo-1597072689227-8882273e8f6a',
                'gallery': ['https://images.unsplash.com/photo-1593085260707-5377ba37f868']
            },
            {
                'name': 'Plante Artificielle',
                'description': 'Plante décorative réaliste',
                'price': 49.99,
                'stock': 40,
                'main_image': 'https://images.unsplash.com/photo-1485955900006-10f4d324d411',
                'gallery': ['https://images.unsplash.com/photo-1509423350716-97f9360b4e09']
            }
        ],
        'Sport': [
            {
                'name': 'Tapis de Yoga',
                'description': 'Tapis antidérapant premium',
                'price': 49.99,
                'stock': 100,
                'main_image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b',
                'gallery': ['https://images.unsplash.com/photo-1518611012118-696072aa579a']
            },
            {
                'name': 'Haltères 5kg',
                'description': 'Paire d\'haltères en fonte',
                'price': 39.99,
                'stock': 50,
                'main_image': 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61',
                'gallery': ['https://images.unsplash.com/photo-1534438327276-14e5300c3a48']
            },
            {
                'name': 'Ballon Fitness',
                'description': 'Ballon de gym anti-éclatement',
                'price': 29.99,
                'stock': 40,
                'main_image': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2',
                'gallery': ['https://images.unsplash.com/photo-1518310383802-640c2de311b2']
            },
            {
                'name': 'Corde à Sauter Pro',
                'description': 'Corde à sauter réglable',
                'price': 19.99,
                'stock': 75,
                'main_image': 'https://images.unsplash.com/photo-1515775538093-d2d95c5ee4f4',
                'gallery': ['https://images.unsplash.com/photo-1434596922112-19c563067271']
            },
            {
                'name': 'Sac de Sport',
                'description': 'Sac de sport spacieux',
                'price': 59.99,
                'stock': 30,
                'main_image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a45',
                'gallery': ['https://images.unsplash.com/photo-1519763421920-f2d769e01a37']
            },
            {
                'name': 'Bandes Élastiques',
                'description': 'Set de 5 bandes de résistance',
                'price': 24.99,
                'stock': 60,
                'main_image': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc',
                'gallery': ['https://images.unsplash.com/photo-1518622358385-8ea7d0794bf6']
            },
            {
                'name': 'Gourde Sport',
                'description': 'Gourde isotherme 750ml',
                'price': 29.99,
                'stock': 100,
                'main_image': 'https://images.unsplash.com/photo-1523362628745-0c100150b504',
                'gallery': ['https://images.unsplash.com/photo-1550505095-81378a674395']
            },
            {
                'name': 'Tenue Fitness',
                'description': 'Ensemble sport respirant',
                'price': 79.99,
                'stock': 45,
                'main_image': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2',
                'gallery': ['https://images.unsplash.com/photo-1518310383802-640c2de311b2']
            },
            {
                'name': 'Montre Sport',
                'description': 'Montre cardio GPS',
                'price': 199.99,
                'stock': 25,
                'main_image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30',
                'gallery': ['https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1']
            },
            {
                'name': 'Tapis Course',
                'description': 'Tapis de course pliable',
                'price': 699.99,
                'stock': 10,
                'main_image': 'https://images.unsplash.com/photo-1540497077202-7c8a3999166f',
                'gallery': ['https://images.unsplash.com/photo-1517963879433-6ad2b056d712']
            }
        ],
        'École': [
            {
                'name': 'Sac à Dos Ergonomique',
                'description': 'Sac à dos confortable avec multiples compartiments et support dorsal renforcé',
                'price': 49.99,
                'stock': 100,
                'main_image': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a45',
                'gallery': ['https://images.unsplash.com/photo-1553062407-98eeb64c6a46']
            },
            {
                'name': 'Trousse Complète',
                'description': 'Trousse garnie avec stylos, crayons, gomme et règle',
                'price': 29.99,
                'stock': 150,
                'main_image': 'https://images.unsplash.com/photo-1558959356-2d0602a3e6ee',
                'gallery': ['https://images.unsplash.com/photo-1558959356-2d0602a3e6ef']
            },
            {
                'name': 'Cahiers Premium',
                'description': 'Lot de 5 cahiers grands carreaux 96 pages',
                'price': 15.99,
                'stock': 200,
                'main_image': 'https://images.unsplash.com/photo-1531346878377-a5be20888e57',
                'gallery': ['https://images.unsplash.com/photo-1531346878377-a5be20888e58']
            },
            {
                'name': 'Calculatrice Scientifique',
                'description': 'Calculatrice avec fonctions scientifiques avancées',
                'price': 39.99,
                'stock': 80,
                'main_image': 'https://images.unsplash.com/photo-1574607383476-f517f260d30b',
                'gallery': ['https://images.unsplash.com/photo-1574607383476-f517f260d30c']
            },
            {
                'name': 'Set Géométrie',
                'description': 'Kit complet avec règle, équerre, rapporteur et compas',
                'price': 19.99,
                'stock': 120,
                'main_image': 'https://images.unsplash.com/photo-1519414442781-fbd745c5b497',
                'gallery': ['https://images.unsplash.com/photo-1519414442781-fbd745c5b498']
            },
            {
                'name': 'Agenda Scolaire',
                'description': 'Agenda avec planning hebdomadaire et mensuel',
                'price': 24.99,
                'stock': 90,
                'main_image': 'https://images.unsplash.com/photo-1506784365847-bbad939e9335',
                'gallery': ['https://images.unsplash.com/photo-1506784365847-bbad939e9336']
            },
            {
                'name': 'Classeur A4',
                'description': 'Classeur robuste avec anneaux et intercalaires',
                'price': 12.99,
                'stock': 160,
                'main_image': 'https://images.unsplash.com/photo-1586075010923-2dd4570fb338',
                'gallery': ['https://images.unsplash.com/photo-1586075010923-2dd4570fb339']
            },
            {
                'name': 'Pochette Art',
                'description': 'Set complet pour artiste avec crayons et pastels',
                'price': 34.99,
                'stock': 70,
                'main_image': 'https://images.unsplash.com/photo-1513364776144-60967b0f800f',
                'gallery': ['https://images.unsplash.com/photo-1513364776144-60967b0f800e']
            },
            {
                'name': 'Dictionnaire Premium',
                'description': 'Dictionnaire complet avec annexes et conjugaisons',
                'price': 29.99,
                'stock': 85,
                'main_image': 'https://images.unsplash.com/photo-1589998059171-988d887df646',
                'gallery': ['https://images.unsplash.com/photo-1589998059171-988d887df647']
            },
            {
                'name': 'Globe Terrestre',
                'description': 'Globe terrestre lumineux avec support',
                'price': 45.99,
                'stock': 40,
                'main_image': 'https://images.unsplash.com/photo-1576877438539-c73c101d41de',
                'gallery': ['https://images.unsplash.com/photo-1576877438539-c73c101d41df']
            }
        ],
        'Cuisine': [
            {
                'name': 'Robot Culinaire Pro',
                'description': 'Robot multifonction 1000W avec 10 accessoires',
                'price': 299.99,
                'stock': 50,
                'main_image': 'https://images.unsplash.com/photo-1570222094114-d054a817e56b',
                'gallery': ['https://images.unsplash.com/photo-1570222094114-d054a817e56c']
            },
            {
                'name': 'Set de Couteaux',
                'description': 'Set de 6 couteaux professionnels en acier inoxydable',
                'price': 199.99,
                'stock': 75,
                'main_image': 'https://images.unsplash.com/photo-1593618998160-e34014e67546',
                'gallery': ['https://images.unsplash.com/photo-1593618998160-e34014e67547']
            },
            {
                'name': 'Batterie de Cuisine',
                'description': 'Set complet de casseroles et poêles antiadhésives',
                'price': 249.99,
                'stock': 45,
                'main_image': 'https://images.unsplash.com/photo-1584990347449-716dc4a26833',
                'gallery': ['https://images.unsplash.com/photo-1584990347449-716dc4a26834']
            },
            {
                'name': 'Machine à Pâtes',
                'description': 'Machine à pâtes manuelle en acier inoxydable',
                'price': 89.99,
                'stock': 60,
                'main_image': 'https://images.unsplash.com/photo-1591985666643-1ecc67616216',
                'gallery': ['https://images.unsplash.com/photo-1591985666643-1ecc67616217']
            },
            {
                'name': 'Balance Digitale',
                'description': 'Balance de cuisine précise avec bol',
                'price': 34.99,
                'stock': 100,
                'main_image': 'https://images.unsplash.com/photo-1591261730799-ee4e6c2d16d7',
                'gallery': ['https://images.unsplash.com/photo-1591261730799-ee4e6c2d16d8']
            },
            {
                'name': 'Planche à Découper',
                'description': 'Planche en bois massif avec rainures',
                'price': 45.99,
                'stock': 85,
                'main_image': 'https://images.unsplash.com/photo-1576866209830-589e1bfbaa4d',
                'gallery': ['https://images.unsplash.com/photo-1576866209830-589e1bfbaa4e']
            },
            {
                'name': 'Mixeur Plongeant',
                'description': 'Mixeur 800W avec accessoires',
                'price': 79.99,
                'stock': 70,
                'main_image': 'https://images.unsplash.com/photo-1578653816054-62b6e5f43755',
                'gallery': ['https://images.unsplash.com/photo-1578653816054-62b6e5f43756']
            },
            {
                'name': 'Four à Pizza',
                'description': 'Four spécial pizza avec pierre réfractaire',
                'price': 159.99,
                'stock': 30,
                'main_image': 'https://images.unsplash.com/photo-1600628421055-4d30de868b8f',
                'gallery': ['https://images.unsplash.com/photo-1600628421055-4d30de868b8e']
            },
            {
                'name': 'Moules Pâtisserie',
                'description': 'Set complet de moules pour pâtisserie',
                'price': 69.99,
                'stock': 90,
                'main_image': 'https://images.unsplash.com/photo-1621236378699-8597faf6a176',
                'gallery': ['https://images.unsplash.com/photo-1621236378699-8597faf6a177']
            },
            {
                'name': 'Machine à Café Pro',
                'description': 'Machine à café expresso automatique',
                'price': 399.99,
                'stock': 25,
                'main_image': 'https://images.unsplash.com/photo-1587080413959-06b859fb107d',
                'gallery': ['https://images.unsplash.com/photo-1587080413959-06b859fb107e']
            }
        ]
    }

    # Création des produits pour chaque catégorie
    for category_name, products in products_data.items():
        if category_name in categories:
            for product in products:
             create_product(
                    name=product['name'],
                    description=product['description'],
                    price=product['price'],
                    stock=product['stock'],
                    category=categories[category_name],
                    main_image_url=product['main_image'],
                    gallery_images=product['gallery']
            )
        else:
            print(f"La catégorie {category_name} n'existe pas")

if __name__ == '__main__':
    print("Initialisation du script...")
    populate_database()
    print("Population de la base de données terminée !") 
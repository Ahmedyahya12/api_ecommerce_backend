import os
import django
from django.core.files import File

# Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerceApiProject.settings")  # Remplace par ton settings
django.setup()

from apiApp.models import Category, Product  # Remplace 'myapp' par le nom de ton application

# Chemin de base des images
BASE_IMG_PATH = r'D:\Django_projects\ecommerce-api\media'

# Données des catégories et produits
categories_data = {
    "Food": [
        ("Pizza", "Delicious cheese pizza", 12.50, "product_img/pizza.jpg"),
        ("Burger", "Beef burger with fries", 8.75, "product_img/burger.jpg"),
        ("Pasta", "Italian pasta with sauce", 10.00, "product_img/pasta.jpg"),
        ("Salad", "Fresh vegetable salad", 6.25, "product_img/salad.jpg"),
    ],
    "Electronics": [
        ("Laptop", "15-inch gaming laptop", 1200.00, "product_img/laptop.jpg"),
        ("Phone", "Latest smartphone 128GB", 800.00, "product_img/phone.jpg"),
        ("Headphones", "Noise cancelling headphones", 150.00, "product_img/headphones.jpg"),
        ("Camera", "Digital SLR camera", 600.00, "product_img/camera.jpg"),
    ],
    "Books": [
        ("Novel", "A best-selling fiction novel", 20.00, "product_img/novel.jpg"),
        ("Science Book", "Physics for beginners", 35.00, "product_img/science.jpg"),
        ("History Book", "World history overview", 28.00, "product_img/history.jpg"),
        ("Dictionary", "English-French dictionary", 18.00, "product_img/dictionary.jpg"),
    ],
    "Clothes": [
        ("T-Shirt", "Cotton T-shirt", 15.00, "product_img/tshirt.jpg"),
        ("Jeans", "Slim fit jeans", 40.00, "product_img/jeans.jpg"),
        ("Jacket", "Winter jacket", 85.00, "product_img/jacket.jpg"),
        ("Shoes", "Running shoes", 55.00, "product_img/shoes.jpg"),
    ],
    "Sports": [
        ("Football", "Professional size football", 30.00, "product_img/football.jpg"),
        ("Tennis Racket", "Lightweight tennis racket", 75.00, "product_img/racket.jpg"),
        ("Basketball", "Official NBA basketball", 35.00, "product_img/basketball.jpg"),
        ("Gloves", "Boxing gloves", 25.00, "product_img/gloves.jpg"),
    ],
}

# Création des catégories et produits
for cat_name, products in categories_data.items():
    cat, created = Category.objects.get_or_create(name=cat_name)
    
    for prod_name, description, price, img_rel_path in products:
        prod, created = Product.objects.get_or_create(
            name=prod_name,
            defaults={
                "description": description,
                "price": price,
                "Category": cat
            }
        )
        
        # Ajouter l'image si elle existe
        img_full_path = os.path.join(BASE_IMG_PATH, img_rel_path)
        if os.path.exists(img_full_path):
            with open(img_full_path, 'rb') as f:
                prod.image.save(os.path.basename(img_rel_path), File(f), save=True)

print("Import terminé !")

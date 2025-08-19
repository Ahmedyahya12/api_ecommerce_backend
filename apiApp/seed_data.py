import os
import sys
import django
from django.utils.text import slugify

# Chemin racine du projet
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

# Définir le settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerceApiProject.settings")
django.setup()

from apiApp.models import Category, Product

# Chemin media pour les images
MEDIA_DIR = os.path.join(PROJECT_DIR, "media")

# Données à insérer
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

# Fonction utilitaire pour créer un slug unique
def unique_slug(model, name):
    slug = slugify(name)
    counter = 1
    unique = slug
    while model.objects.filter(slug=unique).exists():
        unique = f"{slug}-{counter}"
        counter += 1
    return unique

def run():
    for cat_name, products in categories_data.items():
        # Crée la catégorie avec slug unique
        category, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={'slug': unique_slug(Category, cat_name)}
        )
        print(f"{'✅' if created else 'ℹ️'} Category: {cat_name}")

        for prod_name, description, price, img_rel_path in products:
            # Chemin complet de l'image dans media
            img_path = os.path.join(MEDIA_DIR, img_rel_path)
            if not os.path.exists(img_path):
                print(f"⚠️ Image not found: {img_path}")
                img_path = None

            # Crée le produit
            product, _ = Product.objects.get_or_create(
                name=prod_name,
                defaults={
                    'description': description,
                    'price': price,
                    'Category': category,
                    'slug': unique_slug(Product, prod_name),
                    'image': img_path
                }
            )
            print(f"   📦 Product: {prod_name}")

    print("🎉 Seed data completed!")

if __name__ == "__main__":
    run()

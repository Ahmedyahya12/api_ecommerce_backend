import os
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from .models import Category, Product   # غيّر shop إلى اسم app عندك

# مسار الصور (عدّل المسار إذا حاب)
BASE_DIR = "D:/Django_projects/ecommerce-api/media/"

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


class Command(BaseCommand):
    help = "Seed database with categories and products"

    def handle(self, *args, **kwargs):
        for category_name, products in categories_data.items():
            category, created = Category.objects.get_or_create(
                name=category_name,
                slug=category_name.lower()
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category created: {category_name}"))

            for name, desc, price, img_path in products:
                product, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        "description": desc,
                        "price": price,
                        "Category": category,
                    }
                )
                if created:
                    full_path = os.path.join(BASE_DIR, img_path)
                    if os.path.exists(full_path):
                        with open(full_path, "rb") as f:
                            product.image = ImageFile(f, name=os.path.basename(full_path))
                            product.save()
                    self.stdout.write(self.style.SUCCESS(f"Product created: {name}"))
                else:
                    self.stdout.write(f"Product already exists: {name}")

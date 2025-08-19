from django.core.files import File
from apiApp.models import Product

# Chemin local vers ton image
file_path = r"D:\Django_projects\ecommerce-api\media\product_img\book.png"

if __name__ == "__main__":   # corrigé : double égal et guillemets
    with open(file_path, "rb") as f:
        django_file = File(f)
        p = Product.objects.create(name="Test")
        p.image.save("book.png", django_file, save=True)

    print("Image uploadée avec succès !")
    print("URL Cloudinary :", p.image.url)

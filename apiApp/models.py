from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    profile_picture_url=models.URLField(blank=True,null=True)
    def __str__(self):
        return self.email

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,blank=True)
    image=models.ImageField(upload_to='category_img',blank=True,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    slug=models.SlugField(null=True,blank=True)
    image=models.ImageField(upload_to="product_img",blank=True,null=True)
    featured=models.BooleanField(default=True)
    Category=models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True,related_name='products')
    
    def save(self,*args, **kwargs):
        if not self.slug :
            self.slug=slugify(self.name)  
            unique_slug=self.slug
            counter=1
            if Product.objects.filter(slug=unique_slug).exists():
                unique_slug=f'{self.slug} -- {counter}'
                counter +=1
            self.slug=unique_slug
        super().save(*args,**kwargs)
          

    def __str__(self):
         return self.name
    
class Cart(models.Model):
    cart_code=models.CharField(unique=True,max_length=11)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.cart_code

class CartItem(models.Model):
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cartitems")
  product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='item')
  quantity=models.PositiveIntegerField(default=1)
  
  def __str__(self):
      return f'{self.quantity} x  {self.product.name} in cart {self.cart.cart_code} '
  

class Review(models.Model):
    RATING_CHOICES = [
    (1, '1 - Poor'),
    (2, '2 - Fair'),
    (3, '3 - Good'),
    (4, '4 - Very Good'),
    (5, '5 - Excellent'),
     ]
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reviews')
    rating=models.PositiveIntegerField(choices=RATING_CHOICES)
    review=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}⭐"
    
    class Meta:
        unique_together=["user","product"]
        ordering=["created"]


class ProductRating(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE,related_name='rating')
    average_rating=models.FloatField(default=0.0)
    total_reviews=models.PositiveIntegerField(default=0)
    
    def __str__(self):
       return f'{self.product.name} - {self.average_rating} ({self.total_reviews} reviews)'


class Wishlist(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wishlist")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="wishlist")
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=["user","product"]
    
    def __str__(self):
        return f'{self.user.username} -{self.product.name}'
    
# ------------------------
# Order
# ------------------------
class Order(models.Model):
    payment_reference = models.CharField(
        max_length=255, blank=True, null=True
    )  # يحل محل stripe_checkout_id كمرجع عام للدفع
    customer_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    currency = models.CharField(max_length=10, default='MRU')  # العملة المحلية
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid")],
        default="Pending"
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[("Cash", "Cash"), ("Bankily", "Bankily")],
        default="Cash"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_email} - {self.status}"
# ------------------------
# OrderItem
# ------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # السعر عند إنشاء الطلب

    def save(self, *args, **kwargs):
   
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
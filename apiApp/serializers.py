from rest_framework import serializers
from django.contrib.auth import get_user_model
from apiApp.models import Cart, CartItem, Category, Product, Review, Wishlist

class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields=["id","name","slug","image","price"]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id","name","slug","description","image","price"]


class CategoryListSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=Category
        fields=['id','name','image','slug']


class CategoryDetailSerializer(serializers.ModelSerializer):
    products=ProductListSerializer(many=True,read_only=True)

    class Meta:
        model=Category
        fields=['id','name','image','products']


class CartItemSerializer(serializers.ModelSerializer):
    product=ProductListSerializer(read_only=True)
    sub_total=serializers.SerializerMethodField()
    class Meta:
        model=CartItem
        fields=["id","product","quantity","sub_total"]

    def get_sub_total(self,cartItem):
         total=cartItem.product.price * cartItem.quantity
         return total

class CartSerializer(serializers.ModelSerializer):
    cartItems=CartItemSerializer(source="cartitems",read_only=True,many=True)
    cart_total=serializers.SerializerMethodField()
    class Meta:
        model=Cart 
        fields=["id","cart_code","cartItems","cart_total"]
    
    def get_cart_total(self,cart):
        items=cart.cartitems.all()
        total=sum([item.quantity * item.product.price for item in items ])
        return total

class CartStatSerializer(serializers.ModelSerializer):
    total_quantity=serializers.SerializerMethodField()
    
    class Meta:
        model=Cart
        fields=["id","cart_code","total_quantity"]

    def get_total_quantity(self,cart):
        items=cart.cartItems.all()
        total=sum([item.quantity * item.product.price for item in items ])
        return total
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=["id","first_name","last_name","profile_picture_url"]

class ReviewSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Review
        fields=["id","user","rating","review","created","updated"]


class WishListSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    product=ProductListSerializer(read_only=True)
    
    class Meta:
        model=Wishlist
        fields=["id","user","product","created"]

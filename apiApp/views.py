
from .models import Cart, Order, OrderItem, Product
from uuid import uuid4
from decimal import Decimal
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from apiApp.models import Cart, CartItem, Category, Product, Review, Wishlist
from django.contrib.auth.models import User
from django.db.models import Q
from apiApp.serializers import (
    CartItemSerializer,
    CartSerializer,
    CategoryDetailSerializer,
    CategoryListSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ReviewSerializer,
    WishListSerializer,
)

User = get_user_model()  

# Create your views here.
@api_view(["GET"])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data)


@api_view(["POST"])
def add_to_cart(request):
    cart_code = request.data.get("cart_code")
    product_id = request.data.get("product_id")

    # الحصول على السلة أو إنشاؤها إذا لم توجد
    cart, created = Cart.objects.get_or_create(cart_code=cart_code)

    # الحصول على المنتج
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Produit introuvable"}, status=404)

    # الحصول على العنصر داخل السلة أو إنشاؤه
    cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)

    if not created:
        # إذا كان موجود من قبل، زِد الكمية
        cartitem.quantity += 1
    else:
        # إذا جديد، خلي الكمية = 1
        cartitem.quantity = 1

    cartitem.save()

    # نرجع السلة كاملة مع العناصر
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["PUT"])
def update_cartitem_quantity(request):
    cartitem_id = request.data.get("item_id")
    quantity = request.data.get("quantity")
    quantity = int(quantity)
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.quantity = quantity
    cartitem.save()

    serializer = CartItemSerializer(cartitem)

    return Response(
        {"data": serializer.data, "message": "Cartitem updated successfully"}
    )


@api_view(["POST"])
def add_review(request):
    try:
        product_id = request.data.get("product_id")
        email = request.data.get("email")
        rating = request.data.get("rating")
        review_text = request.data.get("review")

        # Vérifier que toutes les données sont présentes
        if not product_id or not email or not rating or not review_text:
            return Response({"error": "Veuillez remplir tous les champs requis"}, status=400)

        # Récupérer le produit
        product = Product.objects.get(id=product_id)

        # Récupérer l'utilisateur
        user = User.objects.get(email=email)

        # Créer la review
        review = Review.objects.create(
            product=product,
            user=user,
            rating=rating,
            review=review_text
        )

        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    except Product.DoesNotExist:
        return Response({"error": "Produit introuvable"}, status=404)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur introuvable"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['PUT'])   
def update_review(request,pk):
  review=Review.objects.get(id=pk)
  rating=request.data.get('rating')
  review_text=request.data.get("review")
  review.rating=rating
  review.review=review_text
  review.save()
  serializer=ReviewSerializer(review)
  return Response(serializer.data)


@api_view(['DELETE'])
def delete_review(request,pk):
    review=Review.objects.get(id=pk)
    review.delete()

    return Response("Review deleted successfully",status=204)

@api_view(['DELETE'])
def delete_cartitem(request,pk):
    cartitem=CartItem.objects.get(id=pk)
    cartitem.delete()

    return Response("CartItem deleted successfully",status=204)


@api_view(['POST'])
def add_to_wishlist(request):
    email=request.data.get("email")
    product_id=request.data.get("product_id")

    user=User.objects.get(email=email)
    product=Product.objects.get(id=product_id)

    wishlist=Wishlist.objects.filter(user=user,product=product)
    if wishlist:
        wishlist.delete()
        return Response("Wishlist deleted successfully ",status=204)
    new_wishlist=Wishlist.objects.create(user=user,product=product)
    serializer=WishListSerializer(new_wishlist)
    return Response(serializer.data)

@api_view(['GET'])
def product_search(request):
    query = request.query_params.get("query")
    if not query:
        return Response({'error': 'No query provided'}, status=400)

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(Category__name__icontains=query)  # تأكد من الحرف الكبير في "Category" حسب الموديل
    )

    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)



# ------------------------
# محاكاة جلسة الدفع
# ------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from uuid import uuid4
from .models import Cart


@api_view(['POST'])
def mock_create_checkout_session(request):
    cart_code = request.data.get("cart_code")
    email = request.data.get("email")

    # جلب Cart
    try:
        cart = Cart.objects.get(cart_code=cart_code)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)

    # إنشاء معرف وهمي للجلسة
    checkout_session_id = str(uuid4())

    # حساب المبلغ الإجمالي
    total_amount = sum([item.product.price * item.quantity for item in cart.cartitems.all()])

    # محاكاة الجواب كما لو كانت Stripe
    response = {
        "id": checkout_session_id,
        "customer_email": email,
        "amount_total": float(total_amount),
        "currency": "USD",
        "metadata": {"cart_code": cart_code},
        "status": "mock_pending",
        # روابط إعادة التوجيه للواجهة الأمامية
        "success_url": "https://my-frontend-app.vercel.app/success",
        "cancel_url": "https://my-frontend-app.vercel.app/cancel"
    }

    return Response(response)


# ------------------------
# محاكاة Webhook / الدفع ناجح
# ------------------------

@api_view(['POST'])
def mock_webhook_payment_success(request):
    """
    هذا endpoint يحاكي Webhook من Stripe عند نجاح الدفع
    """
    session = request.data  # يجب أن يحتوي على checkout_session_id و cart_code و email و amount

    # التأكد من وجود البيانات الأساسية

    required_fields = ["id", "metadata", "customer_email", "amount_total"]
    if not all(field in session for field in required_fields):
        return Response({"error": "Invalid session data"}, status=400)

    cart_code = session["metadata"].get("cart_code")
    email = session["customer_email"]
    amount = Decimal(session["amount_total"])

    # إنشاء Order
    try:
        cart = Cart.objects.get(cart_code=cart_code)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)

    order = Order.objects.create(
        stripe_checkout_id=session["id"],
        amount=amount,
        currency="USD",
        customer_email=email,
        status="Paid"
    )

    # نسخ عناصر Cart إلى OrderItems
    for item in cart.cartitems.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

 
    cart.delete()

    return Response({"message": "Order created successfully", "order_id": order.id})

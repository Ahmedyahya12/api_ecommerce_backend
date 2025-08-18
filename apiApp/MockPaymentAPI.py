from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, Order, OrderItem, Product
from uuid import uuid4
from decimal import Decimal

# ------------------------
# محاكاة جلسة الدفع
# ------------------------
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
        "status": "mock_pending"
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

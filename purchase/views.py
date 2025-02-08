from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import permission_classes
from rest_framework import status
from .serializers import *
from .models import *
from user.models import User

# Create your views here.
@api_view(['GET'])
def test(request):
    return Response({"ok": "hello"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    items_data = request.data.get("items", [])

    if not items_data:
        return Response({"error": "No item selected."}, status=status.HTTP_400_BAD_REQUEST)
    
    order = Order.objects.create(user=user)

    for item in items_data:
        product_id = item.get("product_id")
        amount = item.get("amount")

        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({"error": f"Product {product_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        OrderItem.objects.create(
            order=order,
            product=product,
            amount=amount, 
        )
    
    order.save()

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_order(request, pk):
    order = get_object_or_404(Order, order_id=pk)

    if order.user != request.user:
        return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    
    if order.order_status != Order.StatusChoices.PENDING:
        return Response({"error": "Order is already completed or canceled."}, status=status.HTTP_400_BAD_REQUEST)


    order.order_status = Order.StatusChoices.COMPLETED
    order.save()

    for order_item in OrderItem.objects.filter(order=order):
        Transaction.objects.create(
            order_item=order_item,
            transaction_status=Transaction.StatusChoices.COMPLETED
        )

    return Response({"message": "Order confirmed and transactions created"}, status=status.HTTP_200_OK)

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .serializers import *


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    

@api_view(['POST'])
def create_product(request):
    product = ProductSerializer(data=request.data)

    if Product.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This product already exists')
    
    if product.is_valid():
        product.save()
        return Response(product.data
        )
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def view_product(request):
    if request.query_params:
        products = Product.objects.filter(**request.query_params.dict())
    else:
        products = Product.objects.all()
 
    if products:
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def view_specify_product(request, pk):
    try:
        product = Product.objects.get(product_id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
def update_product(request, pk):
    product = Product.objects.get(product_id=pk)
    data = ProductSerializer(instance=product, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['DELETE'])
def delete_product(request, pk):
    product = get_object_or_404(Product, product_id=pk)
    product.delete()
    return Response({f"Deleted product."}, status=status.HTTP_202_ACCEPTED)

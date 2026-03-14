from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializer import ProductSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ProductListCreateAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()

        vendor_id = request.GET.get("vendor_id")

        if vendor_id:
            products = products.filter(
                vendorproductmapping__vendor_id=vendor_id
            )

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None


    def get(self, request, pk):
        product = self.get_object(pk)

        if not product:
            return Response({"error": "Product not found"}, status=404)

        serializer = ProductSerializer(product)
        return Response(serializer.data)


    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):
        product = self.get_object(pk)

        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


    @swagger_auto_schema(request_body=ProductSerializer)
    def patch(self, request, pk):
        product = self.get_object(pk)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()

        return Response(status=204)
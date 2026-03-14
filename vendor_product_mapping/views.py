from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VendorProductMapping
from .serializer import VendorProductMappingSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class VendorProductMappingListCreateAPIView(APIView):

    def get(self, request):
        mappings = VendorProductMapping.objects.all()
        serializer = VendorProductMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=VendorProductMappingSerializer)
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return VendorProductMapping.objects.get(pk=pk)
        except VendorProductMapping.DoesNotExist:
            return None

    def get(self, request, pk):
        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=VendorProductMappingSerializer)
    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    @swagger_auto_schema(request_body=VendorProductMappingSerializer)
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=204)
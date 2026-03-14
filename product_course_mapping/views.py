from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProductCourseMapping
from .serializer import ProductCourseSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class ProductCourseMappingListCreateAPIView(APIView):

    def get(self, request):
        mappings =ProductCourseMapping.objects.all()
        serializer = ProductCourseSerializer(mappings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductCourseSerializer)
    def post(self, request):
        serializer = ProductCourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return ProductCourseMapping.objects.get(pk=pk)
        except ProductCourseMapping.DoesNotExist:
            return None

    def get(self, request, pk):
        mapping = self.get_object(pk)

        if not mapping:
            return Response({"error": "Mapping not found"}, status=404)

        serializer = ProductCourseSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductCourseSerializer)
    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseSerializer(mapping, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    @swagger_auto_schema(request_body=ProductCourseSerializer)
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseSerializer(mapping, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=204)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Certification
from .serializer import CertificationSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



class CertificationListCreateAPIView(APIView):

    def get(self, request):
        courses = Certification.objects.all()
        
        course_id = request.GET.get("course_id")

        if course_id:
            certifications = certifications.filter(
                coursecertificationmapping__course_id=course_id
            )
        serializer = CertificationSerializer(courses, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CertificationSerializer)
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Certification.objects.get(pk=pk)
        except Certification.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)

        if not course:
            return Response({"error": "Course not found"}, status=404)

        serializer =CertificationSerializer(course)
        return Response(serializer.data)


    @swagger_auto_schema(request_body=CertificationSerializer)
    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CertificationSerializer(course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


    @swagger_auto_schema(request_body=CertificationSerializer)
    def patch(self, request, pk):
        course = self.get_object(pk)
        serializer = CertificationSerializer(course, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response(status=204)
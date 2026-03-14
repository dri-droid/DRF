from rest_framework import serializers
from .models import ProductCourseMapping

class ProductCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCourseMapping
        fields = "__all__"

    def validate(self, data):

        product = data.get('product')
        course = data.get('course')
        primary_mapping = data.get('primary_mapping')

        if ProductCourseMapping.objects.filter(
            product=product,
            course=course
        ).exists():
            raise serializers.ValidationError(
                "This product-course mapping already exists"
            )

        if primary_mapping:
            if ProductCourseMapping.objects.filter(
                product=product,
                primary_mapping=True
            ).exists():
                raise serializers.ValidationError(
                    "This product already has a primary course mapping"
                )

        return data
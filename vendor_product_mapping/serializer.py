from rest_framework import serializers
from .models import VendorProductMapping

class VendorProductMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProductMapping
        fields = "__all__"
    
    def validate(self, data):
        vendor = data.get('vendor')
        product = data.get('product')
        primary_mapping = data.get('primary_mapping')

        if VendorProductMapping.objects.filter(
            vendor=vendor,
            product=product
        ).exists():
            raise serializers.ValidationError(
                "This vendor-product mapping already exists"
            )

        if primary_mapping:
            if VendorProductMapping.objects.filter(
                vendor=vendor,
                primary_mapping=True
            ).exists():
                raise serializers.ValidationError(
                    "This vendor already has a primary product mapping"
                )

        return data
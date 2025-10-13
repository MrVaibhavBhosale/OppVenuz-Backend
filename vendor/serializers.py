from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"

class VendorBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "business_name", "email", "contact_number", "working_since", "years_of_experience"]

class VendorDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "description"]
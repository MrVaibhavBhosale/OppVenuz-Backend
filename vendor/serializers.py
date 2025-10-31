from rest_framework import serializers
from .models import Vendor, Vendor_registration, VendorDocument
from django.contrib.auth import authenticate
import re
from django.db import models
from django.db.models import Q


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


class LocationSerializer(serializers.Serializer):
    pincode = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    latitude = serializers.DecimalField(max_digits=13, decimal_places=6, required=True)
    longitude = serializers.DecimalField(max_digits=13, decimal_places=6, required=True)


class VendorDocumentSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="verification.phone", read_only=True)
    company_type = serializers.CharField(source="company_type.company_type", read_only=True)
    class Meta:
        model = VendorDocument
        fields = ['id', 'phone', 'company_type', 'document_type', 'document_url', 'status']

class VendorSignupSerializer(serializers.ModelSerializer):
    location = LocationSerializer(write_only=True)
    mpin = serializers.CharField(write_only=True, required=True)
    date_of_birth = serializers.DateField(input_formats=['%Y-%m-%d', '%d-%m-%Y'])
    documents = VendorDocumentSerializer(many=True, required=False)

    class Meta:
        model = Vendor_registration
        fields = [
            'first_name', 'middle_name', 'last_name', 'email', 'contact_no', 'whatsapp_no',
            'gender', 'date_of_birth', 'mpin',
            'business_name', 'service_id', 'best_suited', 'city_id', 'state_id',
            'location', 'working_since', 'year_of_experience',
            'terms_conditions', 'privacy_policy', 'payment_cancellation',
            'documents', 'document_id', 'payment_status'
        ]
        extra_kwargs = {
            'terms_conditions': {'required': True},
            'privacy_policy': {'required': True},
            'payment_cancellation': {'required': True},
        }

    def validate_email(self, value):
        if value and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_contact_no(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Contact number must contain digits only.")
        if not 10 <= len(value) <= 12:
            raise serializers.ValidationError("Contact number must be between 10 and 12 digits.")
        return value

    def validate_whatsapp_no(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("WhatsApp number must contain digits only.")
        if value and not 10 <= len(value) <= 12:
            raise serializers.ValidationError("WhatsApp number must be between 10 and 12 digits.")
        return value

    def validate_mpin(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("MPIN must contain only digits.")
        if len(value) < 4 or len(value) > 6:
            raise serializers.ValidationError("MPIN must be 4–6 digits long.")
        return value

    def validate_year_of_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Year of experience cannot be negative.")
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        contact_no = attrs.get('contact_no')
        service_id = attrs.get('service_id')

        if Vendor_registration.objects.filter(
            models.Q(email=email) | models.Q(contact_no=contact_no),
            service_id=service_id
        ).exists():
            raise serializers.ValidationError(
                "Vendor with this email or contact number is already registered for this service."
            )
        return attrs

    def create(self, validated_data):
        # Handle location
        location = validated_data.pop('location', None)
        if location:
            validated_data['pincode'] = location.get('pincode')
            validated_data['address'] = location.get('address')
            validated_data['latitude'] = location.get('latitude')
            validated_data['longitude'] = location.get('longitude')

        # Extract documents data (if provided)
        documents_data = validated_data.pop('documents', [])

        # Extract MPIN
        mpin = validated_data.pop('mpin')
        user = Vendor_registration(is_active=True, **validated_data)
        user.set_mpin(mpin)
        user.save()

        # Save each document linked to this vendor
        for doc_data in documents_data:
            VendorDocument.objects.create(vendor=user, **doc_data)

        user.refresh_from_db()
        return user

    def to_representation(self, instance):
        return {
            "vendor_id": instance.vendor_id,
            "business_name": instance.business_name,
            "first_name": instance.first_name,
            "middle_name": instance.middle_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "contact_no": instance.contact_no,
            "whatsapp_no": instance.whatsapp_no,
            "gender": instance.gender,
            "date_of_birth": instance.date_of_birth,
            "city": getattr(instance.city_id, 'city_name', None),
            "state": getattr(instance.state_id, 'state_name', None),
            "pincode": instance.pincode,
            "address": instance.address,
            "service_name": getattr(instance.service_id, 'service_name', None),
            "best_suited_for": getattr(instance.best_suited, 'subcat_name', None),
            "working_since": instance.working_since,
            "year_of_experience": instance.year_of_experience,
            "referral_code": instance.referral_code,
            "document_id": instance.document_id,
            "payment_status": instance.payment_status,
            "created_at": instance.created_at.isoformat() if instance.created_at else None,
            # "documents": VendorDocumentSerializer(instance.documents.all(), many=True).data
        }
    

class VendorLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    mpin = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        mpin = attrs.get('mpin')

        user = authenticate(username=username, mpin=mpin)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        
        attrs['user'] = user
        return attrs
    

class VendorDataSerializer(serializers.ModelSerializer):
    mpin = serializers.CharField(write_only=True)
    documents = VendorDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor_registration
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "vendor_id": instance.vendor_id,
            "business_name": instance.business_name,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "contact_no": instance.contact_no,
            "gender": instance.gender,
            "date_of_birth": instance.date_of_birth,
            "city": getattr(instance.city_id, 'city_name', None),
            "state": getattr(instance.state_id, 'state_name', None),
            "pincode": instance.pincode,
            "address": instance.address,
            "service_name": getattr(instance.service_id, 'service_name', None),
            "best_suited_for": getattr(instance.best_suited, 'subcat_name', None),
            "working_since": instance.working_since,
            "year_of_experience": instance.year_of_experience,
            "referral_code": instance.referral_code,
            "created_at": instance.created_at.isoformat() if instance.created_at else None,
            "documents": VendorDocumentSerializer(instance.documents.all(), many=True).data
        }


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField(required=False, allow_blank=True)
    purpose = serializers.CharField(required=False, default='verification')

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField(required=False, allow_blank=True)
    otp = serializers.CharField(max_length=10)
    target = serializers.ChoiceField(
        choices=[('email', 'email'), ('phone', 'phone'), ('both', 'both')],
        default='both'
    )

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import (
Role_master, 
Service_master, 
Best_suited_for, 
State_master, 
Payment_type,
document_type,
)

 # Role serializers
class RoleMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role_master
        fields = '__all__'
        read_only_fields = ('created_at', 'created_by', 'updated_at', 'updated_by','status')

    def validate_role_name(self, value):
        if Role_master.objects.filter(role_name=value).exists():
            raise ValidationError("Role name already exists.")
        return value

 # Best suited for serializers
class BestSuitedForSerializer(serializers.ModelSerializer):
    class Meta:
        model = Best_suited_for
        fields = '__all__'
        read_only_fields = ('created_at', 'created_by', 'updated_at', 'updated_by','status')

    def validate_name(self, value):
        if Best_suited_for.objects.filter(name=value).exists():
            raise ValidationError("Name already exists.")
        return value

 # State serializers
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State_master
        fields = '__all__'
        read_only_fields = ('created_at', 'created_by', 'updated_at', 'updated_by','status')

    def validate_name(self, value):
        if State_master.objects.filter(state_name=value).exists():
            raise ValidationError("State already exists.")
        return value

 # Payment Type serializers
class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_type
        fields = '__all__'
        read_only_fields = ('created_at', 'created_by', 'updated_at', 'updated_by','status')

    def validate_name(self, value):
        if Payment_type.objects.filter(payment_type=value).exists():
            raise ValidationError("Payment Type already exists.")
        return value
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_master
        fields = '__all__'
        read_only_fields = ('created_at', 'created_by', 'updated_at', 'updated_by','status')

    def validate_service_name(self, value):
        if Service_master.objects.filter(service_name=value).exists():
            raise ValidationError("Service name already exists")
        return value
    def validate(self, data):
        if data.get("registration_charges") is not None and data["registration_charges"] < 0:
            raise ValidationError({"registration_charges" : "registration charges can not be negative"})
        return data

class document_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = document_type
        fields = ['id', 'document_type', 'status', 'created_by', 'updated_by', 'updated_at']
        read_only_fields = ['created_by', 'updated_by', 'updated_at']

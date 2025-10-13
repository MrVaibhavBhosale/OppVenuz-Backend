from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Model For Role 
class Role_master(models.Model):

    role_name = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=1)

    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name
    
# Model For Best Suited For
class Best_suited_for(models.Model):

    name = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(default=1)

    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Model For State
class State_master(models.Model):

    state_name = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(default=1)

    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.state_name

# Model For City
class City_master(models.Model):
    state = models.ForeignKey(
        State_master, 
        on_delete=models.CASCADE,        
        related_name='cities'           
    )
    city_name = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(default=1)

    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city_name}, {self.state.state_name}"
    
# Model For Payment Type
class Payment_type(models.Model):

    payment_type = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(default=1)

    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_type
class Service_master(models.Model):
    service_name = models.CharField(max_length=255, unique= True)
    registration_charges = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.service_name

class document_type(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
        (3, 'Deleted'),
    )

    document_type = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)

    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.document_type


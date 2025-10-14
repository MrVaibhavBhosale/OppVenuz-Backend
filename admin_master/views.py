from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
import logging
from rest_framework.views import APIView

from .models import (
    Role_master, 
    Service_master, 
    Best_suited_for, 
    State_master, 
    Payment_type,
    document_type
)

from .serializers import (
    RoleMasterSerializer, 
    ServiceSerializer, 
    BestSuitedForSerializer, 
    StateSerializer, 
    PaymentTypeSerializer,
    document_typeSerializer
)

logger = logging.getLogger("django")

# =====================================================
# ✅ ADMIN ROLES
# =====================================================

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Admin Roles']))
class RoleCreateView(generics.CreateAPIView):
    queryset = Role_master.objects.all()
    serializer_class = RoleMasterSerializer
  

    def perform_create(self, serializer):
        user_fullname = getattr(self.request.user, 'fullname', self.request.user.username)
        serializer.save(created_by=user_fullname, updated_by=user_fullname)


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Admin Roles']))
class RoleListView(generics.ListAPIView):
    serializer_class = RoleMasterSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Role_master.objects.filter(status=1).order_by('-id')
        role = self.request.query_params.get('role_name', None)
        if role:
            queryset = queryset.filter(role_name__icontains=role)
            if not queryset.exists():
                logger.warning(f"{role} no such role exists")
                raise ValidationError({"role_name": f"{role} no such role exists"})
        return queryset


@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Admin Roles']))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['Admin Roles']))
class RoleUpdateView(generics.UpdateAPIView):
    queryset = Role_master.objects.all()
    serializer_class = RoleMasterSerializer
    
    lookup_field = 'id'

    def perform_update(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        role_name = data.get('role_name', None)

        if role_name and not role_name.replace(' ', '').isalpha():
            logger.warning(f"Invalid role name: {role_name}")
            raise ValidationError({"role_name": "Role name must contain only letters and spaces."})

        updated_by = getattr(user, "fullname", user.username)
        serializer.save(updated_by=updated_by)


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Admin Roles']))
class RoleDeleteView(generics.DestroyAPIView):
    queryset = Role_master.objects.all()
    serializer_class = RoleMasterSerializer
   
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            instance.status = 2
            instance.updated_by = getattr(user, "fullname", user.username)
            instance.updated_at = timezone.now()
            instance.save(update_fields=['status', 'updated_by', 'updated_at'])
            return Response({"message": "Role deleted successfully."})
        except Role_master.DoesNotExist:
            logger.warning(f"Role ID {kwargs.get('id')} not found")
            return Response({"error": "Role not found"}, status=404)
        except Exception as e:
            logger.error(f"Error deleting role: {str(e)}")
            return Response({"error": str(e)}, status=500)



# =====================================================
# ✅ ADMIN BEST SUITED FOR
# =====================================================

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Admin Best Suited For']))
class BestSuitedForCreateView(generics.CreateAPIView):
    queryset = Best_suited_for.objects.all()
    serializer_class = BestSuitedForSerializer
   

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        name = data.get('name', None) 
        if name and not name.replace(' ', '').isalpha():
            raise ValidationError({"name": "Name must contain only letters and spaces."})
            
        user_fullname = getattr(self.request.user, 'fullname', self.request.user.username)
        serializer.save(created_by=user_fullname, updated_by=user_fullname)


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Admin Best Suited For']))
class BestSuitedForListView(generics.ListAPIView):
    serializer_class = BestSuitedForSerializer
    permission_classes = [AllowAny]
   

    def get_queryset(self):
        queryset = Best_suited_for.objects.filter(status=1).order_by('-id')
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(role_name__icontains=name)
            if not queryset.exists():
                logger.warning(f"{name} no such name exists")
                raise ValidationError({"name": f"{name} no such name exists"})
        return queryset


@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Admin Best Suited For']))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['Admin Best Suited For']))
class BestSuitedForUpdateView(generics.UpdateAPIView):
    queryset = Best_suited_for.objects.all()
    serializer_class = BestSuitedForSerializer
   
    lookup_field = 'id'

    def perform_update(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        name = data.get('name', None)

        if name and not name.replace(' ', '').isalpha():
            logger.warning(f"Invalid name: {name}")
            raise ValidationError({"name": "Name must contain only letters and spaces."})

        updated_by = getattr(user, "fullname", user.username)
        serializer.save(updated_by=updated_by)


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Admin Best Suited For']))
class BestSuitedForDeleteView(generics.DestroyAPIView):
    queryset = Best_suited_for.objects.all()
    serializer_class = BestSuitedForSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            instance.status = 2
            instance.updated_by = getattr(user, "fullname", user.username)
            instance.updated_at = timezone.now()
            instance.save(update_fields=['status', 'updated_by', 'updated_at'])
            return Response({"message": "Name deleted successfully."})
        except Best_suited_for.DoesNotExist:
            logger.warning(f"Name ID {kwargs.get('id')} not found")
            return Response({"error": "Name not found"}, status=404)
        except Exception as e:
            logger.error(f"Error deleting Name: {str(e)}")
            return Response({"error": str(e)}, status=500)


# =====================================================
# ✅ ADMIN STATE
# =====================================================

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Admin State']))
class StateCreateView(generics.CreateAPIView):
    queryset = State_master.objects.all()
    serializer_class = StateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = serializer.validated_data
        state_name = data.get('state_name', None) 
        if state_name and not state_name.replace(' ', '').isalpha():
            raise ValidationError({"state_name": "State Name must contain only letters and spaces."})
            
        user_fullname = getattr(self.request.user, 'fullname', self.request.user.username)
        serializer.save(created_by=user_fullname, updated_by=user_fullname)


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Admin State']))
class StateListView(generics.ListAPIView):
    serializer_class = StateSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = State_master.objects.filter(status=1).order_by('-id')
        state_name = self.request.query_params.get('state_name', None)
        if state_name:
            queryset = queryset.filter(state_name__icontains=state_name)
            if not queryset.exists():
                logger.warning(f"{state_name} no such State exists")
                raise ValidationError({"state_name": f"{state_name} no such name exists"})
        return queryset


@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Admin State']))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['Admin State']))
class StateUpdateView(generics.UpdateAPIView):
    queryset = State_master.objects.all()
    serializer_class = StateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_update(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        state_name = data.get('state_name', None)

        if state_name and not state_name.replace(' ', '').isalpha():
            logger.warning(f"Invalid state name: {state_name}")
            raise ValidationError({"state_name": "State Name must contain only letters and spaces."})

        updated_by = getattr(user, "fullname", user.username)
        serializer.save(updated_by=updated_by)


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Admin State']))
class StateDeleteView(generics.DestroyAPIView):
    queryset = State_master.objects.all()
    serializer_class = StateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            instance.status = 2
            instance.updated_by = getattr(user, "fullname", user.username)
            instance.updated_at = timezone.now()
            instance.save(update_fields=['status', 'updated_by', 'updated_at'])
            return Response({"message": "State deleted successfully."})
        except Best_suited_for.DoesNotExist:
            logger.warning(f"State ID {kwargs.get('id')} not found")
            return Response({"error": "State not found"}, status=404)
        except Exception as e:
            logger.error(f"Error deleting State: {str(e)}")
            return Response({"error": str(e)}, status=500)


# =====================================================
# ✅ ADMIN PAYMENT TYPE
# =====================================================

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Admin Payment Types']))
class PaymentTypeCreateView(generics.CreateAPIView):
    queryset = Payment_type.objects.all()
    serializer_class = PaymentTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = serializer.validated_data
        payment_type = data.get('payment_type', None) 
        if payment_type and not payment_type.replace(' ', '').isalpha():
            raise ValidationError({"payment_type": "Payment Type must contain only letters and spaces."})
            
        user_fullname = getattr(self.request.user, 'fullname', self.request.user.username)
        serializer.save(created_by=user_fullname, updated_by=user_fullname)


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Admin Payment Types']))
class PaymentTypeListView(generics.ListAPIView):
    serializer_class = PaymentTypeSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Payment_type.objects.filter(status=1).order_by('-id')
        payment_type = self.request.query_params.get('payment_type', None)
        if payment_type:
            queryset = queryset.filter(payment_type__icontains=payment_type)
            if not queryset.exists():
                logger.warning(f"{payment_type} no such payment type exists")
                raise ValidationError({"payment_type": f"{payment_type} no such payment type exists"})
        return queryset


@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Admin Payment Types']))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['Admin Payment Types']))
class PaymentTypeUpdateView(generics.UpdateAPIView):
    queryset = Payment_type.objects.all()
    serializer_class = PaymentTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_update(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        payment_type = data.get('payment_type', None)

        if payment_type and not payment_type.replace(' ', '').isalpha():
            logger.warning(f"Invalid payment type: {payment_type}")
            raise ValidationError({"payment_type": "payment type must contain only letters and spaces."})

        updated_by = getattr(user, "fullname", user.username)
        serializer.save(updated_by=updated_by)


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Admin Payment Types']))
class PaymentTypeDeleteView(generics.DestroyAPIView):
    queryset = Payment_type.objects.all()
    serializer_class = PaymentTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            instance.status = 2
            instance.updated_by = getattr(user, "fullname", user.username)
            instance.updated_at = timezone.now()
            instance.save(update_fields=['status', 'updated_by', 'updated_at'])
            return Response({"message": "Payment Type deleted successfully."})
        except Best_suited_for.DoesNotExist:
            logger.warning(f"Payment type ID {kwargs.get('id')} not found")
            return Response({"error": "payment type not found"}, status=404)
        except Exception as e:
            logger.error(f"Error deleting Payment type: {str(e)}")
            return Response({"error": str(e)}, status=500)



# =====================================================
# ✅ ADMIN SERVICES
# =====================================================

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Admin Services']))
class ServiceCreateView(generics.CreateAPIView):
    queryset = Service_master.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_fullname = getattr(self.request.user, 'fullname', self.request.user.username)
        serializer.save(created_by=user_fullname, updated_by=user_fullname)


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Admin Services']))
class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Service_master.objects.all()
        service = self.request.query_params.get('service_name', None)
        if service:
            queryset = queryset.filter(service_name__icontains=service)
            if not queryset.exists():
                logger.warning(f"{service} no such service exists")
                raise ValidationError({"service_name": f"{service} no such service exists"})
        return queryset


@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Admin Services']))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['Admin Services']))
class ServiceUpdateView(generics.UpdateAPIView):
    queryset = Service_master.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_update(self, serializer):
        user = self.request.user
        data = serializer.validated_data

        service_name = data.get('service_name', None)
        if service_name and not service_name.replace(' ', '').isalpha():
            logger.warning(f"Invalid service name: {service_name}")
            raise ValidationError({"service_name": "Service name must contain only letters and spaces."})

        registration_charges = data.get('registration_charges', None)
        if registration_charges is not None and registration_charges < 0:
            logger.warning("Invalid registration charges")
            raise ValidationError({"registration_charges": "Must be a positive number."})

        updated_by = getattr(user, "fullname", user.username)
        serializer.save(updated_by=updated_by)


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Admin Services']))
class ServiceDeleteView(generics.DestroyAPIView):
    queryset = Service_master.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            instance.status = 2
            instance.updated_by = getattr(user, "fullname", user.username)
            instance.updated_at = timezone.now()
            instance.save(update_fields=['status', 'updated_by', 'updated_at'])
            return Response({"message": "Service deleted successfully."})
        except Service_master.DoesNotExist:
            logger.warning(f"Service ID {kwargs.get('id')} not found")
            return Response({"error": "Service not found"}, status=404)
        except Exception as e:
            logger.error(f"Error deleting service: {str(e)}")
            return Response({"error": str(e)}, status=500)


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Document Services']))
class DocumentTypeCreateView(generics.CreateAPIView):
    queryset = document_type.objects.all()
    serializer_class = document_typeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_fullname = getattr(self.request.user, 'fullname', self.request.user.username)
        serializer.save(created_by=user_fullname, updated_by=user_fullname)
        logger.info(f"Document created by user {user_fullname} with data: {self.request.data}")

@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Document Services']))
class DocumentTypeListView(generics.ListAPIView):
    serializer_class = document_typeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = document_type.objects.filter(status=1)
        doc_type = self.request.query_params.get('document_type', None)
        if doc_type:
            queryset = queryset.filter(document_type__icontains=doc_type)
            if not queryset.exists():
                logger.warning(f"{doc_type} no such document type exists")
                raise ValidationError({"document_type": f"{doc_type} no such document type exists"})
        logger.info(f"Document list fetched by user {self.request.user}")
        return queryset

@method_decorator(name='put', decorator=swagger_auto_schema(tags=['Document Services']))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['Document Services']))
class DocumentTypeUpdateView(generics.UpdateAPIView):
    queryset = document_type.objects.all()
    serializer_class = document_typeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        user = self.request.user
        data = serializer.validated_data

        doc_type_name = data.get('document_type', None)
        if doc_type_name and not doc_type_name.replace(' ', '').isalpha():
            logger.warning(f"Invalid document_type name: {doc_type_name}")
            raise ValidationError({"document_type": "Document type must contain only letters and spaces."})

        updated_by = getattr(user, "fullname", user.username)
        serializer.save(updated_by=updated_by)
        logger.info(f"Document ID {self.get_object().id} updated by user {updated_by}")

@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['Document Services']))
class DocumentTypeDeleteView(generics.DestroyAPIView):
    queryset = document_type.objects.all()
    serializer_class = document_typeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            instance.status = 3  
            instance.updated_by = getattr(user, "fullname", user.username)
            instance.updated_at = timezone.now()
            instance.save(update_fields=['status', 'updated_by', 'updated_at'])
            logger.info(f"Document ID {instance.id} soft deleted by user {user}")
            return Response({"message": "Document deleted successfully."})
        except document_type.DoesNotExist:
            logger.warning(f"Document ID {kwargs.get('pk')} not found for delete")
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

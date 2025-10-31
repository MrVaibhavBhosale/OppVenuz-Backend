from django.http import JsonResponse
from rest_framework import generics, permissions, status
from django.db import transaction
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from admin_master.models import CompanyTypeMaster

from decouple import config
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from datetime import timedelta
import traceback

from .models import (
    Vendor, 
    VendorDevice, 
    Vendor_registration, 
    EmailPhoneVerification,
    VendorDocument,
)

from .serializers import (
    VendorSerializer,
    VendorBasicSerializer,
    VendorDescriptionSerializer,
    VendorSignupSerializer,
    VendorLoginSerializer,
    VendorDataSerializer,
    VerifyEmailOTPSerializer,
    VerifyPhoneOTPSerializer,
    RequestEmailOTPSerializer,
    RequestPhoneOTPSerializer,
    VendorDocumentSerializer,
)

from .utils import generate_numeric_otp, send_otp_email, send_otp_sms
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_agents import parse
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
import logging
import boto3
from rest_framework.views import APIView
logger = logging.getLogger("django")


class VendorBasicDetailsAPI(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = VendorBasicSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "message": "Vendor basic details created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = Vendor.objects.get(id=kwargs.get('id'))
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "message": "Vendor basic details updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class VendorDescriptionAPI(generics.UpdateAPIView):
    serializer_class = VendorDescriptionSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Vendor.objects.all()
    lookup_field = "id"
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "message": "Vendor description updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class VendorListCreateAPI(generics.ListCreateAPIView):
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Vendor.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Fetched all vendors",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "message": "Vendor created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

class VendorRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Vendor.objects.all()
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Vendor fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "status": "success",
            "message": "Vendor updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "status": "success",
            "message": "Vendor deleted successfully"
        }, status=status.HTTP_200_OK)
    
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Vendor Signup']))
class VendorSignupView(generics.GenericAPIView):
    serializer_class = VendorSignupSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
 
        if serializer.is_valid():
            contact_no = serializer.validated_data.get("contact_no")
            uploaded_docs = VendorDocument.objects.filter(
            vendor_business_no=contact_no, 
            status="TEMP"
        )
            document_ids = list(uploaded_docs.values_list("id", flat=True))
            vendor = serializer.save()
            if document_ids:
                vendor.document_id = document_ids
                vendor.save(update_fields=["document_id"])

                # Update VendorDocument status to PERMANENT
                uploaded_docs.update(status="PERMANENT")
                vendor.save()
 
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_string)
 
            if user_agent.is_mobile:
                device_type = "Mobile"
            elif user_agent.is_tablet:
                device_type = "Tablet"
            elif user_agent.is_pc:
                device_type = "Desktop"
            else:
                device_type = "Other"
 
            device_info = {
                "device_type": device_type,
                "os_version": user_agent.os.version_string,
                "browser_name": user_agent.browser.family,
                "browser_version": user_agent.browser.version_string,
            }
 
            # Save or update device info
            VendorDevice.objects.update_or_create(
                vendor_id=vendor,
                device_type=device_info["device_type"],
                os_version=device_info["os_version"],
                browser_name=device_info["browser_name"],
                defaults={"browser_version": device_info["browser_version"]}
            )
 
            refresh = RefreshToken.for_user(vendor)
 
            vendor_data = self.get_serializer(vendor).data
            vendor_data.update({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "device_info": device_info
                })
            return Response({
                "status": True,
                "message": "Vendor registered successfully.",
                "data": vendor_data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": False,
                "message": "Validation failed.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['Vendor login']))
class VendorLoginView(generics.GenericAPIView):
    serializer_class = VendorLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": False,
                "message": "Invalid credentials",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)

        if user_agent.is_mobile:
            device_type = "Mobile"
        elif user_agent.is_tablet:
            device_type = "Tablet"
        elif user_agent.is_pc:
            device_type = "Desktop"
        else:
            device_type = "Other"

        device_info = {
        "device_type": device_type,
        "os_version": user_agent.os.version_string,
        "browser_name": user_agent.browser.family,
        "browser_version": user_agent.browser.version_string,
        }

        # Save or update device
        VendorDevice.objects.update_or_create(
            vendor_id=user,
            device_type=device_info["device_type"],
            os_version=device_info["os_version"],
            browser_name=device_info["browser_name"],
            defaults={
                "browser_version": device_info["browser_version"],
            }
            )
        
        refresh = RefreshToken.for_user(user)

        vendor_data = VendorDataSerializer(user).data
        vendor_data.update({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "device_info": device_info
        })

        return Response({
            "status": True,
            "message": "Login successful",
            "data": vendor_data
        }, status=status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['sendEmail- otp']))
class RequestEmailOTPView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RequestEmailOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')

        try:
            with transaction.atomic():
                # Get or create verification record first
                verification, created = EmailPhoneVerification.objects.get_or_create(email=email)

                # Cooldown check (60 seconds)
                if (
                    verification.email_otp_created_at and 
                    timezone.now() - verification.email_otp_created_at < timedelta(seconds=60)
                ):
                    return Response({
                        "status": False,
                        "message": "Please wait at least 60 seconds before requesting another OTP."
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)

                # generate and set OTP using model method
                otp = generate_numeric_otp()
                verification.set_email_otp(otp)

        except Exception as e:
            logger.exception("Error generating email OTP")
            return Response({
                "status": False,
                "message": f"Failed to process OTP: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        # send email OTP
        email_sent = send_otp_email(email, otp)
        return Response({
            "status": True,
            "message": "OTP sent successfully.",
            "email_sent": email_sent == 202
        }, status=status.HTTP_200_OK)


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['sendPhone otp'])) 
class RequestPhoneOTPView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RequestPhoneOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')

        try:
            with transaction.atomic():
                # Get or create verification record first
                verification, created = EmailPhoneVerification.objects.get_or_create(phone=phone)

                # Check if the user is temporarily blocked
                if verification._is_blocked():
                    return Response({
                        "status": False,
                        "message": "Too many failed attempts. Please try again later."
                    }, status=status.HTTP_403_FORBIDDEN)
                
                # Cooldown check (60 seconds)
                if (
                    verification.phone_otp_created_at and 
                    timezone.now() - verification.phone_otp_created_at < timedelta(seconds=60)
                ):
                    return Response({
                        "status": False,
                        "message": "Please wait at least 60 seconds before requesting another OTP."
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)

                # Generate and set OTP
                otp = generate_numeric_otp()
                verification.set_phone_otp(otp)

        except ValueError as ve:
            # Raised if blocked due to too many attempts
            logger.warning(f"Blocked OTP request for {phone}: {str(ve)}")
            return Response({
                "status": False,
                "message": str(ve)
            }, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            logger.exception("Error generating phone OTP")
            return Response({
                "status": False,
                "message": f"Failed to process OTP: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Send SMS OTP
        sms_sent = send_otp_sms(phone, otp)

        return Response({
            "status": True,
            "message": "OTP sent successfully.",
            "sms_sent": sms_sent
        }, status=status.HTTP_200_OK)
    

@method_decorator(name='post', decorator=swagger_auto_schema(tags=['VerifyOTP - Email']))
class VerifyEmailOTPView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = VerifyEmailOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        raw_otp = serializer.validated_data['otp']

        verification = get_object_or_404(EmailPhoneVerification, email=email)

        if verification._is_blocked():
            return Response({
                "status": False,
                "message": "Too many attempts. Try again later."
            }, status=status.HTTP_403_FORBIDDEN)
        
        # validate OTP
        if not verification.check_email_otp(raw_otp):
            verification.mark_attempt()
            return Response({
                "status": False,
                "message": "Invalid or expired OTP."
            }, status=status.HTTP_400_BAD_REQUEST)

        # mark email as verified
        with transaction.atomic():
            verification.is_email_verified = True
            verification.email_otp = None
            verification.email_otp_created_at = None
            verification.email_otp_expired_at = None
            verification.attempts = 0
            verification.is_blocked_until = None
            verification.save(update_fields=[
                'is_email_verified',
                'email_otp', 'email_otp_created_at', 'email_otp_expired_at',
                'attempts', 'is_blocked_until'
            ])

        return Response({
            "status": True,
            "message": "Email Verified successfully.",
            "is_email_verified": verification.is_email_verified,
        }, status=status.HTTP_200_OK)
    
    
@method_decorator(name='post', decorator=swagger_auto_schema(tags=['VerifyyyOTP - Phone']))
class VerifyPhoneOTPView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = VerifyPhoneOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']
        verification = get_object_or_404(EmailPhoneVerification, phone=phone)

        #check if temporary blocked
        if verification._is_blocked():
            return Response({
                "status": False,
                "message": "Too many attempts. Try again later."
            }, status=status.HTTP_403_FORBIDDEN)

        
        #validate OTP
        if not verification.check_phone_otp(otp):
            verification.mark_attempt()
            return Response({
                "status": False,
                "message": "Invalid or Expired OTP."
            },
            status=status.HTTP_400_BAD_REQUEST)
        
        #mark phone as verified
        with transaction.atomic():
            verification.is_phone_verified = True
            verification.phone_otp = None
            verification.phone_otp_created_at = None
            verification.phone_otp_expired_at = None
            verification.attempts = 0
            verification.is_blocked_until = None
            verification.save(update_fields=['is_phone_verified', 'phone_otp','phone_otp_created_at',
             'phone_otp_expired_at', 'attempts', 'is_blocked_until'
             ])
            
        return Response({
            "status": True,
            "message": "Phone verified successfully.",
            "is_phone_verified": verification.is_phone_verified,
        }, status=status.HTTP_200_OK)


class VendorDocumentUploadAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (OAuth2Authentication, JWTAuthentication)

    def post(self, request, *args, **kwargs):
        try:
            phone = request.data.get("vendor_business_no")
            document_type = request.data.get("document_type")
            section_type = request.data.get("section_type")
            image = request.FILES.get("file")
            company_type_id = request.data.get("company_type")

            if not all([phone, document_type, image, company_type_id]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # Step 1: Get verification entry using phone
            verification = EmailPhoneVerification.objects.filter(phone=phone, is_phone_verified=True).first()
            if not verification:
                return Response({"error": "Phone number not verified"}, status=status.HTTP_400_BAD_REQUEST)

            # Step 2: Get CompanyTypeMaster instance using id
            try:
                company_type_obj = CompanyTypeMaster.objects.get(id=company_type_id)
            except CompanyTypeMaster.DoesNotExist:
                return Response({"error": "Invalid company_type id"}, status=status.HTTP_400_BAD_REQUEST)

            # Step 3: Delete expired TEMP docs
            now = timezone.now()
            VendorDocument.objects.filter(status='TEMP', expires_at__lt=now).update(status='DELETED')

            # Step 4: Upload to S3
            s3 = boto3.client(
                "s3",
                aws_access_key_id=config("s3AccessKey"),
                aws_secret_access_key=config("s3Secret"),
            )
            bucket = config("S3_BUCKET_NAME")
            key = f"vendor_documents/{phone}/{image.name}"
            s3.upload_fileobj(image, bucket, key, ExtraArgs={"ACL": "public-read"})
            document_url = f"https://{bucket}.s3.amazonaws.com/{key}"

            # Step 5: Save in DB
            doc = VendorDocument.objects.create(
                verification=verification,
                company_type=company_type_obj,
                document_type=document_type,
                document_url=document_url,
                status="TEMP",
                expires_at=timezone.now() + timedelta(hours=1),
            )

            serializer = VendorDocumentSerializer(doc)
            return Response({
                "message": f"{document_type} uploaded successfully.",
                "document": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
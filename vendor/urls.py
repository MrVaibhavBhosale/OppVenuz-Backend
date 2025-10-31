from django.urls import path
from .views import (
    VendorBasicDetailsAPI, 
    VendorDescriptionAPI,
    VendorDocumentUploadAPIView,
    VendorListCreateAPI,
    VendorRetrieveUpdateDeleteAPI,
    VendorSignupView,
    VendorLoginView,
    RequestEmailOTPView,
    VerifyEmailOTPView,
    RequestPhoneOTPView,
    VerifyPhoneOTPView
)

urlpatterns = [
    path('basic-details/', VendorBasicDetailsAPI.as_view(), name='vendor-basic-create'),
    path('basic-details/<int:id>/', VendorBasicDetailsAPI.as_view(), name='vendor-basic-update'),
    path('description/<int:id>/', VendorDescriptionAPI.as_view(), name='vendor-description'),
    path('vendors/', VendorListCreateAPI.as_view(), name='vendor-list-create'),
    path('vendors/<int:id>/', VendorRetrieveUpdateDeleteAPI.as_view(), name='vendor-rud'),
    path('signup/', VendorSignupView.as_view(), name="vendor-sihnup"),
    path('login/', VendorLoginView.as_view(), name="login"),
    path('requestEmail-otp/', RequestEmailOTPView.as_view(), name="requestEmail-otp"),
    path('verifyEmail-otp/', VerifyEmailOTPView.as_view(), name="verifyEmail-otp"),
    path('requestPhone-otp/', RequestPhoneOTPView.as_view(), name="requestPhone-otp"),
    path('verifyPhone-otp/', VerifyPhoneOTPView.as_view(), name="verifyPhone-otp"),
    path('uploadDocument/', VendorDocumentUploadAPIView.as_view(), name='upload-document'),

]

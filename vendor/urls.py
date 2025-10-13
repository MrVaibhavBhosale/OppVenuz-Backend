from django.urls import path
from .views import (
    VendorBasicDetailsAPI, 
    VendorDescriptionAPI,
    VendorListCreateAPI,
    VendorRetrieveUpdateDeleteAPI
)

urlpatterns = [
    path('basic-details/', VendorBasicDetailsAPI.as_view(), name='vendor-basic-create'),
    path('basic-details/<int:id>/', VendorBasicDetailsAPI.as_view(), name='vendor-basic-update'),
    path('description/<int:id>/', VendorDescriptionAPI.as_view(), name='vendor-description'),
    path('vendors/', VendorListCreateAPI.as_view(), name='vendor-list-create'),
    path('vendors/<int:id>/', VendorRetrieveUpdateDeleteAPI.as_view(), name='vendor-rud'),
]

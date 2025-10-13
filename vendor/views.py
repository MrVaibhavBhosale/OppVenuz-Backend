from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer, VendorBasicSerializer, VendorDescriptionSerializer

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
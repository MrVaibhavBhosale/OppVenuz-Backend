from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from vendor.models import Vendor_registration

class VendorAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, mpin=None, **kwargs):
        """
        Custom authentication backend for Vendor using email/contact_no + mpin.
        """
        if username is None or mpin is None:
            return None

        try:
            vendor = Vendor_registration.objects.filter(
                Q(email=username) | Q(contact_no=username)
            ).first()
            if vendor and vendor.check_mpin(mpin):
                return vendor
        except Vendor_registration.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Vendor_registration.objects.get(pk=user_id)
        except Vendor_registration.DoesNotExist:
            return None

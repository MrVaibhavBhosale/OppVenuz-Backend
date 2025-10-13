from django.urls import path
from .views import (
    RoleCreateView,
    RoleListView,
    RoleUpdateView,
    RoleDeleteView,
    ServiceCreateView,
    ServiceListView,
    ServiceUpdateView,
    ServiceDeleteView,
    BestSuitedForCreateView,
    BestSuitedForListView,
    BestSuitedForUpdateView,
    BestSuitedForDeleteView,
    StateCreateView,
    StateListView,
    StateUpdateView,
    StateDeleteView,
    PaymentTypeCreateView,
    PaymentTypeListView,
    PaymentTypeUpdateView,
    PaymentTypeDeleteView,
    DocumentTypeCreateView,
    DocumentTypeListView,
    DocumentTypeUpdateView,
    DocumentTypeDeleteView, 
)

urlpatterns = [
    # Role URLs
    path('createRole/', RoleCreateView.as_view(), name="create-role"),
    path('getAllRoles/', RoleListView.as_view(), name="get-role"),
    path('updateRole/<int:id>/', RoleUpdateView.as_view(), name="update-role"),
    path('deleteRole/<int:id>/', RoleDeleteView.as_view(), name="delete-role"),

    # Best Suitef For URLs
    path('createBestSuitedFor/', BestSuitedForCreateView.as_view(), name="create-BestSuitedFor"),
    path('getAllBestSuitedFor/', BestSuitedForListView.as_view(), name="get-BestSuitedFor"),
    path('updateBestSuitedFor/<int:id>/', BestSuitedForUpdateView.as_view(), name="update-BestSuitedFor"),
    path('deleteBestSuitedFor/<int:id>/', BestSuitedForDeleteView.as_view(), name="delete-BestSuitedFor"),

    # State URLs
    path('createState/', StateCreateView.as_view(), name="create-State"),
    path('getAllState/', StateListView.as_view(), name="get-State"),
    path('updateState/<int:id>/', StateUpdateView.as_view(), name="update-State"),
    path('deleteState/<int:id>/', StateDeleteView.as_view(), name="delete-State"),

    # Payment Types URLs
    path('createPaymentType/', PaymentTypeCreateView.as_view(), name="create-PaymentType"),
    path('getAllPaymentType/', PaymentTypeListView.as_view(), name="get-PaymentType"),
    path('updatePaymentType/<int:id>/', PaymentTypeUpdateView.as_view(), name="update-PaymentType"),
    path('deletePaymentType/<int:id>/', PaymentTypeDeleteView.as_view(), name="delete-PaymentType"),


    path('services/', ServiceCreateView.as_view(), name="servie-create"),
    path('getServices/', ServiceListView.as_view(), name="services-get"),
    path('updateservice/<int:id>/', ServiceUpdateView.as_view(), name="service-update"),
    path('deleteservice/<int:id>/', ServiceDeleteView.as_view(), name="delete-service"),

    # Document Type URLs
    path('createDocument/', DocumentTypeCreateView.as_view(), name='document-master-create'),
    path('getAllDocument/', DocumentTypeListView.as_view(), name='document-master-list'),
    path('updateDocument/<int:pk>/', DocumentTypeUpdateView.as_view(), name='document-master-update'),
    path('deleteDocument/<int:pk>/', DocumentTypeDeleteView.as_view(), name='document-master-delete'),

]


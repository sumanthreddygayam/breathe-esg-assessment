from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmissionRecordViewSet, SourceViewSet, TenantViewSet, UploadCsvView, demo_token

router = DefaultRouter()
router.register(r'emission-records', EmissionRecordViewSet, basename='emissionrecord')
router.register(r'sources', SourceViewSet, basename='source')
router.register(r'tenants', TenantViewSet, basename='tenant')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-csv/', UploadCsvView.as_view(), name='upload-csv'),
    path('demo-token/', demo_token, name='demo-token'),
]

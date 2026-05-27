from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tenant, Source, EmissionRecord
from .serializers import TenantSerializer, SourceSerializer, EmissionRecordSerializer
import csv
import io


class EmissionRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = EmissionRecord.objects.all().order_by('-created_at')
    serializer_class = EmissionRecordSerializer

    @action(detail=False, methods=['get'])
    def pending(self, request):
        qs = self.get_queryset().filter(status='pending_review')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        rec = self.get_object()
        user = request.user.username if request.user and request.user.is_authenticated else (request.data.get('user') or 'analyst')
        rec.status = 'approved'
        rec.updated_by = user
        rec.save()
        # create audit log
        try:
            from .models import AuditLog
            AuditLog.objects.create(emission_record=rec, action='approve', performed_by=user, details={})
        except Exception:
            pass
        return Response({'status': 'approved', 'id': rec.id})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        rec = self.get_object()
        user = request.user.username if request.user and request.user.is_authenticated else (request.data.get('user') or 'analyst')
        rec.status = 'rejected'
        rec.updated_by = user
        rec.save()
        try:
            from .models import AuditLog
            AuditLog.objects.create(emission_record=rec, action='reject', performed_by=user, details={})
        except Exception:
            pass
        return Response({'status': 'rejected', 'id': rec.id})


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all().order_by('-ingested_at')
    serializer_class = SourceSerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


from rest_framework.views import APIView


class UploadCsvView(APIView):
    """Simple CSV upload that creates EmissionRecord rows. Expects `tenant_id` and `source_type` in query params."""

    def post(self, request, format=None):
        tenant_id = request.query_params.get('tenant_id')
        source_type = request.query_params.get('source_type', 'unknown')
        file = request.FILES.get('file')
        if not file or not tenant_id:
            return Response({'detail': 'file and tenant_id required'}, status=status.HTTP_400_BAD_REQUEST)

        tenant = Tenant.objects.get(pk=tenant_id)
        raw = file.read().decode('utf-8')
        source = Source.objects.create(tenant=tenant, source_type=source_type, filename=getattr(file, 'name', None), raw_payload=raw)

        reader = csv.DictReader(io.StringIO(raw))
        created = []
        # Route to specialized parsers when known
        st = source_type.lower()
        try:
            if st == 'sap_fuel' or st == 'sap_procurement':
                from .parsers.sap_parser import parse_sap_csv
                created = parse_sap_csv(tenant, source, reader, category='fuel' if 'fuel' in st else 'procurement')
            elif st == 'utility_electricity':
                from .parsers.utility_parser import parse_utility_csv
                created = parse_utility_csv(tenant, source, reader)
            elif st == 'travel_export':
                from .parsers.travel_parser import parse_travel_csv
                created = parse_travel_csv(tenant, source, reader)
            else:
                for row in reader:
                    amount = row.get('consumption') or row.get('quantity') or row.get('amount')
                    unit = row.get('unit') or row.get('units') or ''
                    start = row.get('start_date') or row.get('date')
                    end = row.get('end_date') or row.get('date')
                    rec = EmissionRecord.objects.create(
                        tenant=tenant,
                        source=source,
                        source_row_id=row.get('id') or row.get('row_id') or None,
                        category=source_type,
                        scope=None,
                        start_date=start or None,
                        end_date=end or None,
                        amount=amount or None,
                        unit=unit or None,
                        metadata=row,
                    )
                    created.append(rec.id)
        except Exception as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'created': created})

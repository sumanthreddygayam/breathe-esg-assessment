from ..models import EmissionRecord, Source, Tenant
from decimal import Decimal
from dateutil import parser as dateparser

# Simplified per-passenger-km emission factors (kg CO2e per passenger-km)
EMISSION_FACTORS = {
    'flight': Decimal('0.09'),
    'car': Decimal('0.192'),
}


def parse_travel_csv(tenant: Tenant, source: Source, rows):
    created = []
    for row in rows:
        seg = (row.get('segment_type') or '').lower()
        dist = row.get('distance_km') or row.get('distance')
        try:
            distance = Decimal(str(dist)) if dist not in (None, '', ' ') else None
        except Exception:
            distance = None

        ef = EMISSION_FACTORS.get(seg)
        normalized = None
        if ef and distance is not None:
            normalized = (ef * distance).quantize(Decimal('0.000001'))

        rec = EmissionRecord.objects.create(
            tenant=tenant,
            source=source,
            source_row_id=row.get('trip_id') or None,
            category='travel',
            scope=3,
            start_date=row.get('start_date') or None,
            end_date=row.get('end_date') or None,
            amount=distance,
            unit='passenger-km' if distance is not None else None,
            normalized_unit='kgCO2e' if normalized is not None else None,
            normalized_amount_kgco2e=normalized,
            metadata=row,
        )
        created.append(rec.id)
    return created
